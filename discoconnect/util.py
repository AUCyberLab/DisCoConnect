from functools import reduce
from discopy.frobenius import Ty, Box, Hypergraph


def tensor_list(components):
    """
    To tensor a set of objects.

    Input:
        components (list): a list of Ty objects.
    Returns:
        The tensored list of objects.
    """
    assert len(components) > 0
    return reduce(lambda a, b: a @ b, components)

def construct_hypergraph_diagram(objects: list, boxes: dict, dom_objects: list, cod_objects: list):
    types = dict((o, Ty(o)) for o in objects)
    diagram = Hypergraph(
        dom=tensor_list([types[o] for o in dom_objects]),
        cod=tensor_list([types[o] for o in cod_objects]),
        boxes=tuple(Box(name=b, dom=tensor_list([types[o] for o in boxes[b][0]]), cod=tensor_list([types[o] for o in boxes[b][1]])) for b in boxes),
        wires=(tuple(dom_objects), tuple(boxes.values()), tuple(cod_objects)),
        spider_types=dict((o.name, o) for o in types.values()),
    )
    return diagram

