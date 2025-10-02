from example_diagrams import diagram1, diagram2
from category_algorithms import HypergraphCategory, diagram_to_metagraph

def main():
    objects = {'x', 'y', 'z', 'a', 'b'}
    morphisms = {
        'f': (('x', 'y'), ('a')),
        'g': (('x', 'y'), ('b')),
        'l': (('a', 'b'), ('z')),
        'gg': (('z'), ('x', 'y'))
    }
    category = HypergraphCategory(morphisms, objects=objects)
    print(category.objects)
    assert len(category.wires) == len(category.objects)

    d1 = diagram1(category)
    # d1 = diagram2(category, prev_diagram=d1)
    d1 = d1 >> category.boxes['l']
    d1.draw()
    
    # HG = d1.to_hypergraph()
    # d2 = HG.to_diagram()
    # d2.draw()

    MG = diagram_to_metagraph(d1)
    print(MG)
    paths = MG.get_all_metapaths_from({'x', 'y'}, {'z'})
    for path in paths:
        print(path)
        
    path = MG.get_dominant_metapath({'x', 'y'}, {'z'})    
    print(path)

if __name__ == '__main__':
    main()