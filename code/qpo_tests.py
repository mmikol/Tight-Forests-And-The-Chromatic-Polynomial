import sage.all
from sage.graphs.graph import Graph
from sage.combinat.permutation import Arrangements
from qpo import *
import unittest
import qpo_test_helpers as TestHelpers


class CandidatePathGeneratorTests(unittest.TestCase):
    def test_no_duplicates(self):
        def contains_duplicate_path(path_list):
            path_set = set(path_list)
            for path in path_list:
                if path in path_set:
                    return True
                else:
                    path_set.add(path)
            return False

        vertices = [i + 1 for i in range(5)]
        for a, b, c, d, e in Arrangements(vertices, len(vertices)):
            # Randomly created graph
            specimen = Graph({a: [b, c], b: [c], c: [d], e: [a, b, c, d]})
            specimen_candidate_paths = candidate_paths(specimen)
            self.assertFalse(contains_duplicate_path(specimen_candidate_paths))

    def test_empty_graph(self):
        specimen = Graph()
        self.assertTrue(not list(candidate_paths(specimen)))

    def test_single_vertex(self):
        specimen = Graph({1: []})
        self.assertTrue(not list(candidate_paths(specimen)))

    def test_two_vertex_tree(self):
        specimen = Graph({1: [2]})
        self.assertTrue(not list(candidate_paths(specimen)))

    def test_three_vertex_tree(self):
        specimen = Graph({1: [2], 2: [3]})
        self.assertTrue(not list(candidate_paths(specimen)))

    def test_all_four_cycles(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        vertex_labels = (1, 2, 3, 4)
        for a, b, c, d in Arrangements(vertex_labels, len(vertex_labels)):
            specimen = Graph({a: [b], b: [c], c: [d], d: [c]})
            specimen_candidate_paths = set(candidate_paths(specimen))
            # All found paths are candidate paths
            self.assertTrue(
                all(path in POSSIBLE_CANDIDATE_PATHS for path in specimen_candidate_paths))

    def test_three_cycle_with_dangle(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        vertices = [i + 1 for i in range(4)]
        for a, b, c, d in Arrangements(vertices, len(vertices)):
            specimen = Graph({a: [b, c], b: [c], c: [d]})
            specimen_candidate_paths = set(candidate_paths(specimen))
            if specimen_candidate_paths:
                # All found paths are candidate paths
                self.assertTrue(
                    all(path in POSSIBLE_CANDIDATE_PATHS for path in specimen_candidate_paths))

    def test_all_five_cycles(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 5, 2, 3), (1, 5, 3, 2), (1, 5, 3, 4),
                                    (1, 5, 2, 4), (1, 5, 4, 2), (1, 5, 4, 3),
                                    (1, 4, 2, 3), (1, 4, 3, 2), (1, 4, 3, 5, 2),
                                    (1, 4, 2, 5, 3), (2, 5, 3, 4), (2, 5, 3, 1),
                                    (2, 5, 4, 1), (2, 5, 4, 3), (2, 4, 3, 1),
                                    (2, 4, 3, 5, 1), (3, 5, 4, 2), (3, 5, 4, 1)}
        vertices = [i + 1 for i in range(5)]
        for a, b, c, d, e in Arrangements(vertices, len(vertices)):
            specimen = Graph({a: [b, e], b: [c], c: [d], d: [e]})
            specimen_candidate_paths = set(candidate_paths(specimen))
            # All found paths are candidate paths
            self.assertTrue(
                all(path in POSSIBLE_CANDIDATE_PATHS for path in specimen_candidate_paths))

    def test_K23_graph(self):
        POSSIBLE_CANDIDATE_PATHS = {(3, 5, 4, 1), (2, 5, 3, 1), (2, 5, 4, 1)}
        specimen = Graph({1: [2, 3, 4], 5: [2, 3, 4]})
        specimen_candidate_paths = set(candidate_paths(specimen))
        # All found paths are candidate paths
        self.assertTrue(
            all(path in POSSIBLE_CANDIDATE_PATHS for path in specimen_candidate_paths))
        # All candidate paths found
        self.assertTrue(
            all(path in specimen_candidate_paths for path in POSSIBLE_CANDIDATE_PATHS))

    def test_vertex_glued_four_cycles(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 7, 6, 5)}
        specimen = Graph({1: [2, 4, 5, 7], 3: [2, 4], 6: [5, 7]})
        specimen_candidate_paths = set(candidate_paths(specimen))
        # All found paths are candidate paths
        self.assertTrue(
            all(path in POSSIBLE_CANDIDATE_PATHS for path in specimen_candidate_paths))
        # All candidate paths found
        self.assertTrue(
            all(path in specimen_candidate_paths for path in POSSIBLE_CANDIDATE_PATHS))

    def test_edge_glued_four_cycles(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 5, 3, 2), (2, 6, 4, 1)}
        specimen = Graph({1: [2, 4, 5], 2: [3, 6], 3: [5], 4: [6]})
        specimen_candidate_paths = set(candidate_paths(specimen))
        # All found paths are candidate paths
        self.assertTrue(
            all(path in POSSIBLE_CANDIDATE_PATHS for path in specimen_candidate_paths))
        # All candidate paths found
        self.assertTrue(
            all(path in specimen_candidate_paths for path in POSSIBLE_CANDIDATE_PATHS))

    def test_random_complex_graph(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 10, 9, 4), (1, 10, 9, 8), (3, 7, 5, 2),
                                    (3, 7, 5, 6), (3, 7, 5, 11,
                                                   6), (3, 7, 5, 8, 9, 4),
                                    (3, 7, 5, 8, 9, 10, 1), (4, 9, 8, 5)}
        specimen = Graph({1: [4, 10], 5: [2, 7, 8, 11, 6],
                          7: [3], 9: [4, 8, 10], 11: [6]})
        specimen_candidate_paths = set(candidate_paths(specimen))
        # All found paths are candidate paths
        self.assertTrue(
            all(path in POSSIBLE_CANDIDATE_PATHS for path in specimen_candidate_paths))
        # All candidate paths found
        self.assertTrue(
            all(path in specimen_candidate_paths for path in POSSIBLE_CANDIDATE_PATHS))


class QPOCheckerTests(unittest.TestCase):
    def test_empty_graph(self):
        specimen = Graph()
        self.assertTrue(has_QPO(specimen))

    def test_single_vertex_graph(self):
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
