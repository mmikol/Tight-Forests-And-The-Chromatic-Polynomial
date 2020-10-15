import sage.all
from sage.combinat.permutation import Arrangements
from datetime import datetime
from itertools import combinations

def path_traversals(G):
    for c in combinations(G.vertices(), 2):
        for p in G.all_paths(*c):
            yield (p, list(reversed(p)))
    return 

def get_candidate_paths(G):
    candidate_paths = set()
    
    for fwd, rvr in path_traversals(G):
        if is_candidate_path(fwd):
            candidate_paths.add(tuple(fwd))
        if is_candidate_path(rvr):
            candidate_paths.add(tuple(rvr))
            
    return candidate_paths

def is_candidate_path(P):
    MIN_LEN = 4

    if (len(P) < MIN_LEN):
        return False

    a, c, b, d = *P[:3], P[len(P) - 1]

    if not (a < b and b < c and d < c):
        return False
    
    if any(v_i < c for v_i in P[MIN_LEN:]):
        return False
            
    return True

def has_QPO(G, show_checks = False):
    candidate_paths = get_candidate_paths(G)

    if show_checks:
        print('--new graph---')
        print(f'candidate paths: {candidate_paths}')
        G.show()

    for cp in candidate_paths:
        a, c = cp[0], cp[1]
        b, d = cp[2], cp[len(cp) - 1]

        if not G.has_edge(a, d) and not (d < b and G.has_edge(c, d)):
            if show_checks:
                print('THIS IS NOT A QPO!')
                print(f'failed path: {cp}\n')
                return False

    return True

def get_labeling_permutation_patterns(order):
    labels = [i + 1 for i in range(order)]
    return list(Arrangements(labels, order))

def QPO_check(G, show_checks = False):
    print('checking this graph: ')
    G.show()

    if has_QPO(G, show_checks):
        print('\nQPO: ')
        G.show()
        return (f'has QPO: {True}')

    return (f'has QPO: {False}')

def find_QPO(G, 
             stop_at_QPO = False, 
             show_checks = False, 
             show_QPOs = False, 
             count_QPOs = False):

    start_time = datetime.now()

    print(f'start time: {start_time}')

    print('checking a graph like this: ')
    G.show()

    permutation_patterns = get_labeling_permutation_patterns(G.order())

    QPO_count = 0
    QPO_found = False

    for perm in permutation_patterns:
        G.relabel(perm)

        if has_QPO(G, show_checks):
            QPO_found = True
            QPO_count += 1

        if (show_QPOs):
            G.show()
            print('--THIS IS A QPO!--\n')

        if stop_at_QPO:
            break

    end_time = datetime.now()

    print(f'end time: {end_time}')
    print(f'total time ran: {end_time - start_time}')

    if (count_QPOs):
        print(f'number of possible QPOs: {QPO_count}')

    return (f'has QPO: {QPO_found}')