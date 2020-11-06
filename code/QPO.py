from sage.all import *
from sage.combinat.permutation import Arrangements
from datetime import datetime
from orderedset import OrderedSet

def last_possible_vertex(path, path_position, current_vertex):
    # For a-c-b-...-v_i-...-v_m = d, d < c
    return path_position >= 3 and current_vertex < path[1]

def still_candidate_path(path, current_vertex, path_position):
    # For a-c, a < c
    if path_position == 1:
        return current_vertex > path[0]

    # For a-c-b, a < b < c
    if path_position == 2:
        return current_vertex > path[0] and current_vertex < path[1] 
    
    # For a-c-b-...-v_i-..., v_i > c
    if path_position >= 3:
        return current_vertex > path[1]
    
    return False

def candidate_paths(G):
    """Yields all candidate paths in a given graph"""

    def _backtrack(path, current_vertex, path_position):
        neighbors = set(G.neighbors(current_vertex)) - path

        if last_possible_vertex(path, current_vertex, path_position):
            yield tuple([*path, current_vertex])

        if still_candidate_path(path, current_vertex, path_position):
            path.add(current_vertex)
            for neighbor in neighbors:
                yield from _backtrack(path, neighbor, path_position + 1)
            path.remove(current_vertex)

    # Property: Two largest vertices never begin a candidate path
    for vertex in G.vertices()[: G.order() - 1]:
        # Property: Three smallest vertices never follow the first vertex in a candidate path
        for neighbor in filter(
                lambda v: G.order() > 3 and v > G.vertices()[2],
                G.neighbors(vertex)):
            yield from _backtrack(
                path=OrderedSet([vertex]),
                current_vertex=neighbor,
                path_position=1)


def labeled_graph_permutations(G):
    """
    Yields graphs with labels permuted according to a 
    lexicographically ordered set of permutation patterns.
    """
    for vertex_ordering in Arrangements(G.vertices(), G.order()):
        G.relabel(vertex_ordering)
        yield G


def is_QPO(G, show_checks=False):
    """
    Returns whether all candidate paths a-c-b-v_i-v_m=d
    satisfy the condition that either a-d is an edge
    or else d < b and c-d is an edge.
    """

    if show_checks:
        G.show()

    for candidate_path in candidate_paths(G):
        a, c, b, d = *candidate_path[:3], candidate_path[-1]
        if (not G.has_edge(a, d) and not (d < b and G.has_edge(c, d))):
            return False, candidate_path

    return True, None


def QPO_check(G, show_checks=False):
    print('checking this labeling: ')
    G.show()

    if is_QPO(G, show_checks):
        print('\nQPO: ')
        G.show()
        return (f'has QPO: {True}')

    return (f'has QPO: {False}')


def find_QPO(G, stop_at_QPO=False, show_checks=False, show_QPOs=False, count_QPOs=False):
    start_time = datetime.now()

    print(f'start time: {start_time}')
    print('checking a graph like this: ')
    G.show()

    QPO_count = 0
    QPO_found = False

    for graph in labeled_graph_permutations(G):
        if is_QPO(graph, show_checks):
            QPO_found = True
            QPO_count += 1

        if (show_QPOs):
            graph.show()
            print('--THIS IS A QPO!--\n')

        if stop_at_QPO:
            break

    end_time = datetime.now()

    print(f'end time: {end_time}')
    print(f'total time ran: {end_time - start_time}')

    if (count_QPOs):
        print(f'number of possible QPOs: {QPO_count}')

    return (f'has QPO: {QPO_found}')
