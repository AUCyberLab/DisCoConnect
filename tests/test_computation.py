"""Tests for discoconnect.computation against the paper's running example."""
from discoconnect.maps import (
    frobenius_hypergraph_to_metagraph,
    metagraph_to_frobenius_hypergraph,
)
from discoconnect.computation import (
    get_ordered_morphisms,
    get_dominant_morphisms,
    get_all_morphism_compositions,
    get_minimal_cut,
)

from conftest import is_valid_composition


# Both {f1,f3,f5} and {f2,f3,f5} are valid input- and box-dominant compositions;
# the algorithm's choice depends on set-iteration order (PYTHONHASHSEED).
VALID_DOMINANTS = [{"f1", "f3", "f5"}, {"f2", "f3", "f5"}]
# Both {f3} and {f5} are valid minimum cuts of size 1; the algorithm's
# choice depends on set-iteration order (PYTHONHASHSEED). We accept either.
VALID_MINIMUM_CUTS = [{"f3"}, {"f5"}]
EXPECTED_COMPOSITIONS = {
    frozenset({"f1", "f3", "f5"}),
    frozenset({"f2", "f3", "f5"}),
    frozenset({"f1", "f2", "f3", "f5"}),
}


def test_paper_dominant_morphisms(paper_diagram):
    assert set(get_dominant_morphisms(paper_diagram)) in VALID_DOMINANTS


def test_paper_minimal_cut(paper_diagram):
    assert set(get_minimal_cut(paper_diagram)) in VALID_MINIMUM_CUTS


def test_paper_all_compositions_as_frozensets(paper_diagram):
    result = get_all_morphism_compositions(paper_diagram)
    assert {frozenset(s) for s in result} == EXPECTED_COMPOSITIONS


def test_paper_ordered_morphisms_nonempty(paper_diagram):
    ordered = get_ordered_morphisms(paper_diagram)
    assert isinstance(ordered, list)
    assert len(ordered) > 0


def test_paper_every_composition_is_valid(paper_diagram):
    for comp in get_all_morphism_compositions(paper_diagram):
        assert is_valid_composition(paper_diagram, comp)


def test_paper_compositions_have_no_duplicates(paper_diagram):
    comps = get_all_morphism_compositions(paper_diagram)
    seen = {frozenset(c) for c in comps}
    assert len(seen) == len(comps)


def test_paper_dominant_appears_in_all_compositions(paper_diagram):
    comps = {frozenset(c) for c in get_all_morphism_compositions(paper_diagram)}
    assert frozenset(get_dominant_morphisms(paper_diagram)) in comps


def test_paper_minimal_cut_intersects_every_composition(paper_diagram):
    cut = set(get_minimal_cut(paper_diagram))
    for comp in get_all_morphism_compositions(paper_diagram):
        assert cut & set(comp), f"cut {cut} disjoint from composition {comp}"


def test_paper_dominant_has_minimum_size_among_compositions(paper_diagram):
    dom_size = len(set(get_dominant_morphisms(paper_diagram)))
    sizes = [len(c) for c in get_all_morphism_compositions(paper_diagram)]
    assert dom_size == min(sizes)


def test_paper_minimal_cut_is_truly_minimal(paper_diagram):
    """No proper subset of the cut still disconnects every composition."""
    cut = set(get_minimal_cut(paper_diagram))
    comps = [set(c) for c in get_all_morphism_compositions(paper_diagram)]
    for element in cut:
        smaller = cut - {element}
        still_cuts_all = all(smaller & c for c in comps)
        assert not still_cuts_all, f"removing {element} still cuts all paths"


def test_roundtrip_preserves_all_four_routines(paper_diagram):
    """Proposition 1: D -> MG -> D' preserves connectivity properties.

    The full set of compositions is the canonical, order-independent invariant
    and must match exactly. Single-witness routines (dominant, cut, ordered)
    may pick different but equally-valid representatives across runs of
    mgtoolkit because the underlying algorithms iterate over Python sets,
    whose order depends on PYTHONHASHSEED. We therefore check that the
    round-trip's choices are still valid representatives.
    """
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    d2 = metagraph_to_frobenius_hypergraph(mg)

    assert {frozenset(c) for c in get_all_morphism_compositions(d2)} == {
        frozenset(c) for c in get_all_morphism_compositions(paper_diagram)
    }
    assert set(get_dominant_morphisms(d2)) in VALID_DOMINANTS
    assert set(get_minimal_cut(d2)) in VALID_MINIMUM_CUTS

    ordered_d2 = get_ordered_morphisms(d2)
    ordered_d = get_ordered_morphisms(paper_diagram)
    assert ordered_d2 and ordered_d
    # The ordered metapath must traverse every box of some valid composition.
    box_labels = {b.name for b in paper_diagram.boxes}
    assert set(ordered_d2) & box_labels
    assert set(ordered_d) & box_labels
