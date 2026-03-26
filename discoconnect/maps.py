from discopy import frobenius
from mgtoolkit import library
from discoconnect.util import tensor_list
from discoconnect.util import construct_hypergraph_diagram


def frobenius_hypergraph_to_metagraph(hc: frobenius.Hypergraph):
    """
    Convert from a hypergraph string diagram to a metagraph.

    Input:
        hc (discopy.frobenius.Hypergraph): a hypergraph string diagram.
    
    Returns:
        mg (mgtoolkit.library.Metagraph): a metagraph.
    """
    gen_set = set()
    edges = set()
    for box in hc.boxes:
        src = {o.name for o in box.dom}
        dest = {o.name for o in box.cod}
        gen_set.update(src)
        gen_set.update(dest)
        size1 = len(edges)
        edges.add(library.Edge(src, dest, label=box.name))
        assert len(edges) == size1 + 1

    # Flag domain and codomain objects
    edges.add(library.Edge({'dom_pointer'}, {o.name for o in hc.dom}, label='hg_dom'))
    edges.add(library.Edge({o.name for o in hc.cod}, {'cod_pointer'}, label='hg_cod'))
    gen_set.update({'dom_pointer', 'cod_pointer'})
    mg = library.Metagraph(gen_set)
    mg.add_edges_from(edges)
    return mg

def frobenius_diagram_to_metagraph(hc: frobenius.Diagram):
    """
    Convert a planar string diagram to a metagraph.

    Input:
        hc (discopy.frobenius.Diagram): a planar string diagram.
    
    Returns:
        mg (mgtoolkit.library.Metagraph): a metagraph.
    """
    gen_set = set()
    edges = set()
    for b in hc.boxes:
        if isinstance(b, frobenius.Spider) or isinstance(b, frobenius.Swap) or isinstance(b, frobenius.Cap) or isinstance(b, frobenius.Cup):
            # print(f'Skipped morphism: {b}')
            continue
        else:
            heads, tails = set(), set()
            for o in b.dom.inside:
                tails.add(o.name)
            for o in b.cod.inside:
                heads.add(o.name)
            edges.add(library.Edge(tails, heads, label=b.name))
            gen_set.update(heads)
            gen_set.update(tails)
    mg = library.Metagraph(gen_set)
    mg.add_edges_from(edges)
    return mg

def metagraph_to_frobenius_hypergraph(mg: library.Metagraph) -> frobenius.Hypergraph:
    """
    Convert from a metagraph to a hypergraph string diagram.

    Input:
        mg (mgtoolkit.library.Metagraph): a metagraph.
    
    Returns:
        hc (discopy.frobenius.Hypergraph): a hypergraph string diagram.
    """
    dom, cod = [], []
    objects = {}
    boxes = {}

    for v in mg.generating_set:
        if v == 'dom_pointer' or v == 'cod_pointer': 
            continue
        objects[v] = frobenius.Ty(v)
        

    for e in mg.edges:
        if 'dom_pointer' in e.invertex:
            dom = [objects[o] for o in e.outvertex]
        elif 'cod_pointer' in e.outvertex:
            cod = [objects[o] for o in e.invertex]
        else:
            # Morphism / box
            boxes[e.label] = frobenius.Box(e.label, tensor_list([objects[o] for o in e.invertex]), tensor_list([objects[o] for o in e.outvertex]))
    
    # dom, cod of hypergraph category
    hypergraph_dom = tuple([o.name for o in dom])
    hypergraph_cod = tuple([o.name for o in cod])
    ## wires
    wires = []
    for b in boxes.values():
        # wires
        input = tuple([o.name for o in b.dom])
        output = tuple([o.name for o in b.cod])
        wires.append(tuple([input, output]))

    hg = frobenius.Hypergraph(
        dom=tensor_list(dom),
        cod=tensor_list(cod),
        boxes=tuple(b for b in boxes.values()),
        wires=(hypergraph_dom, tuple(wires), hypergraph_cod),
        spider_types=dict((o.name, o) for o in objects.values()),
    )
    return hg

def visualise_metapath_as_planar_diagram(path: library.Metapath):
    """
    Convert a metapath to a planar diagram, then visualise the composition of boxes included.

    Input:
        path (mgtoolkit.library.Metapath): a metapath.
    
    Returns:
        None.
    """
    objects = set()
    objects.update(path.source)
    objects.update(path.target)
    boxes = {}

    for e in path.edge_list:
        objects.update(e.invertex)
        objects.update(e.outvertex)
        boxes[e.label] = (tuple(e.invertex), tuple(e.outvertex))
    
    diagram = construct_hypergraph_diagram(list(objects), boxes, list(path.source), list(path.target))

    diagram.to_diagram().draw()



