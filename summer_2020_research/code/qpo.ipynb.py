from sage.graphs.connectivity import connected_components_subgraphs
from datetime import datetime

def get_candidate_paths(G):
    candidate_paths = set([])
    
    def check_and_add(p):
        if (is_candidate_path(p)):
            candidate_paths.add(tuple(p))
        return
    
    for i in range(1, G.order()):
        for j in range(i + 1, G.order() + 1):
            for p in G.all_paths(i, j):
                check_and_add(p)
                p.reverse()
                check_and_add(p)
            
    return candidate_paths

def is_candidate_path(P):
    min_len = 4

    if (len(P) < min_len):
        return False

    a, c = P[0], P[1]
    b, d = P[2], P[len(P) - 1]

    if a < b and b < c and P[len(P) - 1] < c:
        for i in range(min_len, len(P)):
            if (P[i - 1] < c):
                return False

        return True

    return False

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
    return Arrangements(labels, order).list()

def QPO_check(G, show_checks = False):
    print('checking this graph: ')
    G.show()

    if has_QPO(G, show_checks):
        print('\nQPO: ')
        G.show()
        return (f'has QPO: {True}')

    return (f'has QPO: {False}')

def QPO_check_all_labelings(G,
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
