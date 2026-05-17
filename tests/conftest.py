"""Shared pytest fixtures and helpers for DisCoConnect tests."""
from __future__ import annotations

import pytest
from discopy.frobenius import Hypergraph

from discoconnect.util import construct_hypergraph_diagram


PAPER_OBJECTS = [f"ob{i}" for i in range(1, 10)]
PAPER_BOXES = {
    "f1": (("ob1", "ob2"), ("ob4", "ob6")),
    "f2": (("ob1", "ob3"), ("ob4", "ob5")),
    "f3": (("ob4",), ("ob7",)),
    "f4": (("ob5", "ob6"), ("ob8",)),
    "f5": (("ob7",), ("ob9",)),
}
PAPER_DOM = ["ob1", "ob2", "ob3"]
PAPER_COD = ["ob9"]


@pytest.fixture
def paper_diagram():
    """The running example from the SoftwareX paper."""
    return construct_hypergraph_diagram(
        objects=PAPER_OBJECTS,
        boxes=PAPER_BOXES,
        dom_objects=PAPER_DOM,
        cod_objects=PAPER_COD,
    )


@pytest.fixture
def paper_box_info():
    """Mapping name -> (input objects, output objects) for the paper example."""
    return {k: (set(v[0]), set(v[1])) for k, v in PAPER_BOXES.items()}


def boxes_info_from_hypergraph(hc: Hypergraph) -> dict:
    """Extract {box_name: (set(dom_obj_names), set(cod_obj_names))} from a Hypergraph."""
    info = {}
    for b in hc.boxes:
        info[b.name] = (
            {o.name for o in b.dom},
            {o.name for o in b.cod},
        )
    return info


def is_valid_composition(hc: Hypergraph, box_names, src=None, dest=None) -> bool:
    """
    Verify a candidate set of box names forms a valid metapath cover from src to dest.

    A valid composition must:
      - use every named box (each box's input objects are eventually covered);
      - cover the target (every dest object is produced or already in src).
    """
    info = boxes_info_from_hypergraph(hc)
    if src is None:
        src = {o.name for o in hc.dom}
    if dest is None:
        dest = {o.name for o in hc.cod}

    box_names = set(box_names)
    if not box_names.issubset(info.keys()):
        return False

    available = set(src)
    remaining = set(box_names)
    progressed = True
    while progressed:
        progressed = False
        for name in list(remaining):
            b_in, b_out = info[name]
            if b_in.issubset(available):
                available.update(b_out)
                remaining.discard(name)
                progressed = True
    if remaining:
        return False
    return set(dest).issubset(available)
