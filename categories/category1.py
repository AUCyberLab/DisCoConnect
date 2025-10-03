from category_algorithms import HypergraphCategory
from discopy.frobenius import Spider, Swap, Id

class Category1:
    def __init__(self):
        self.category = HypergraphCategory(
            morphisms = {
                'f': (('x', 'y'), ('a')),
                'g': (('x', 'y'), ('b')),
                'l': (('a', 'b'), ('z')),
                'gg': (('z'), ('x', 'y'))
            }
        )
        print(f'* Objects: {self.category.wires}')
        print(f'* Morphisms: {self.category.boxes}')
    
    def diagram1(self):
        """
        dom: x @ y
        cod: a @ b
        composition: f, g
        """
        # Spiders
        x_1_2 = Spider(1, 2, self.category.wires['x'])
        y_1_2 = Spider(1, 2, self.category.wires['y'])
        spiders = x_1_2 @ y_1_2  # x @ y -> x @ x @ y @ y
        reorder = Id(self.category.wires['x']) @ Swap(self.category.wires['x'], self.category.wires['y']) @ Id(self.category.wires['y']) # x @ y @ x @ y
        diagram = spiders >> reorder >> (self.category.boxes['f'] @ self.category.boxes['g']) 
        return diagram

    def diagram2(self):
        """
        dom: a @ b
        cod: x @ y
        composition: diagram1, l, gg
        """
        diagram = self.category.boxes['l'] >> self.category.boxes['gg']
        return self.diagram1() >> diagram
    
    def diagram3(self):
        """
        dom: x @ y
        cod: z
        composition: diagram1 >> l
        """
        return self.diagram1() >> self.category.boxes['l']
