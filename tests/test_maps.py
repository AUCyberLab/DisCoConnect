"""Tests for discoconnect.maps: hypergraph <-> metagraph translation."""
from discoconnect.maps import (
    frobenius_hypergraph_to_metagraph,
    metagraph_to_frobenius_hypergraph,
)
from discoconnect.computation import (
    get_dominant_morphisms,
    get_minimal_cut,
    get_all_morphism_compositions,
    get_ordered_morphisms,
)


def test_metagraph_has_box_count_plus_two_edges(paper_diagram):
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    assert len(mg.edges) == len(paper_diagram.boxes) + 2


def test_metagraph_has_pointer_objects(paper_diagram):
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    assert "dom_pointer" in mg.generating_set
    assert "cod_pointer" in mg.generating_set


def test_metagraph_generating_set_contains_all_objects(paper_diagram):
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    for i in range(1, 10):
        assert f"ob{i}" in mg.generating_set


def test_metagraph_pointer_edges_reference_dom_cod(paper_diagram):
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    dom_edges = [e for e in mg.edges if "dom_pointer" in e.invertex]
    cod_edges = [e for e in mg.edges if "cod_pointer" in e.outvertex]
    assert len(dom_edges) == 1
    assert len(cod_edges) == 1
    assert dom_edges[0].outvertex == {"ob1", "ob2", "ob3"}
    assert cod_edges[0].invertex == {"ob9"}


def test_roundtrip_preserves_box_set(paper_diagram):
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    d2 = metagraph_to_frobenius_hypergraph(mg)
    assert {b.name for b in d2.boxes} == {b.name for b in paper_diagram.boxes}


def test_roundtrip_preserves_dom_and_cod(paper_diagram):
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    d2 = metagraph_to_frobenius_hypergraph(mg)
    assert {o.name for o in d2.dom} == {o.name for o in paper_diagram.dom}
    assert {o.name for o in d2.cod} == {o.name for o in paper_diagram.cod}


def test_roundtrip_preserves_box_signatures(paper_diagram, paper_box_info):
    mg = frobenius_hypergraph_to_metagraph(paper_diagram)
    d2 = metagraph_to_frobenius_hypergraph(mg)
    for b in d2.boxes:
        expected_in, expected_out = paper_box_info[b.name]
        assert {o.name for o in b.dom} == expected_in
        assert {o.name for o in b.cod} == expected_out
