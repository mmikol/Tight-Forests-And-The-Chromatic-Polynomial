import sage.all
from sage.combinat.permutation import Arrangements
from datetime import datetime
from orderedset import OrderedSet

# TODO This needs to really be cleaned up


def candidate_paths(G):
    """Yields all candidate paths in a given graph"""
    def _backtrack(path, current_vertex, path_position):
        neighbors = set(G.neighbors(current_vertex)) - path

        # Bug: seems to continue on to find more vertices, different base case needed?
        if path_position >= 3 and current_vertex < path[1]:
            path.add(current_vertex)
            yield tuple(path)
            return

        if ((path_position == 1 and current_vertex > path[0]) or
            (path_position == 2 and current_vertex > path[0] and current_vertex < path[1]) or
                (path_position >= 3 and current_vertex > path[1])):

            path.add(current_vertex)

            for neighbor in neighbors:
                yield from _backtrack(path, neighbor, path_position + 1)

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


def permuted_graphs(G):
    for vertex_ordering in Arrangements(G.vertices(), G.order()):
        G.relabel(vertex_ordering)
        yield G


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
