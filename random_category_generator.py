import random
from discopy.frobenius import Ty, Box, Hypergraph
from discoconnect.util import tensor_list


def random_hypergraph_generator(s, box_count):
    """
    Fixing the size of generating set to 20, generate metagraph of varying density (box count).

    Parameters:
        s (int): random seed.
        box_count: the number of boxes to generate.
    
    Returns:
        hypergraph string diagram (discopy.frobenius.Hypergraph)

    """
    random.seed(s)
    object_count = 10
    objects = {}
    for i in range(object_count):
        objects[f'obj_{i+1}'] = Ty(f'obj_{i+1}')
    # Randomly define 20 object sets
    sets = set()
    while True:
        if len(sets) == 20: break
        group = set(random.sample(list(objects.keys()), k=random.randint(1, 3)))
        sets.add(tuple(group))
    
    boxes = {} # name -> Box
    wires = []
    global_dom = []
    global_cod = []
    for i in range(box_count):
        dom, cod = tuple(random.sample(list(sets), k=2))
        box_name = f'box_{len(boxes)+1}'
        boxes[box_name] = Box(box_name, tensor_list([objects[o] for o in dom]), tensor_list([objects[o] for o in cod]))
        wires.append((dom, cod))
        if len(global_dom) == 0: global_dom = dom
        if i == (box_count - 1): global_cod = cod
    hc = Hypergraph(
        dom=tensor_list([objects[o] for o in global_dom]),
        cod=tensor_list([objects[o] for o in global_cod]),
        boxes=tuple(b for b in boxes.values()),
        wires=(tuple(global_dom), tuple(wires), tuple(global_cod)),
        spider_types=dict((o.name, o) for o in objects.values()),
    )
    return hc
