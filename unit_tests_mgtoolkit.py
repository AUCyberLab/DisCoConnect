import unittest
from mgtoolkit.library import Metagraph, ConditionalMetagraph, Edge, MetagraphHelper, Metapath


# noinspection PyAttributeOutsideInit
class RunTests(unittest.TestCase):

    # noinspection PyPep8Naming
    def setUp(self):
        
        import numpy
        t = numpy.version

        self.generating_set1 = {1, 2, 3, 4, 5, 6, 7}
        self.mg1 = Metagraph(self.generating_set1)
        self.mg1.add_edges_from([Edge({1}, {2, 3}), Edge({1, 4}, {5}), Edge({3}, {6, 7})])

        self.variable_set = set(range(1, 8))
        self.propositions_set = {'p1', 'p2'}
        self.cmg1 = ConditionalMetagraph(self.variable_set, self.propositions_set)
        self.cmg1.add_edges_from([Edge({1, 2}, {3, 4}, attributes=['p1']), Edge({2}, {4, 6}, attributes=['p2']),
                                  Edge({3, 4}, {5}, attributes=['p1', 'p2']), Edge({4, 6}, {5, 7}, attributes=['p1'])])

    def test_mg_creation(self):
        self.assertEqual(len(self.mg1.edges), 3)
        self.assertEqual(len(self.mg1.nodes), 6)

    def test_mg_adjacency_matrix(self):
        adj_matrix = self.mg1.adjacency_matrix()
        row_count = adj_matrix.shape[0]
        col_count = adj_matrix.shape[1]
        row1 = adj_matrix[0, :]
        col1 = adj_matrix[:, 0]
        self.assertEqual(row_count, 7)
        self.assertEqual(col_count, 7)
        self.assertEqual(len(row1.tolist()), 7)
        self.assertEqual(len(col1.tolist()), 7)
        self.assertEqual(row1.tolist()[1][0].coinputs, None)
        self.assertEqual(row1.tolist()[1][0].cooutputs, {3})
        self.assertEqual(row1.tolist()[1][0].edges.invertex, {1})
        self.assertEqual(row1.tolist()[1][0].edges.outvertex, {2, 3})

    def test_mg_incidence_matrix(self):
        incidence_m = self.mg1.incidence_matrix()
        row_count = incidence_m.shape[0]
        col_count = incidence_m.shape[1]
        row1 = incidence_m[0, :]
        col1 = incidence_m[:, 0]
        self.assertEqual(row_count, 7)
        self.assertEqual(col_count, 3)
        self.assertEqual(len(row1.tolist()), 3)
        self.assertEqual(len(col1.tolist()), 7)
        self.assertEqual(row1.tolist(), [-1, -1, None])

    def test_make_ordered_metapath(self):
        # Instance from Higher-Order Graph Models in Network Security
        generating_set2 = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        mg2 = Metagraph(generating_set2)
        mg2.add_edges_from([Edge({1, 2, 3}, {4}), Edge({4}, {5, 6}), Edge({5, 7}, {8, 9})])
        source = {4, 7}
        target = {8}
        metapath = mg2.make_ordered_metapath(source, target)
        isOrdered = mg2.is_ordered_metapath(metapath)
        self.assertEqual(isOrdered, True)
        metapath2 = Metapath({1, 2, 3, 7}, {8}, [Edge({4}, {5, 6}), Edge({1, 2, 3}, {4}), Edge({5, 7}, {8, 9})] )
        isOrdered = mg2.is_ordered_metapath(metapath2)
        self.assertEqual(isOrdered, False)
        
    def test_dominating_metapath_1(self):
        generating_set2 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
        mg2 = Metagraph(generating_set2)
        mg2.add_edges_from([Edge({1, 2, 3}, {4}), Edge({4}, {5, 6}), Edge({5, 7}, {8, 9}), 
                            Edge({1, 2 ,3}, {10}), Edge({10}, {7, 5})])
        
        # test is edge dominant 
        metapath = Metapath({4, 7}, {8}, [Edge({4}, {5, 6}), Edge({5, 7}, {8, 9})] )
        is_edge_dominant = mg2.is_edge_dominating_ordered_metapath(metapath)
        self.assertEqual(is_edge_dominant, True)
        is_input_dominant = mg2.is_input_dominating_ordered_metapath(metapath)
        self.assertEqual(is_input_dominant, True)
        
        metapath = mg2.make_ordered_metapath({1, 2, 3, 4}, {8})
        is_edge_dominant = mg2.is_edge_dominating_ordered_metapath(metapath)
        self.assertEqual(is_edge_dominant, False)
        is_input_dominant = mg2.is_input_dominating_ordered_metapath(metapath)
        self.assertEqual(is_input_dominant, False)
        
        #test make dominant
        metapath_fix_edge = mg2.make_edge_dominant(metapath)
        is_edge_dominant = mg2.is_edge_dominating_ordered_metapath(metapath_fix_edge)
        self.assertEqual(is_edge_dominant, True)
        is_input_dominant =mg2.is_input_dominating_ordered_metapath(metapath_fix_edge)
        self.assertEqual(is_input_dominant, False)
        
        #test make input dominant
        metapath_fix_input = mg2.make_input_dominant(metapath)
        is_edge_dominant = mg2.is_edge_dominating_ordered_metapath(metapath_fix_input)
        self.assertEqual(is_edge_dominant, False)
        is_input_dominant =mg2.is_input_dominating_ordered_metapath(metapath_fix_input)
        self.assertEqual(is_input_dominant, True)
        
        dominant_mp = mg2.get_dominant_metapath({1, 2, 3}, {8})
        true_dominant_mp = [Edge({1, 2, 3}, {10}), Edge({10}, {5, 7}), Edge({5, 7}, {8, 9})]
        self.assertEqual(dominant_mp.edge_list, true_dominant_mp)
        
    def test_dominating_metapath_2(self):
        generating_set2 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
        mg2 = Metagraph(generating_set2)
        mg2.add_edges_from([Edge({1, 2, 3}, {4}), Edge({4}, {5, 6}), Edge({5, 7}, {8, 9}), 
                            Edge({1, 2 ,3}, {10}), Edge({10}, {7, 5}), 
                            Edge({11}, {5, 6}), Edge({5, 6}, {8, 9})])
        dominant_mp = mg2.get_dominant_metapath({1, 2, 3, 11}, {8})
        print("dominannt path: ", dominant_mp)
        
if __name__ == '__main__':
    unittest.main()


