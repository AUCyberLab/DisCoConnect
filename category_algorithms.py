from discopy.frobenius import Spider, Swap
from mgtoolkit.library import Metagraph, Edge
from discopy.frobenius import Ty, Box, Spider, Swap, Id, Diagram, Cap, Cup
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
            boxes[name] = Box(name, tensor_list([self.wires[obj] for obj in morphism[0]]), tensor_list([self.wires[obj] for obj in morphism[1]]))
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
        if isinstance(b, Spider) or isinstance(b, Swap) or isinstance(b, Cap) or isinstance(b, Cup):
            print(f'Skipped morphism: {b}')
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

def tensor_list(components):
    return reduce(lambda a, b: a @ b, components)

def extract_morphisms_objects(metapath):
    """
    Return the morphisms contained in a metapath.

    """
    morphisms = set()
    objects = set()
    for e in metapath.edge_list:
        morphisms.add(e.label)
        objects.update(e.invertex)
        objects.update(e.outvertex)
    return morphisms, objects

def metapath_to_diagram(diagram, metapath):
    """
    At each layer of diagram, add all spiders, swapping and objects; only add morphisms that appear in the metapath.

    """
    morphisms, objects = extract_morphisms_objects(metapath)
    sub_diagram = None
    for layer in diagram.__iter__():
        sub_layer = []
        contains_morphisms = False
        for x in layer:
            if isinstance(x, Spider):
                sub_layer.append(x)
                contains_morphisms = True
            elif isinstance(x, Swap):
                sub_layer.append(x)
                contains_morphisms = True
            elif isinstance(x, Box):
                if x.name in morphisms:
                    sub_layer.append(x)
                    contains_morphisms = True
            elif isinstance(x, Ty):
                if x.name in objects:
                    sub_layer.append(x)
        if contains_morphisms:
            composed_layer = tensor_list(sub_layer)
            if not sub_diagram: sub_diagram = composed_layer
            else:
                if sub_diagram.cod == composed_layer.dom:
                    sub_diagram = sub_diagram >> composed_layer
                else:
                    # Create buffer between prev_cod and curr_dom
                    # TODO: fix this: the diagram is broken; same objects are not composed.
                    prev_cod = list(sub_diagram.cod)
                    curr_dom = list(composed_layer.dom)
                    buffer = []
                    i, j = 0, 0
                    while i < len(prev_cod) and j < len(curr_dom):
                        if prev_cod[i].name == curr_dom[j].name:
                            buffer.append(prev_cod[i])
                            i += 1
                            j += 1
                        else:
                            if prev_cod[i].name not in set(curr_dom[temp].name for temp in range(j, len(curr_dom))):
                                # delete prev_cod[i] by making a spider
                                buffer.append(Spider(1, 0, prev_cod[i]))
                                i += 1
                            else:
                                # add curr_dom[j]
                                buffer.append(Spider(0, 1, curr_dom[j]))
                                j += 1
                    while i < len(prev_cod):
                        buffer.append(Spider(1, 0, prev_cod[i]))
                        i += 1
                    while j < len(curr_dom):
                        buffer.append(Spider(0, 1, curr_dom[j]))
                        j += 1
                    sub_diagram = sub_diagram >> tensor_list(buffer)
                    sub_diagram = sub_diagram >> composed_layer
    

    sub_diagram.simplify()
    return sub_diagram