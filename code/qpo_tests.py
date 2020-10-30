import sage.all
from sage.graphs.graph import Graph
from sage.combinat.permutation import Arrangements
from qpo import *
import unittest
import qpo_test_helpers as TestHelpers


class PathTraversalGeneratorTests(unittest.TestCase):
    def test_path_traversal_1(self):
        specimen = Graph()
        traversals = paths(specimen)
        self.assertTrue(not list(traversals))
        

    def test_path_traversal_2(self):
        specimen = Graph({1: []})
        traversals = paths(specimen)
        self.assertTrue(not list(traversals))
        

    def test_path_traversal_3(self):
        EXPECTED = {(1, 2), (2, 1)}
        specimen = Graph({1: [2]})
        traversals = set(paths(specimen))
        self.assertTrue(len(list(traversals)) == len({(1, 2), (2, 1)}))
        self.assertTrue(all(sequence in traversals for sequence in EXPECTED))
        

    def test_path_traversal_4(self):
        EXPECTED = {
            (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3),
            (1, 2, 3), (3, 2, 1), (1, 3, 2), (2, 3, 1), (2, 1, 3),
            (3, 1, 2), (1, 3, 4), (4, 3, 1), (2, 3, 4), (4, 3, 2),
            (1, 2, 3, 4), (4, 3, 2, 1), (2, 1, 3, 4), (4, 3, 1, 2)
        }
        specimen = Graph({1: [2, 3], 2: [3], 3: [4]})
        traversals = set(paths(specimen))
        self.assertTrue(len(traversals) == len(EXPECTED))
        self.assertTrue(all(sequence in traversals for sequence in EXPECTED))
        


class CandidatePathCheckerTests(unittest.TestCase):
    def test_is_candidate_path_1(self):
        with self.assertRaises(ValueError):
            is_candidate_path((1, 2, 3, 1))
        

    def test_is_candidate_path_2(self):
        self.assertFalse(is_candidate_path((1,)))
        self.assertFalse(is_candidate_path((1, 2)))
        self.assertFalse(is_candidate_path((1, 2, 3)))
        

    def test_is_candidate_path_3(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        for path in TestHelpers.generate_path_sequences(vertex_labels=(1, 2, 3, 4), min_path_len=4, max_path_len=4):
            path = tuple(path)
            self.assertTrue(is_candidate_path(path) ==
                            (path in POSSIBLE_CANDIDATE_PATHS))
        

    def test_is_candidate_path_4(self):
        POSSIBLE_CANDIDATE_PATHS = {
            (1, 4, 2, 3), (1, 4, 3, 2), (1, 5, 2, 3),
            (1, 5, 2, 4), (1, 5, 3, 2), (1, 5, 3, 4),
            (1, 5, 4, 2), (1, 5, 4, 3), (2, 4, 3, 1),
            (2, 5, 3, 1), (2, 5, 3, 4), (2, 5, 4, 1),
            (2, 5, 4, 3), (3, 5, 4, 1), (3, 5, 4, 2),
            (1, 4, 2, 5, 3), (1, 4, 3, 5, 2), (2, 4, 3, 5, 1)
        }

        for path in TestHelpers.generate_path_sequences((1, 2, 3, 4, 5), min_path_len=4, max_path_len=5):
            self.assertTrue(is_candidate_path(path) ==
                            (path in POSSIBLE_CANDIDATE_PATHS))

        


class CandidatePathGeneratorTests(unittest.TestCase):
    def test_candidate_path_generator_1(self):
        specimen = Graph()
        self.assertTrue(not list(candidate_paths(specimen)))
        

    def test_candidate_path_generator_2(self):
        specimen = Graph({1: [2]})
        self.assertTrue(not list(candidate_paths(specimen)))
        

    def test_candidate_path_generator_3(self):
        specimen = Graph({1: [2], 2: [3]})
        self.assertTrue(not list(candidate_paths(specimen)))
        

    def test_candidate_path_generator_4(self):
        EXPECTED = (1, 4, 2, 3)
        specimen = Graph({1: [4], 2: [3], 3: [1], 4: [2]})
        self.assertTrue(list(candidate_paths(specimen)) == [EXPECTED])
        

    def test_candidate_path_generator_5(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        vertex_labels = (1, 2, 3, 4)
        for a, b, c, d in Arrangements(vertex_labels, len(vertex_labels)):
            specimen = Graph({a: [b], b: [c], c: [d]})
            for path in candidate_paths(specimen):
                self.assertTrue(path in POSSIBLE_CANDIDATE_PATHS)
        

    def test_candidate_path_generator_6(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        vertices = [i + 1 for i in range(4)]
        for a, b, c, d in Arrangements(vertices, len(vertices)):
            specimen = Graph({a: [b, c], b: [c], c: [d]})
            paths = list(candidate_paths(specimen))
            if paths:
                self.assertTrue(
                    all(cp in POSSIBLE_CANDIDATE_PATHS for cp in paths))
        

    def test_candidate_path_generator_7(self):
        POSSIBLE_CANDIDATE_PATHS = {(2, 5, 3, 4), (1, 4, 3, 5, 2)}
        specimen = Graph({1: [4], 2: [1], 3: [5], 4: [3], 5: [2]})
        self.assertTrue(all(path in candidate_paths(specimen)
                            for path in POSSIBLE_CANDIDATE_PATHS))
        


class QPOCheckerTests(unittest.TestCase):
    def test_qpo_checker_1(self):
        specimen = Graph()
        self.assertTrue(has_QPO(specimen))
        

    def test_qpo_checker_2(self):
        specimen = Graph({1: []})
        self.assertTrue(has_QPO(specimen))
        

    def test_qpo_checker_3(self):
        # 3-cycle
        pass

    def test_qpo_checker_4(self):
        # 4-cycle
        pass

    def test_qpo_checker_5(self):
        # 5-cycle
        pass

    def test_qpo_checker_6(self):
        # bipartite
        pass

    def test_qpo_checker_7(self):
        # complete bipartite
        pass

    def test_qpo_checker_8(self):
        # complete
        pass


unittest.main(argv=[''], verbosity=2, exit=False)
