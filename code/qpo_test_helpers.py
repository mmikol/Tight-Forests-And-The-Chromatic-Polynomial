from sage.all import *
from sage.combinat.permutation import Arrangements


def generate_path_sequences(vertex_labels, *, min_path_len=None, max_path_len=None):
    for i in range(min_path_len, max_path_len + 1):
        for p in Arrangements(vertex_labels, i):
            yield tuple(p)


def graph_permutations(G):
    for permutation in Arrangements(G.vertices(), G.order()):
        G.relabel(permutation)
        yield G


def is_candidate_path(P):
    """
    Determines if a path is of the form a - c - b - v_i - v_m = d 
    such that a < b < c and v_m is the only v_i smaller than c.
    """

    if (len(set(P)) != len(P)):
        raise ValueError('path must be a sequence of distinct vertices')

    MIN_LEN = 4

    if len(P) < MIN_LEN:
        return False

    a, c, b, d = *P[:3], P[-1]

    if len(P) == MIN_LEN and not (d < c):
        return False

    if not (a < b and b < c):
        return False

    if not (a < b and b < c and d < c):
        return False

    if len(P) > MIN_LEN and any(v_i < c for v_i in P[MIN_LEN - 1:-1]):
        return False

    return True
