import matplotlib.pyplot as plt
import math

from qiskit.visualization import plot_histogram
from qiskit import transpile
from qiskit import QuantumCircuit, QuantumRegister
from qiskit import IBMQ

provider = IBMQ.load_account()


def list_to_chunks(l, chunk_size):
    """Yield n number of striped chunks from l."""
    for i in range(0, len(l) // chunk_size):
        st = i * chunk_size
        ed = (i + 1) * chunk_size
        yield l[st:ed]


def set_inputs(qc, inp_w, inp_p):
    for i, c in enumerate(inp_w):
        if c == "1":
            qc.x(w[i])

    for i, c in enumerate(inp_p):
        if c == "1":
            qc.x(p[i])


def initialize_s(qc):
    """Apply a H-gate to 'qubits' in qc"""
    qc.h(s)


def oracle(qc: QuantumCircuit, start_pos):
    # if the start_pos'th bit is equal on w and p, then increase
    format_string = "{:0" + str(len(s)) + "b}"
    pos_in_binary = format_string.format(start_pos)
    qc.barrier(label=f"start {pos_in_binary}")

    flipped_s = []
    # Here, we would need a anc line to or the cases then the s1 should be 1
    # there are n-m-1 such cases, w0 = p0, w1=p0 ...
    for k, pos in enumerate(pos_in_binary):  # 10
        if pos == "0":
            flipped_s.append(s[k])
            qc.x(s[k])

    for offset, match_bit in enumerate(bit_matches):
        flipped_w = []
        flipped_p = []

        if inp_p[0 + offset] == "0":
            flipped_p.append(p[0 + offset])
            qc.x(p[0 + offset])

            flipped_w.append(w[0 + start_pos + offset])
            qc.x(w[0 + start_pos + offset])

        qc.mcx(list(s) + [w[start_pos + offset], p[0 + offset]], bit_matches[offset])

        # qc.ccz(w[start_pos + offset], p[0 + offset], s[k])

        if len(flipped_w):
            qc.x(flipped_w)
        if len(flipped_p):
            qc.x(flipped_p)

    if len(flipped_s):
        qc.x(flipped_s)
    qc.barrier(label=f"end {pos_in_binary}")


def diffusion(qc: QuantumCircuit):
    """Apply a diffusion circuit to the register 'qubits' in qc"""
    qc.h(s)
    qc.x(s)

    qc.mcx(s, match)
    qc.z(match)

    qc.x(s)
    qc.h(s)


def measurement_s(qc):
    num_bits = len(s)
    meas = QuantumCircuit(num_bits, num_bits)
    meas.measure(list(range(num_bits)), list(range(num_bits)))
    qc.compose(meas, inplace=True, qubits=s)


def execute(qc, num_shots=1000):
    backend = provider.backend.ibmq_qasm_simulator
    result = backend.run(transpile(qc, backend), shots=num_shots).result()
    return result.get_counts(qc)


counts = execute(qc)

inp_w = "11001000"
inp_p = "1000"

n = len(inp_w)
m = len(inp_p)

assert n >= m, "n must be greater than m"
assert m >= 1, "m must be greater than 0"
assert 2 ** int(math.log2(n)) == n, "n must be a power of 2"
assert 2 ** int(math.log2(m)) == m, "m must be a power of 2"

num_sbits = math.ceil(math.log2(n - m)) + 1

print(num_sbits)

# Number of s'es will be len(m)
# Number of bits in s'es will be num_sbits

s = QuantumRegister(num_sbits, 's_list')
# s_chunks = list(list_to_chunks(s_list, num_sbits))
w = QuantumRegister(n, 'w')
p = QuantumRegister(m, 'p')
bit_matches = QuantumRegister(m, 'bit_matches')
match = QuantumRegister(1, 'match')

qc = QuantumCircuit(s, w, p, bit_matches, match)
set_inputs(qc, inp_w, inp_p)
initialize_s(qc)

num_repetitions = int(math.sqrt(2 ** (num_sbits)))
print(f"Circuit depth is {num_repetitions}")
for repetition in range(num_repetitions):  # num_repetitions
    for start_pos in range(n - m + 1):
        oracle(qc, start_pos)
        qc.mcx(bit_matches, match)
        oracle(qc, start_pos)
    diffusion(qc)

measurement_s(qc)

counts = execute(qc)
plot_histogram(counts)
print(qc.depth())

qc.draw(output='mpl', scale=0.5)
plt.show()
