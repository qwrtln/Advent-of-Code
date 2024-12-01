import collections

import graphviz
import networkx as nx

puzzle = [line for line in open("inputs/25.txt").read().strip().split("\n")]


# to_break = [("cmg", "bvb"), ("pzl", "hfx"), ("jqt", "nvd")]
# vgk: kcz xqg krn mbq
# nmv: thl tqn sht
# fzb: qtv kqs xjc fxr
to_break = [("fzb", "fxr"), ("vgk", "mbq"), ("nmv", "thl")]

graph = collections.defaultdict(list)
for line in puzzle:
    source, targets = line.split(": ")
    for target in targets.split():
        if (source, target) not in to_break:
            graph[source].append(target)

G = nx.Graph(graph)

disconnected = nx.connected_components(G)
result = 1
for d in disconnected:
    result *= len(d)

print("1:", result)


def plot(puzzle):
    graph = graphviz.Digraph(filename="25", node_attr={"shape": "square"})
    # graph.format = "svg"
    for line in puzzle:
        node_name, nodes = line.split(": ")
        nodes = nodes.split()
        for node in nodes:
            if (node_name, node) not in to_break:
                graph.edge(node_name, node)
            else:
                print(node_name, node)
    print(graph.render(directory="visual").replace("\\", "/"))


# plot(puzzle)
