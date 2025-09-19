# Implementation of my master's thesis

This repository contains the implementation of my master's thesis “Horizontal Fragmentation for Data Outsourcing with Formula-Based Confidentiality Constraints - Using Ontological Reasoning” at the Department of Computer Science at Goethe University Frankfurt am Main.

As part of this thesis, the original approach by Wiese (2010) to horizontal fragmentation with formula-based confidentiality constraints was expanded with the concepts "harmless egds", "warded tgds", "safe taintedness", "relaxed warded chase" and "t-isomorphism" used by Bellomarini et al. The integration of those concepts from the field of ontological reasoning resulted in a new algorithm called harmless SEARCH. 
The developed algorithm combines data security aspects with more efficient fragmentation methods, thus providing a sound basis for further research and practical applications in the field of cloud and database systems.

The developed algorithm combines data security aspects with more efficient fragmentation methods, thus providing a sound basis for further research and practical applications in the field of cloud and database systems.

---

## Installation & Requirements
- Python 3.10 or higher  
- No additional libraries required for the core prototype  
- (Optional) [Owlready2](https://owlready2.readthedocs.io/en/latest/) for integration with external reasoners

Clone this repository:
```
git clone https://github.com/SandipSinghN/Master-s-Thesis-Implementation.git
cd Master-s-Thesis-Implementation
```

## How to Run
The prototype consists of two main modules:
1. ``harmless_search.py``, which contains the core implementation of the HARMLESS SEARCH algorithm
2. ``test_cases.py``, which provides example scenarios and simple test runs

To run the included test cases use the terminal:
```
python test_cases.py
```
