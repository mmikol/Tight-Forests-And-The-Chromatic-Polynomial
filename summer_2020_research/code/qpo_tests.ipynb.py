import qpo
import sage.graphs

# qpos
G = graphs.CycleGraph(4)
G = graphs.CycleGraph(3)
G = graphs.RandomTree(20)
G = graphs.CompleteGraph(5)

#not qpos
G = graphs.CompleteBipartiteGraph(2, 3)
G = graphs.CycleGraph(5)
G = graphs.CompleteBipartiteGraph(4, 4)