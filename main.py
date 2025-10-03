from category_algorithms import HypergraphCategory, diagram_to_metagraph
from categories.category1 import Category1
from categories.util import random_diagram_generator
import random
from discopy.frobenius import Ty, Box, Id, Spider


def main():
    # Example diagram 1: a small category.
    # c1 = Category1()
    # d1 = c1.diagram1()
    # d1 = c1.diagram2()
    # d1 = c1.diagram3()
    # d1.draw()
    # MG = diagram_to_metagraph(d1)
    # paths = MG.get_all_metapaths_from({'x', 'y'}, {'z'})
    # for path in paths:
    #     print(path)


    # Example 2: randomly generate diagram (larger category)
    seed = 10
    d, objects, morphisms = random_diagram_generator(seed, object_size=30, diagram_dom_size=3)
    print(f'Diagram domain: {d.dom}')
    print(f'Diagram codomain: {d.cod}')
    MG = diagram_to_metagraph(d)
    sources = {'obj_1', 'obj_2', 'obj_3'}
    targets = {'obj_30'}
    path = MG.get_dominant_metapath(sources, targets)
    print(path)


if __name__ == '__main__':
    main()
