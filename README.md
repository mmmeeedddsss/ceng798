# METU Ceng798 - Quantum Computing Term Project
## Grover's Algorithm for String Matching
### Mert Tunc - 2023 Spring

This repository contains implementation of [String matching problem](https://en.wikipedia.org/wiki/String-searching_algorithm)(Also called string search or string searching) for quantum computers, using [Grover's algorithm](https://learn.qiskit.org/course/ch-algorithms/grovers-algorithm). 
String matching problem is defined as follows:
```
Given a string w and a pattern p, find all the starting positions of p in w
```

The implementation included in this repository is not performant as the ones that can be found in the literature, 
still in my opinion, it is a good starting point for understanding the algorithm and the problem. Implementation presented in here is well documented and easy to understand.

## Dependencies

To run the code, you'll need to install dependencies of the project using
```
pip install -r requirements.txt
```
Project is developed with python 3.9, but it should work with 3.7 and above. 

Also, the implementation depends on IBM's Qiskit backend provider for IBM's `ibmq_qasm_simulator`. Usage requires you to set up IBM Credentials if you want to stick with this simulator, 
or you can change the backend to a local simulator.

See how you could set up the credentials from here: https://qiskit.org/ecosystem/ibm-runtime/getting_started.html

## Usage

Repository contains two files:
- `grovers_string_search.py`: Implementation as a single file, runnable as `python grovers_string_search.py`
- `grovers_string_search.ipynb`: Implementation with explanations as a tutorial, in jupyter notebook form, runnable as `jupyter notebook grovers_string_search.ipynb`

## Contributing

This work is done as a term project, and I'm not a quantum computing expert. If you see any mistakes, or have any suggestions, issue or a pull request are very welcomed. 

## Licence
Work is licensed under [MIT License](LICENSE)
