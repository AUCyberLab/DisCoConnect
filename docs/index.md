# DisCoConnect

DisCoConnect is a Python toolkit for computing syntactic connectivity properties of hypergraph category string diagrams. It extends DisCoPy by providing algorithmic support for analysing how morphisms compose in hypergraph categories at the diagrammatic level.

## Quick Start

```python
from example import example_diagram1
from discoconnect.computation import (
    get_ordered_morphisms,
    get_dominant_morphisms,
    get_all_morphism_compositions,
    get_minimal_cut,
)

d = example_diagram1()
print("Ordered morphisms:", get_ordered_morphisms(d))
print("Dominant morphisms:", get_dominant_morphisms(d))
print("All compositions:", get_all_morphism_compositions(d))
print("Minimal cut:", get_minimal_cut(d))
```

Expected output:
```
Ordered morphisms: ['f1', 'f3', 'f2', 'f5', 'hg_cod', 'f4']
Dominant morphisms: ['f1', 'f3', 'f5']
All compositions: [{'f2', 'f1', 'f3', 'f5'}, {'f1', 'f3', 'f5'}, {'f2', 'f3', 'f5'}]
Minimal cut: ['f3']
```

For a complete walkthrough, see [`main.py`](../main.py).

## Documentation

- **[API Reference](api/)** — Full module documentation for `discoconnect` and `mgtoolkit`
- **[Developer Guide](developer.md)** — Repository structure, running tests, and the `PYTHONHASHSEED` determinism caveat
- **[MGtoolkit Migration](../mgtoolkit/CHANGES.md)** — Python 2→3 changes and new routines added for DisCoConnect

## Installation

```bash
git clone https://github.com/AUCyberLab/DisCoConnect.git
cd DisCoConnect
pip install -r requirements.txt
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/
```

See the [Developer Guide](developer.md) for more details.
