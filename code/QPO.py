from sage.all import *
from sage.combinat.permutation import Arrangements
# from datetime import datetime

def valid_candidate_path(path, v):
    if len(path) == 1:            
        return path[0] < v
    if len(path) == 2:
        return path[0] < v < path[1]
    if len(path) >= 3:
        return path[1] < v
    return False

def candidate_paths(G, v): 
    stack = [[v]]
    while len(stack) > 0:
        path = stack.pop()
        for n in filter(lambda n: n not in path, G.neighbors(path[-1])):
            if len(path) >= 3 and n < path[1]:
                yield (*path , n)
            if valid_candidate_path(path , n):
                stack.append([*path , n])
                
# an iterative solution TODO: test and prove complexity/completeness
def is_QPO(G):
    for v in G.vertices():
        for p in candidate_paths(G, v):
            a, c, b, d = *p[:3], p[-1]
            if (not G.has_edge(a, d) and not (d < b and G.has_edge(c, d))):
                return False, p
    return True, ()

def recursive_candidate_paths(G):
    def valid_candidate_path(path, current_vertex, path_position):
        if path_position == 1:
            return path[0] < current_vertex
        if path_position == 2:
            return path[0] < current_vertex < path[1]
        if path_position >= 3:
            return path[1] < current_vertex
        return False
    
    def search(path, current_vertex, path_position):
        if path_position >= 3 and current_vertex < path[1]:
            yield tuple([*path, current_vertex])
        if valid_candidate_path(list(path), current_vertex, path_position):
            path.append(current_vertex)
            for neighbor in filter(lambda n: n not in path, G.neighbors(current_vertex)):
                yield from search(path, neighbor, path_position + 1)
            path.remove(current_vertex)
            
    # Property: Two largest vertices never begin a candidate path
    for vertex in G.vertices()[:G.order() - 1]:
        # Property: Three smallest vertices never follow the first vertex in a candidate path
        for neighbor in filter(lambda v: G.order() > 3 and v > G.vertices()[2], G.neighbors(vertex)):
            yield from search(path=[vertex], current_vertex=neighbor, path_position=1)

def recursive_is_QPO(G):
    for candidate_path in recursive_candidate_paths(G):
        a, c, b, d = *candidate_path[:3], candidate_path[-1]
        if (not G.has_edge(a, d) and not (d < b and G.has_edge(c, d))):
            return False, candidate_path
    return True, ()
def labeled_graph_permutations(G):
    """
    Yields graphs with labels permuted according to a 
    lexicographically ordered set of permutation patterns.
    """
    for vertex_ordering in Arrangements(G.vertices(), G.order()):
        G.relabel(vertex_ordering)
        yield G



# def qpo_check(G, show_checks=False):
#     print('checking this labeling: ')
#     G.show()

#     if is_QPO(G, show_checks)[0]:
#         print('\nQPO: ')
#         G.show()
#         return (f'has QPO: {True}')

#     return (f'has QPO: {False}')


def find_qpo(G, show_checks=False, stop_at_qpo=False, stop_at_non_qpo=False):
    start_time = datetime.now()

    if show_checks:
        print(f'start time: {start_time}')
        print('General Structure:')
        G.show()

    qpo_count, qpo_found = (0, False)
    for graph in labeled_graph_permutations(G):
        if is_qpo(graph)[0]:
            qpo_found = True

            if show_checks:
                graph.show()
                print(f'is QPO: {qpo_found}')

            if stop_at_qpo:
                break

            qpo_count += 1
            
        if not is_qpo(graph)[0] and stop_at_non_qpo:
            graph.show()
            return is_qpo(graph)

    end_time = datetime.now()

    if show_checks:
        print(f'end time: {end_time}')
        print(f'total time ran: {end_time - start_time}\n')
        print(f'has QPO: {qpo_found}\n')

    return qpo_found
