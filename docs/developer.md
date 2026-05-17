# Developer Guide

## Repository Structure

```
DisCoConnect/
├── discoconnect/              # Main package
│   ├── __init__.py
│   ├── maps.py                # Hypergraph ↔ metagraph conversion
│   ├── computation.py         # Connectivity analysis (4 main routines)
│   └── util.py                # Hypergraph construction helper
├── mgtoolkit/                 # Vendored metagraph library (Python 3 fork)
│   ├── __init__.py
│   ├── library.py             # Core Metagraph and Metapath classes
│   ├── enums.py
│   ├── exception.py
│   ├── properties.py
│   └── CHANGES.md             # Migration notes from Python 2 → 3
├── tests/                     # Test suite
│   ├── conftest.py            # Fixtures (paper_diagram, is_valid_composition)
│   ├── test_maps.py           # Roundtrip translation tests
│   ├── test_computation.py    # Paper example + invariant tests
│   ├── test_edge_cases.py     # Single-box, disconnected, parallel paths
│   └── test_properties.py     # Property-based tests on random diagrams
├── docs/                      # Documentation
│   ├── index.md               # Homepage with quick-start example
│   ├── developer.md           # This file
│   └── api/                   # Auto-generated API documentation (pdoc)
├── main.py                    # Complete walkthrough of the paper example
├── example.py                 # Paper example diagram fixture
├── requirements.txt           # Pinned runtime deps
├── requirements-dev.txt       # Pinned dev/test deps
├── pyproject.toml             # Package metadata and build config
├── pytest.ini                 # Test configuration
└── README.md
```

## Running Tests

**Install dev dependencies:**
```bash
pip install -r requirements-dev.txt
```

**Run the default test suite** (skips slow tests):
```bash
pytest tests/
```

**Run with verbose output:**
```bash
pytest tests/ -v
```

**Run a specific test file:**
```bash
pytest tests/test_computation.py
```

**Run a specific test:**
```bash
pytest tests/test_computation.py::test_paper_dominant_morphisms
```

**Run only slow tests** (marked with `@pytest.mark.slow`):
```bash
pytest tests/ -m slow
```

**Run everything, including slow:**
```bash
pytest tests/ -m ""
```

## Determinism and PYTHONHASHSEED

The `mgtoolkit` library's single-witness routines (`get_dominant_metapath`, `get_minimal_cutset`, `make_ordered_metapath`) iterate over Python sets. Because Python 3 randomizes hash order across process invocations (controlled by `PYTHONHASHSEED`), these routines may return *different but equally-valid* witnesses on different runs.

For example, in the paper's running example, both `{f1, f3, f5}` and `{f2, f3, f5}` are valid dominant morphisms; which one is returned depends on the hash seed.

**To get reproducible results across runs:**
```bash
PYTHONHASHSEED=0 pytest tests/
```

**The tests handle this:** They accept any valid witness rather than a specific one, so they pass under any seed. The full-enumeration routine `get_all_morphism_compositions` is canonical (set-equal across runs) and is tested for exact matches.

See [`mgtoolkit/CHANGES.md`](../mgtoolkit/CHANGES.md) for details on the Python 2 → 3 migration and its implications.

## Regenerating API Docs

API docs are auto-generated from docstrings using [pdoc](https://pdoc.dev/). To regenerate:

```bash
PDOC_ALLOW_EXEC=1 pdoc discoconnect mgtoolkit -o docs/api
```

(The `PDOC_ALLOW_EXEC=1` environment variable is needed because `discopy` imports matplotlib, which shells out to `gs --version` at import time.)

The docs are published to GitHub Pages via `.github/workflows/ci.yml` on every push to `main`.

## Contributing

1. Write or modify code in `discoconnect/`.
2. Add or update tests in `tests/` (use `conftest.py` fixtures for common patterns).
3. Run `pytest tests/` locally to verify.
4. Docstrings are extracted into the API docs, so keep them concise and accurate.
5. See `mgtoolkit/CHANGES.md` before modifying anything in `mgtoolkit/`.
