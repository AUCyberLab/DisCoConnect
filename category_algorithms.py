from discopy.frobenius import Spider, Swap
from mgtoolkit.library import Metagraph, Edge
from discopy.frobenius import Ty, Box, Spider, Swap, Id, Diagram
from functools import reduce


class HypergraphCategory:
    def __init__(self, morphisms, objects=set()):
        self.morphisms = morphisms
        self.objects = objects
        self.wires = self.create_wires(objects)
        self.boxes = self.create_boxes(morphisms)

    def create_boxes(self, morphisms):
        """
        Using self.wires, convert morphisms into DisCoPy boxes.
        If there exist input/output objects that are not recorded in self.wires, create wires for them.

        Example:
        - input: {
            'f': (('x', 'y'), ('a')),
            'g': (('x', 'y'), ('b'))
        }
        - output: {
            'f': Box('f', Ty('x'))
            'y': Ty('y'),
            'z': Ty('z')
        }
        """
        boxes = {}
        for name, morphism in morphisms.items():
            for ws in morphism:
                for w in ws:
                    if w not in self.wires: 
                        self.wires[w] = Ty(w)
                        self.objects.add(w)
            boxes[name] = Box(name, reduce(lambda a, b: self.wires[a] @ self.wires[b], morphism[0]), reduce(lambda a, b: self.wires[a] @ self.wires[b], morphism[1]))
        return boxes
    
    def create_wires(self, objects):
        """
        Convert objects (strings) into DisCoPy wires.

        Example:
        - input: {'x', 'y', 'z'}
        - output: {
            'x': Ty('x'),
            'y': Ty('y'),
            'z': Ty('z')
        }
        """
        if objects:
            return dict((name, Ty(name)) for name in objects)
        else:
            return dict()
    
def diagram_to_metagraph(diagram):
    """
    Converting from a string diagram to a metagraph.

    """
    gen_set = set()
    edges = set()
    for b in diagram.boxes:
        if isinstance(b, Spider):
            print(f'Is spider: {b}')
        elif isinstance(b, Swap):
            print(f'Is swap: {b}')
        else:
            heads, tails = set(), set()
            for o in b.dom.inside:
                tails.add(o.name)
            for o in b.cod.inside:
                heads.add(o.name)
            edges.add(Edge(tails, heads, label=b.name))
            gen_set.update(heads)
            gen_set.update(tails)
    MG = Metagraph(gen_set)
    MG.add_edges_from(edges)
    return MG

def show_morphisms(metapath):
    """
    Is it possible to authomate the generation of a string diagram?
    
    """
