import sage.all
import unittest
from qpo import *
import qpo_test_helpers as TestHelpers
from sage.graphs.graph import Graph


class PathTraversalGeneratorTests(unittest.TestCase):
    def test_path_traversal_1(self):
        specimen = Graph()
        traversals = generate_path_traversals(specimen)
        self.assertTrue(not list(traversals))
        return

    def test_path_traversal_2(self):
        specimen = Graph({1: []})
        traversals = generate_path_traversals(specimen)
        self.assertTrue(not list(traversals))
        return

    def test_path_traversal_3(self):
        EXPECTED = {(1, 2), (2, 1)}
        specimen = Graph({1: [2]})
        traversals = set(generate_path_traversals(specimen))
        self.assertTrue(len(list(traversals)) == len({(1, 2), (2, 1)}))
        self.assertTrue(all(p in traversals for p in EXPECTED))
        return

    def test_path_traversal_4(self):
        EXPECTED = {
            (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3),
            (1, 2, 3), (3, 2, 1), (1, 3, 2), (2, 3, 1), (2, 1, 3),
            (3, 1, 2), (1, 3, 4), (4, 3, 1), (2, 3, 4), (4, 3, 2),
            (1, 2, 3, 4), (4, 3, 2, 1), (2, 1, 3, 4), (4, 3, 1, 2)
        }
        specimen = Graph({1: [2, 3], 2: [3], 3: [4]})
        traversals = set(generate_path_traversals(specimen))
        self.assertTrue(len(traversals) == len(EXPECTED))
        self.assertTrue(all(p in traversals for p in EXPECTED))
        return


class CandidatePathCheckerTests(unittest.TestCase):
    def test_is_candidate_path_1(self):
        with self.assertRaises(ValueError):
            is_candidate_path((1, 2, 3, 1))
        return

    def test_is_candidate_path_2(self):
        self.assertFalse(is_candidate_path((1,)))
        self.assertFalse(is_candidate_path((1, 2)))
        self.assertFalse(is_candidate_path((1, 2, 3)))
        return

    def test_is_candidate_path_3(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        for p in TestHelpers.generate_paths(vertex_labels=(1, 2, 3, 4), min_path_len=4, max_path_len=4):
            p = tuple(p)
            self.assertTrue(is_candidate_path(p) ==
                            (p in POSSIBLE_CANDIDATE_PATHS))
        return

    def test_is_candidate_path_4(self):
        POSSIBLE_CANDIDATE_PATHS = {
            (1, 4, 2, 3), (1, 4, 3, 2), (1, 5, 2, 3),
            (1, 5, 2, 4), (1, 5, 3, 2), (1, 5, 3, 4),
            (1, 5, 4, 2), (1, 5, 4, 3), (2, 4, 3, 1),
            (2, 5, 3, 1), (2, 5, 3, 4), (2, 5, 4, 1),
            (2, 5, 4, 3), (3, 5, 4, 1), (3, 5, 4, 2),
            (1, 4, 2, 5, 3), (1, 4, 3, 5, 2), (2, 4, 3, 5, 1)
        }

        for p in TestHelpers.generate_paths((1, 2, 3, 4, 5), min_path_len=4, max_path_len=5):
            self.assertTrue(is_candidate_path(p) ==
                            (p in POSSIBLE_CANDIDATE_PATHS))

        return


"""class CandidatePathGeneratorTests(unittest.TestCase):
    def test_candidate_path_generator_1(self):
        specimen = Graph()
        candidate_paths = generate_candidate_paths(specimen)
        self.assertTrue(not list(candidate_paths))
        return

    def test_candidate_path_generator_2(self):
        specimen = Graph({1: [2]})
        candidate_paths = generate_candidate_paths(specimen)
        self.assertTrue(not list(candidate_paths))
        return

    def test_candidate_path_generator_3(self):
        specimen = Graph({1: [2], 2: [3]})
        candidate_paths = generate_candidate_paths(specimen)
        self.assertTrue(not list(candidate_paths))
        return

    def test_candidate_path_generator_4(self):
        specimen = Graph({1: [2], 2: [3]})
        candidate_paths = generate_candidate_paths(specimen)
        self.assertTrue(not list(candidate_paths))
        return

    def test_candidate_path_generator_5(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        vertices = [i + 1 for i in range(4)]
        for a, b, c, d in Arrangements(vertices, len(vertices)):
            specimen = Graph({a: [b], b: [c], c: [d]})
            candidate_paths = generate_candidate_paths(specimen)
            if list(candidate_paths):
                self.assertTrue(all(p in POSSIBLE_CANDIDATE_PATHS
                                    for p in candidate_paths))
        return

    def test_candidate_path_generator_6(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        vertices = [i + 1 for i in range(4)]
        for a, b, c, d in Arrangements(vertices, len(vertices)):
            specimen = Graph({a: [b, c], b: [c], c: [d]})
            candidate_paths = generate_candidate_paths(specimen)
            if list(candidate_paths):
                self.assertTrue(
                    all(p in POSSIBLE_CANDIDATE_PATHS for p in candidate_paths))
        return

    def test_candidate_path_generator_7(self):
        POSSIBLE_CANDIDATE_PATHS = {(2, 5, 3, 4), (1, 4, 3, 5, 2)}
        specimen = Graph({1: [4], 2: [1], 3: [5], 4: [3], 5: [2]})
        candidate_paths = generate_candidate_paths(specimen)
        print(list(candidate_paths))
        self.assertTrue(
            all(p in candidate_paths for p in POSSIBLE_CANDIDATE_PATHS))
        return
"""

unittest.main(argv=[''], verbosity=2, exit=False)
