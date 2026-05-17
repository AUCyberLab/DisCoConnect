"""Edge-case tests for small or degenerate diagrams."""
from discoconnect.util import construct_hypergraph_diagram
from discoconnect.computation import (
    get_dominant_morphisms,
    get_minimal_cut,
    get_all_morphism_compositions,
    get_ordered_morphisms,
)

from conftest import is_valid_composition


def _build(objects, boxes, dom, cod):
    return construct_hypergraph_diagram(objects, boxes, dom, cod)


def test_single_box_diagram():
    d = _build(["a", "b"], {"f": (("a",), ("b",))}, ["a"], ["b"])
    assert set(get_dominant_morphisms(d)) == {"f"}
    assert set(get_minimal_cut(d)) == {"f"}
    comps = get_all_morphism_compositions(d)
    assert {frozenset(c) for c in comps} == {frozenset({"f"})}


def test_disconnected_codomain_returns_empty():
    """Two disjoint components: a->b and c->d, with src=a but cod=d."""
    d = _build(
        ["a", "b", "c", "d"],
        {"f": (("a",), ("b",)), "g": (("c",), ("d",))},
        ["a"],
        ["d"],
    )
    assert get_dominant_morphisms(d) == []
    assert get_all_morphism_compositions(d) == []
    assert get_minimal_cut(d) == []
    assert get_ordered_morphisms(d) == []


def test_parallel_paths_cut_requires_both_branches():
    """Two disjoint paths a->x->z and a->y->z. The minimal cut must remove
    something from both branches."""
    d = _build(
        ["a", "x", "y", "z"],
        {
            "f1": (("a",), ("x",)),
            "f2": (("a",), ("y",)),
            "g1": (("x",), ("z",)),
            "g2": (("y",), ("z",)),
        },
        ["a"],
        ["z"],
    )
    cut = set(get_minimal_cut(d))
    comps = [set(c) for c in get_all_morphism_compositions(d)]
    assert comps, "expected at least one composition for parallel-paths diagram"
    assert cut, "expected non-empty cut for parallel-paths diagram"
    for c in comps:
        assert cut & c, f"cut {cut} fails to intersect {c}"
    # Both branches must be represented: at least one f-box and one g-box appear
    # in some composition's required-cut surface.
    all_boxes_seen = set().union(*comps)
    assert {"f1", "f2"} & all_boxes_seen and {"g1", "g2"} & all_boxes_seen


def test_branching_via_shared_object():
    """One shared object feeds two boxes producing the codomain pair."""
    d = _build(
        ["a", "x", "y", "z"],
        {
            "f": (("a",), ("x",)),
            "g": (("x",), ("y",)),
            "h": (("x",), ("z",)),
        },
        ["a"],
        ["y", "z"],
    )
    dom = set(get_dominant_morphisms(d))
    assert dom == {"f", "g", "h"}
    for c in get_all_morphism_compositions(d):
        assert is_valid_composition(d, c)


def test_get_ordered_morphisms_with_explicit_src_dest(paper_diagram):
    ordered = get_ordered_morphisms(paper_diagram, src={"ob1", "ob2"}, dest={"ob7"})
    assert isinstance(ordered, list)
    assert len(ordered) > 0
    # The ordered metapath must witness reachability: f1 and f3 jointly
    # take {ob1, ob2} to {ob7}, so both must appear.
    assert {"f1", "f3"}.issubset(set(ordered))


def test_subdomain_query_on_paper_diagram(paper_diagram):
    """Using only ob1, ob2 as src in the paper diagram still reaches ob9 via f1, f3, f5."""
    dom = set(get_dominant_morphisms(paper_diagram, src={"ob1", "ob2"}, dest={"ob9"}))
    assert dom == {"f1", "f3", "f5"}
