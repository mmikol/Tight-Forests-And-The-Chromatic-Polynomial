import sage.all
from sage.combinat.permutation import Arrangements


def generate_path_sequences(vertex_labels, *, min_path_len=None, max_path_len=None):
    for i in range(min_path_len, max_path_len + 1):
        for p in Arrangements(vertex_labels, i):
            yield tuple(p)


def generate_graphs_with_permuted_labels(G):
    for permutation in Arrangements(G.vertices(), G.order()):
        G.relabel(permutation)
        yield G
