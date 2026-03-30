# DisCoConnect

**DisCoConnect** is a Python toolkit for computing syntactic connectivity properties of hypergraph category string diagrams. It extends the [DisCoPy](https://github.com/discopy/) by providing algorithmic support for analysing how morphisms compose in hypergraph categories at the diagrammatic level.

DisCoConnect maps hypergraph string diagrams to *metagraph* representations, enabling the reuse of established metagraph connectivity algorithms to reason about composition, dominance, and cut structures in categorical diagrams.

---

## Features

DisCoConnect provides algorithms to:

- Identify compositions of morphisms witnessing a given input–output relationship
- Enumerate all distinct morphism compositions between a specified domain and codomain
- Compute **dominant** sets of objects and morphisms required to preserve connectivity
- Identify **minimal cuts** (critical morphisms) whose removal breaks diagrammatic connectivity

The package is lightweight, modular, and interoperable with DisCoPy’s `frobenius.Hypergraph` representation.

---

## Motivation

Hypergraph categories provide a natural formalism for modelling open, interconnected systems with shared variables and multi‑terminal connections. While DisCoPy supports the construction and evaluation of string diagrams, it currently lacks mechanisms for analysing *syntactic connectivity*—that is, how morphisms compose to establish or block relationships between inputs and outputs.

DisCoConnect addresses this gap by translating hypergraph category string diagrams into metagraphs and applying metagraph connectivity algorithms. This enables systematic analysis of compositional structure, which is particularly useful in domains such as cybersecurity, information‑flow analysis, and the study of compositional attack paths, but is applicable to any setting employing graphical and categorical reasoning.

---

## Installation

DisCoConnect requires **Python 3.9+**.

Clone the repository and install locally:

```bash
git clone https://github.com/AUCyberLab/DisCoConnect.git
cd discoconnect
pip install -r requirements.txt
```

