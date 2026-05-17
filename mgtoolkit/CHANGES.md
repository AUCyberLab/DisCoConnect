# MGtoolkit changes (vendored fork)

This `mgtoolkit/` package is a fork of the original [MGtoolkit](https://pypi.org/project/mgtoolkit/) (Ranathunga, T., *MGtoolkit: a Python library for metagraph analysis*, 2017). It has been vendored into DisCoConnect with the modifications below; we keep the original GPL/Apache-style attribution intact in source headers.

## Python 2 -> Python 3 migration

The upstream MGtoolkit was written for Python 2. The vendored copy here has been ported to Python 3 (>=3.9). Notable changes:

- `print` statements -> `print()` function calls.
- `dict.iteritems()` / `iterkeys()` / `itervalues()` -> `dict.items()` / `keys()` / `values()`.
- `xrange` -> `range`.
- Implicit relative imports -> explicit absolute imports.
- String / unicode handling collapsed onto `str`.
- Integer division (`/` -> `//`) where the original relied on Py2 truncation.
- Exception syntax (`except E, e:` -> `except E as e:`).
- Replaced `cmp=` / `__cmp__` ordering with `__lt__` / `functools.total_ordering` where needed.
- `set()` / `frozenset()` iteration is non-deterministic across processes under Python 3's hash randomization; algorithms that previously appeared deterministic on Py2 are now order-dependent on `PYTHONHASHSEED`. This affects single-witness routines (`get_dominant_metapath`, `get_minimal_cutset`, `make_ordered_metapath`) which may return any one of several valid representatives. The full-enumeration routine `get_all_metapaths_from` remains canonical (set-equal) across runs.

## New routines added for DisCoConnect

Three methods were added to `mgtoolkit.library.Metagraph` to support the connectivity analyses used by DisCoConnect:

- **`make_ordered_metapath(source, target)`** — constructs an ordered metapath (a linearised composition) from `source` to `target`, or returns `None` if none exists. This is the building block used by `get_ordered_morphisms` in DisCoConnect.

- **`make_edge_dominant(metapath)`** — given an ordered metapath, removes redundant edges to produce a **box-dominant** (edge-dominant) ordered metapath — a minimal set of edges whose removal would disconnect `source` from `target`.

- **`make_input_dominant(metapath)`** — given an ordered metapath, prunes inputs to produce an **input-dominant** metapath — a minimal subset of `source` from which `target` is still reachable through the metapath's edges.

These two reductions are composed inside `get_dominant_metapath(source, target)` (which first calls `make_ordered_metapath`, then `make_edge_dominant`, then `make_input_dominant`) to produce a metapath that is simultaneously edge- and input-dominant, matching the notion of *dominance* used in the DisCoConnect SoftwareX paper.

## Determinism note

Because the upstream algorithms iterate over Python sets, single-witness outputs can vary between Python processes. To get reproducible CI runs, pin `PYTHONHASHSEED` in the environment. The DisCoConnect tests are written to accept any *valid* witness rather than a specific one, so they pass under any seed.
