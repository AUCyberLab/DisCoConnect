import random
from discopy.frobenius import Ty, Box, Spider, Swap, Id, Diagram
from functools import reduce


def random_diagram_generator(seed, object_size, diagram_dom_size):
    """
    Random hypergraph category diagram generator
    Random morphism generator
    Start from domain, randomly generate layers
    Specify the size of diagram.dom
    Stop when the number of objects reach the intended size.

    """
    random.seed(seed)
    objects = {}
    morphisms = {}
    diagram = None
    # At each iteration, 10 (adjustable) components: randomly decide if make a morphism / spider / swap / wire (new or existing) / terminating a wire
    while True:
        if len(objects) >= object_size:
            break
        domain = [] # The domain of the layer; codomain of the previous layer.
        if not diagram:
            # First layer, generate domain of the diagram: just wires
            dom_size = random.randint(1, diagram_dom_size)
            for _ in range(dom_size):
                obj_name = f'obj_{len(objects) + 1}'
                objects[obj_name] = Ty(obj_name)
                domain.append(objects[obj_name])
            # diagram = reduce(lambda a, b: a @ b, domain)
            # diagram.draw()
            print(f'*** Diagram domain: {domain}')
        else:
            # set domain as domain.cod
            print(diagram)
            # diagram.draw()
            domain = diagram.cod
        # Randomly generate: morphism / spider / swap / wire (new / existing); or terminating a wire.    
        # !!! Toss a coin: morphism / spider / swap / wire (new / existing) / termianting a wire.
        print(f'Domain: {domain}')
        left = 0
        layer_composition = []
        while left <= len(domain) - 1:
            # right = random.randint(left, len(domain) - 1) # TODO: fix this
            dom_size = random.randint(1, 3)
            right = min(len(domain) - 1, left + dom_size - 1)
            # TODO: If right + 1 == left, create a new wire at this layer
            # If left == right (one wire), randomly decide between: morphism / spider
            if left == right:
                dice = random.randint(1, 5)
                if dice == 1 or dice == 2:
                    # spider: 1 -> randomint
                    print(f'Generating spider...')
                    layer_composition.append(Spider(1, 2, domain[left])) # make random outn later.
                elif dice == 3 or dice == 4:
                    # morphism
                    print(f'Generating morphism...')
                    m_name = f'f_{len(morphisms) + 1}'
                    morphisms[m_name] = _generate_morphism(m_name, domain[left:right+1], objects)
                    layer_composition.append(morphisms[m_name])
                else:
                    # terminate wire
                    print(f'Terminating wire...')
                    layer_composition.append(Spider(1, 0, domain[left]))
            elif left + 1 == right:
                # randomly decide if morphism or swap
                if random.randint(1, 2) == 1:
                    # swap
                    print('Swapping...')
                    layer_composition.append(Swap(domain[left], domain[right]))
                else:
                    # morphism
                    m_name = f'f_{len(morphisms) + 1}'
                    morphisms[m_name] = _generate_morphism(m_name, domain[left:right+1], objects)
                    layer_composition.append(morphisms[m_name])
            else:
                # Create morphism
                m_name = f'f_{len(morphisms) + 1}'
                morphisms[m_name] = _generate_morphism(m_name, domain[left:right+1], objects)
                layer_composition.append(morphisms[m_name])
            left = right + 1
        if diagram:
            diagram = diagram >> reduce(lambda a, b: a @ b, layer_composition)
        else:
            diagram = reduce(lambda a, b: a @ b, layer_composition)
    return diagram.simplify(), objects, morphisms

def _generate_morphism(m_name, m_dom, objects):
    # randomly generate codomain for the new morphism
    m_cod = []
    # Randomise the size of cod: [1, 3]
    for _ in range(random.randint(1, 3)): 
        if random.randint(1, 2) == 1: 
            # pick existing wire
            m_cod.append(random.choice(list(objects.values())))
        else:
            # Create a new wire
            obj_name = f'obj_{len(objects) + 1}'
            objects[obj_name] = Ty(obj_name)
            m_cod.append(objects[obj_name])
    assert len(m_dom) <= 3
    return Box(m_name, reduce(lambda a, b: a @ b, m_dom), reduce(lambda a, b: a @ b, m_cod))
