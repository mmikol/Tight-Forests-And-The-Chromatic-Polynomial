from sage.all import *
from sage.combinat.permutation import Arrangements
from datetime import datetime
from ordered_set import OrderedSet


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

    def search(path, current_vertex, path_position):
        neighbors = set(G.neighbors(current_vertex)) - path

        if last_possible_vertex(path, path_position, current_vertex):
            yield tuple([*path, current_vertex])

        if still_candidate_path(path, current_vertex, path_position):
            path.add(current_vertex)
            for neighbor in neighbors:
                yield from search(path, neighbor, path_position + 1)
            path.remove(current_vertex)

    # Property: Two largest vertices never begin a candidate path
    for vertex in G.vertices()[: G.order() - 1]:
        # Property: Three smallest vertices never follow the first vertex in a candidate path
        neighbors = filter(lambda v: G.order() > 3 and v > G.vertices()[2],
                           G.neighbors(vertex))
        for neighbor in neighbors:
            yield from search(path=OrderedSet([vertex]), current_vertex=neighbor, path_position=1)


def labeled_graph_permutations(G):
    """
    Yields graphs with labels permuted according to a 
    lexicographically ordered set of permutation patterns.
    """
    for vertex_ordering in Arrangements(G.vertices(), G.order()):
        G.relabel(vertex_ordering)
        yield G


def is_qpo(G):
    """
    Returns whether all candidate paths a-c-b-v_i-v_m=d
    satisfy the condition that either a-d is an edge
    or else d < b and c-d is an edge.
    """
    for candidate_path in candidate_paths(G):
        a, c, b, d = *candidate_path[:3], candidate_path[-1]
        if (not G.has_edge(a, d) and not (d < b and G.has_edge(c, d))):
            return False, candidate_path

    return True, ()


# def qpo_check(G, show_checks=False):
#     print('checking this labeling: ')
#     G.show()

#     if is_QPO(G, show_checks)[0]:
#         print('\nQPO: ')
#         G.show()
#         return (f'has QPO: {True}')

#     return (f'has QPO: {False}')


# def find_qpo(G, show_checks=False, stop_at_QPO=False, stop_at_non_QPO=False):
#     start_time = datetime.now()

#     if show_checks:
#         print(f'start time: {start_time}')
#         print('General Structure:')
#         G.show()

#     QPO_count, QPO_found = (0, False)
#     for graph in labeled_graph_permutations(G):
#         if is_QPO(graph)[0]:
#             QPO_found = True

#             if show_checks:
#                 graph.show()
#                 print(f'is QPO: {QPO_found}')

#             if stop_at_QPO or stop_at_non_QPO:
#                 break

#             QPO_count += 1

#     # if (not stop_at_QPO and not stop_at_non_QPO):
#     #     print(
#     #         f'{QPO_count} possible labelings are QPOs\n')

#     end_time = datetime.now()

#     if show_checks:
#         print(f'end time: {end_time}')
#         print(f'total time ran: {end_time - start_time}\n')
#         print(f'has QPO: {QPO_found}\n')

#     return QPO_found
