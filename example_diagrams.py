from discopy.frobenius import Ty, Box, Spider, Swap, Id, Diagram
from discopy.hypergraph import Hypergraph
from functools import reduce


def diagram1(category):
    """
    dom: x @ y
    cod: a @ b
    morphisms: f, g
    """
    # Spiders
    x_1_2 = Spider(1, 2, category.wires['x'])
    y_1_2 = Spider(1, 2, category.wires['y'])
    spiders = x_1_2 @ y_1_2  # x @ y -> x @ x @ y @ y
    reorder = Id(category.wires['x']) @ Swap(category.wires['x'], category.wires['y']) @ Id(category.wires['y']) # x @ y @ x @ y
    diagram = spiders >> reorder >> (category.boxes['f'] @ category.boxes['g']) 
    return diagram

def diagram2(category, prev_diagram=None):
    """
    dom: a @ b
    cod: x @ y
    morphisms: l, gg
    """
    diagram = category.boxes['l'] >> category.boxes['gg']
    if prev_diagram:
        diagram = prev_diagram >> diagram
    return diagram