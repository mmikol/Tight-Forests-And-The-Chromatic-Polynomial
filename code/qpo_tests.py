import unittest
import sage.all
from sage.graphs.graph import Graph
from sage.combinat.permutation import Arrangements
from sage.combinat.combination import Combinations
from qpo import *


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
        self.assertFalse(is_candidate_path((1,)))
        self.assertFalse(is_candidate_path((1, 2)))
        self.assertFalse(is_candidate_path((1, 2, 3)))
        return

    def test_is_candidate_path_2(self):
        POSSIBLE_CANDIDATE_PATHS = {(1, 4, 3, 2), (1, 4, 2, 3), (2, 4, 3, 1)}
        vertices = [i + 1 for i in range(4)]
        for cp in Arrangements(vertices, len(vertices)):
            self.assertTrue(is_candidate_path(cp) ==
                            (cp in POSSIBLE_CANDIDATE_PATHS))
        return

    def test_is_candidate_path_3(self):
        POSSIBLE_CANDIDATE_PATHS = {
            (1, 4, 2, 3), (1, 4, 3, 2), (1, 5, 2, 3),
            (1, 5, 2, 4), (1, 5, 3, 2), (1, 5, 3, 4),
            (1, 5, 4, 2), (1, 5, 4, 3), (2, 4, 3, 1),
            (2, 5, 1, 3), (2, 5, 1, 4), (2, 5, 3, 1),
            (2, 5, 3, 4), (2, 5, 4, 1), (2, 5, 4, 3),
            (3, 5, 4, 1), (3, 5, 4, 2), (1, 4, 2, 5, 3),
            (1, 4, 3, 5, 2), (2, 4, 3, 5, 1)
        }
        # find all combinations of n numbers (length 1 - n)
        # get combos and then permute?
        vertices = {tuple(p)
                    for i in range(4, 6)
                    for c in Combinations(range(1, 6), i) if len(c) >= 4
                    for p in Arrangements(c, len(c))}

        for p in vertices:
            print(p)
        # test all permutations of length  5
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
