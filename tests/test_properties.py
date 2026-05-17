"""Property-based tests over random small diagrams."""
import pytest

from random_category_generator import random_hypergraph_generator
from discoconnect.computation import (
    get_all_morphism_compositions,
    get_minimal_cut,
    get_dominant_morphisms,
)

from conftest import is_valid_composition


SEEDS = list(range(20))


@pytest.mark.parametrize("seed", SEEDS)
def test_random_diagram_invariants(seed):
    """For random diagrams: validity, no duplicates, cut intersects all compositions."""
    d = random_hypergraph_generator(seed, 5)
    comps = get_all_morphism_compositions(d)
    if not comps:
        pytest.skip(f"seed {seed} produced a disconnected diagram")

    # No duplicates among compositions.
    as_sets = [frozenset(c) for c in comps]
    assert len(set(as_sets)) == len(as_sets), f"duplicates in compositions: {comps}"

    # Each box label in each composition refers to a real box.
    box_labels = {b.name for b in d.boxes}
    for c in comps:
        assert set(c).issubset(box_labels), f"unknown labels in composition {c}"

    # Minimal cut intersects every composition.
    cut = set(get_minimal_cut(d))
    assert cut, f"non-empty compositions but empty cut for seed {seed}"
    for c in comps:
        assert cut & set(c), (
            f"seed {seed}: cut {cut} fails to intersect composition {c}"
        )


@pytest.mark.parametrize("seed", SEEDS)
def test_random_dominant_is_valid_when_nonempty(seed):
    d = random_hypergraph_generator(seed, 5)
    dom = get_dominant_morphisms(d)
    if not dom:
        pytest.skip(f"seed {seed} has no dominant metapath")
    # The dominant set may use a strict subset of the source, so we validate
    # against the actual source it covers.
    box_info = {b.name: ({o.name for o in b.dom}, {o.name for o in b.cod})
                for b in d.boxes}
    used_inputs = set().union(*(box_info[b][0] for b in dom))
    full_src = {o.name for o in d.dom}
    eff_src = used_inputs & full_src
    assert is_valid_composition(d, dom, src=eff_src), (
        f"seed {seed}: dominant {dom} not a valid composition from {eff_src}"
    )


@pytest.mark.slow
def test_random_larger_diagram_completes():
    """Sanity-check: a larger random diagram still runs to completion."""
    d = random_hypergraph_generator(42, 10)
    _ = get_all_morphism_compositions(d)
    _ = get_minimal_cut(d)
    _ = get_dominant_morphisms(d)
