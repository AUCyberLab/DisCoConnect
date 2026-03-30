from discopy.frobenius import Hypergraph
from discoconnect.maps import frobenius_hypergraph_to_metagraph

def get_ordered_morphisms(hc: Hypergraph, src: set[str] | None = None, dest: set[str] | None = None):
    """
    Find an ordered composition of boxes connecting src to dest.

    Parameters:
        hc (discopy.frobenius.Hypergraph): the hypergraph sring diagram.
        src (set): a set of object (string). If not specified, the hypergraph string diagram's domain is used.
        dest (set): a set of objects (string). If not specified, the hypergraph string diagram's codomain is used.

    Return: 
        A list of box names. The list is empty is src if not connected to dest.
    """
    if src is None or len(src) == 0: src = set([o.name for o in hc.dom])
    if dest is None or len(dest) == 0: dest = set([o.name for o in hc.cod])
    MG = frobenius_hypergraph_to_metagraph(hc)
    assert len(MG.edges) == len(hc.boxes) + 2

    path = MG.make_ordered_metapath(src, dest)
    if path is not None:
        return [e.label for e in path.edge_list]
    else:
        return []

def get_dominant_morphisms(hc: Hypergraph, src: set[str] | None = None, dest: set[str] | None = None):    
    """
    Find a composition of boxes connecting src to dest that is both input-dominant and box-dominant.
    - Input-dominant: a minimal subset of src that has a composition of boxes connected to dest.
    - Box-dominant: a minimal set of boxes required to connect src to dest.

    Parameters:
        hc (discopy.frobenius.Hypergraph): the hypergraph sring diagram.
        src (set): a set of object (string). If not specified, the hypergraph string diagram's domain is used.
        dest (set): a set of objects (string). If not specified, the hypergraph string diagram's codomain is used.

    Return: 
        A list of box names. The list is empty is src if not connected to dest.
    """
    if src is None or len(src) == 0: src = set([o.name for o in hc.dom])
    if dest is None or len(dest) == 0: dest = set([o.name for o in hc.cod])
    MG = frobenius_hypergraph_to_metagraph(hc)
    assert len(MG.edges) == len(hc.boxes) + 2

    path = MG.get_dominant_metapath(src, dest)

    if path is not None:
        assert MG.is_edge_dominating_ordered_metapath(path)
        assert MG.is_input_dominating_ordered_metapath(path)
        return [e.label for e in path.edge_list]
    else:
        return []

def get_all_morphism_compositions(hc: Hypergraph, src: set[str] | None = None, dest: set[str] | None = None):
    """
    Using get_all_metapaths_from algorithm from MGtoolkit, extract a set of all composition of boxes that coonect from src to dest.

    Parameters:
        hc (discopy.frobenius.Hypergraph): the hypergraph sring diagram.
        src (set): a set of object (string). If not specified, the hypergraph string diagram's domain is used.
        dest (set): a set of objects (string). If not specified, the hypergraph string diagram's codomain is used.

    Return: 
        A list of box names. The list is empty is src if not connected to dest.
    """
    if src is None or len(src) == 0: src = set([o.name for o in hc.dom])
    if dest is None or len(dest) == 0: dest = set([o.name for o in hc.cod])
    MG = frobenius_hypergraph_to_metagraph(hc)
    assert len(MG.edges) == len(hc.boxes) + 2
    paths = MG.get_all_metapaths_from(src, dest)
    res = []
    if paths:
        for p in paths:
            collection = set()
            for e in p.edge_list:
                collection.add(e.label)
            res.append(collection)
    return res

def get_minimal_cut(hc: Hypergraph, src: set[str] | None = None, dest: set[str] | None = None):
    """
    Get a minimal set of boxes removing which src would be disconnected from dest.

    Parameters:
        hc (discopy.frobenius.Hypergraph): the hypergraph sring diagram.
        src (set): a set of object (string). If not specified, the hypergraph string diagram's domain is used.
        dest (set): a set of objects (string). If not specified, the hypergraph string diagram's codomain is used.

    Return: 
        A list of box names. The list is empty if a cut is not found.
    """

    if src is None or len(src) == 0: src = set([o.name for o in hc.dom])
    if dest is None or len(dest) == 0: dest = set([o.name for o in hc.cod])
    MG = frobenius_hypergraph_to_metagraph(hc)
    assert len(MG.edges) == len(hc.boxes) + 2
    c = MG.get_minimal_cutset(src, dest)
    if c is not None:
        return [e.label for e in c]
    else:
        return []
    
