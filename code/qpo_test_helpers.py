import sage.all
from sage.combinat.permutation import Arrangements
from sage.combinat.combination import Combinations


def generate_paths(vertex_labels, *, min_path_len=None, max_path_len=None):
    for i in range(min_path_len, max_path_len + 1):
        for p in Arrangements(vertex_labels, i):
            yield tuple(p)
    return
