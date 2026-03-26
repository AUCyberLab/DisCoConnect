from discoconnect.util import construct_hypergraph_diagram


def example_diagram1():
    types = [f'ob{i}' for i in range(1, 10)]
    boxes = {
        'f1': (('ob1', 'ob2'), ('ob4', 'ob6')),
        'f2': (('ob1', 'ob3'), ('ob4', 'ob5')),
        'f3': (('ob4',), ('ob7',)),
        'f4': (('ob5', 'ob6'), ('ob8',)),
        'f5': (('ob7',), ('ob9',)),
    }   
    diagram = construct_hypergraph_diagram(objects=types, boxes=boxes, dom_objects=['ob1', 'ob2', 'ob3'], cod_objects=['ob9'])

    return diagram
