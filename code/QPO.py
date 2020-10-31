import sage.all
from itertools import combinations
from sage.combinat.permutation import Arrangements
from datetime import datetime
from orderedset import OrderedSet


# TODO: create a better algorithm
def candidate_paths(G):
    """Yields all candidate paths in a given graph"""
    def backtrack(P, paths, current_vertex, path_position):
        neighbors = set(G.neighbors(current_vertex)) - P

        if path_position >= 3 and current_vertex < P[1]:
            P.add(current_vertex)
            paths.add(tuple(P))
            return

        valid_recurse = (
            (path_position == 1 and current_vertex > P[0]) or
            (path_position == 2 and current_vertex > P[0] and current_vertex < P[1]) or
            (path_position >= 3 and current_vertex > P[1])
        )

        if valid_recurse:
            P.add(current_vertex)

            for neighbor in neighbors:
                backtrack(P, paths, neighbor, path_position + 1)

        return

    paths = set()
    # Possible heuristics (since ordered, we know that paths can't begin with n largest)
    for vertex in G.vertices():
        # Possible heuristics (since ordered, we know that second vertex can't be with n smallest)
        for neighbor in G.neighbor_iterator(vertex):
            backtrack(
                P=OrderedSet([vertex]),
                paths=paths,
                current_vertex=neighbor,
                path_position=1)

    return paths


def permuted_graphs(G):
    for vertex_ordering in Arrangements(G.vertices(), G.order()):
        G.relabel(vertex_ordering)
        yield G


def is_candidate_path(P):
    """
    Returns whether a path is of the form a - c - b - v_i - v_m = d
    such that a < b < c and v_m is the only v_i smaller than c.
    """

    if (len(set(P)) != len(P)):
        raise ValueError('path must be a sequence of distinct vertices')

    MIN_LEN = 4

    if len(P) < MIN_LEN:
        return False

    a, c, b, d = *P[:3], P[-1]

    if not (a < b and b < c and d < c):
        return False

    if len(P) > MIN_LEN and any(v_i < c for v_i in P[MIN_LEN - 1:-1]):
        return False

    return True


def has_QPO(G, show_checks=False):
    """
    Returns whether all candidate paths a-c-b-v_i-v_m=d
    satisfy the condition that either a-d is an edge
    or else d < b and c-d is an edge.
    """

    if show_checks:
        print('--new graph--')
        G.show()

    for candidate_path in candidate_paths(G):
        a, c, b, d = *candidate_path[:3], candidate_path[-1]

        if (not G.has_edge(a, d) and not (d < b and G.has_edge(c, d))):
            if show_checks:
                print('THIS IS NOT A QPO!')
                print(f'failed path: {candidate_path}')
            return False

    return True


def QPO_check(G, show_checks=False):
    print('checking this labeling: ')
    G.show()

    if has_QPO(G, show_checks):
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

    for graph in permuted_graphs(G):
        if has_QPO(graph, show_checks):
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
