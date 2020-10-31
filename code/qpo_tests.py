import sage.all
from sage.graphs.graph import Graph
from sage.combinat.permutation import Arrangements
from qpo import *
import unittest
import qpo_test_helpers as TestHelpers


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
