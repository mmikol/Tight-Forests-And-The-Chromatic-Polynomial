import unittest
import sage.all
from sage.graphs.graph import Graph
from sage.combinat.permutation import Arrangements
from qpo import *


class PathTraversalGeneratorTests(unittest.TestCase):
    def test_path_traversal_1(self):
        traversals = generate_path_traversals(Graph())
        self.assertTrue(not list(traversals))

    def test_path_traversal_2(self):
        traversals = generate_path_traversals(Graph({1: []}))
        self.assertTrue(not list(traversals))

    def test_path_traversal_3(self):
        EXPECTED = {(1, 2), (2, 1), }
        traversals = set(generate_path_traversals(Graph({1: [2]})))
        self.assertTrue(len(list(traversals)) == len({(1, 2), (2, 1)}))
        self.assertTrue(all(p in traversals for p in EXPECTED))

    def test_path_traversal_4(self):
        EXPECTED = {(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3),
                    (1, 2, 3), (3, 2, 1), (1, 3, 2), (2, 3, 1), (2, 1, 3),
                    (3, 1, 2), (1, 3, 4), (4, 3, 1), (2, 3, 4), (4, 3, 2),
                    (1, 2, 3, 4), (4, 3, 2, 1), (2, 1, 3, 4), (4, 3, 1, 2), }
        traversals = set(generate_path_traversals(
            Graph({1: [2, 3], 2: [3], 3: [4]})))
        self.assertTrue(len(traversals) == len(EXPECTED))
        self.assertTrue(all(p in traversals for p in EXPECTED))


class CandidatePathGeneratorTests(unittest.TestCase):
    def test_candidate_path_generator_1(self):
        c_paths = generate_candidate_paths(Graph())
        self.assertTrue(not list(c_paths))

    def test_candidate_path_generator_2(self):
        c_paths = generate_candidate_paths(Graph({1: [2]}))
        self.assertTrue(not list(c_paths))

    def test_candidate_path_generator_3(self):
        c_paths = generate_candidate_paths(Graph({1: [2], 2: [3]}))
        self.assertTrue(not list(c_paths))

    def test_candidate_path_generator_4(self):
        POSSIBLE_CANDIDATE_PATHS = [1, 4, 3, 2], [2, 4, 3, 1]
        vertices = [i + 1 for i in range(4)]
        paths = [a for a in Arrangements(vertices, len(vertices))
                 if a not in POSSIBLE_CANDIDATE_PATHS]

        print(paths)
        print(len(paths))
        for [a, b, c, d] in paths:
            c_paths = generate_candidate_paths(Graph({a: [b], b: [c], c: [d]}))


        # CompleteGraph(15)
unittest.main(argv=[''], verbosity=2, exit=False)