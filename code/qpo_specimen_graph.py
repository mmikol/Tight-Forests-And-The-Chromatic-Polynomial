import sage.all
from sage.graphs.graph import Graph
from orderedset import OrderedSet


class QPOSpecimenGraph:
    def __init__(self, structure):
        self.G = Graph(structure)

    @property
    def vertices(self):
        return self.G.vertices()

    # Possible heuristics (since ordered, we know that paths can't begin with n largest)

    @property
    def candidate_paths(self):
        """Yields all candidate paths in a given graph"""

        def _is_potential_candidate_path(path, path_position, vertex):
            """
            Checks for a candidate path of the form a - c - b - v_i - ... - v_m = d
            such that a < b < c and d is the only v_i smaller than c
            """
            return (
                (path_position == 1 and vertex > path[0]) or
                (path_position == 2 and vertex > path[0] and vertex < path[1]) or
                (path_position >= 3 and vertex > path[1])
            )

        def _candidate_path_ends(path_position, vertex, *, c):
            """
            Checks for a candidate path of the form a - c - b - v_i - ... - v_m = d
            such that d is the only v_i smaller than c
            """
            return path_position >= 3 and vertex < c

        def _backtrack(path, current_vertex, path_position):
            neighbors = set(self.G.neighbors(current_vertex)) - path

            if _candidate_path_ends(path, path_position, vertex):
                path.add(current_vertex)
                yield tuple(path)

            if _is_potential_candidate_path(path, path_position, current_vertex):
                path.add(current_vertex)

                for neighbor in neighbors:
                    yield from _backtrack(path, neighbor, path_position + 1)

        for vertex in self.G.vertex_iterator():
            for neighbor in self.G.neighbor_iterator(vertex):
                yield from _backtrack(
                    path=OrderedSet([vertex]),
                    current_vertex=neighbor,
                    path_position=1)

    def has_QPO(self, show_checks=False):
        """
        Returns whether all candidate paths a-c-b-v_i-v_m=d
        satisfy the condition that either a-d is an edge
        or else d < b and c-d is an edge.
        """

        if show_checks:
            print('--new graph--')
            self.G.show()

        for candidate_path in self.candidate_paths:
            a, c, b, d = *candidate_path[:3], candidate_path[-1]

            if (not self.G.has_edge(a, d) and not (d < b and self.G.has_edge(c, d))):
                if show_checks:
                    print('THIS IS NOT A QPO!')
                    print(f'failed path: {candidate_path}')
                return False

        return True
