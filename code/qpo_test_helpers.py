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
