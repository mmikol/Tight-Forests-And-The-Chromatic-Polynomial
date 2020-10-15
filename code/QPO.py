import sage.all
from itertools import combinations
from sage.combinat.permutation import Arrangements
from datetime import datetime


def generate_path_traversals(G):
    for c in combinations(G.vertices(), 2):
        for p in G.all_paths(*c):
            yield tuple(p)
            yield tuple(reversed(p))
    return


def generate_candidate_paths(G):
    for p in generate_path_traversals(G):
        if is_candidate_path(p):
            yield tuple(p)
    return


def is_candidate_path(P):
    MIN_LEN = 4

    if len(P) < MIN_LEN:
        return False

    a, c, b, d = *P[:3], P[-1]

    if len(P) == MIN_LEN and not (d < c):
        return False

    if not (a < b and b < c):
        return False

    if any(v_i < c for v_i in P[MIN_LEN:len(P)]):
        return False

    if not (d < c):
        return False

    return True


def has_QPO(G, show_checks=False):
    if show_checks:
        print('--new graph--')
        G.show()

    for cp in generate_candidate_paths(G):
        a, c, b, d = *cp[:3], cp[-1]

        if (not G.has_edge(a, d) and not (d < b and G.has_edge(c, d))):
            print('THIS IS NOT A QPO!')
            print(f'failed path: {cp}')
            return False

    return True


def get_label_permutations(order):
    labels = [i + 1 for i in range(order)]
    for a in Arrangements(labels, order):
        yield a
    return


def QPO_check(G, show_checks=False):
    print('checking this labeling: ')
    G.show()

    if has_QPO(G, show_checks):
        print('\nQPO: ')
        G.show()
        return (f'has QPO: {True}')

    return (f'has QPO: {False}')


def find_QPO(G,
             stop_at_QPO=False,
             show_checks=False,
             show_QPOs=False,
             count_QPOs=False):

    start_time = datetime.now()

    print(f'start time: {start_time}')
    print('checking a graph like this: ')
    G.show()

    QPO_count = 0
    QPO_found = False

    for perm in get_label_permutations(G.order()):
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
