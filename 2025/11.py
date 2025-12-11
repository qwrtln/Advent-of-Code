import collections
import functools

import graphviz

puzzle = [line for line in open("inputs/11.txt").read().strip().split("\n")]

graph = collections.defaultdict(list)

visual = graphviz.Digraph()
visual.attr(rankdir="LR")

for line in puzzle:
    source, destinations = line.split(":")
    for dest in destinations.strip().split():
        visual.edge(source, dest)
        graph[source].append(dest)

visual.node("svr", style="filled", fillcolor="green", color="black", penwidth="2")
visual.node("fft", style="filled", fillcolor="red", color="black", penwidth="2")
visual.node("dac", style="filled", fillcolor="red", color="black", penwidth="2")
visual.node("out", style="filled", fillcolor="pink", color="black", penwidth="2")
visual.render("graph_output", view=True, format="png")


def dfs(graph, start, end):
    @functools.cache
    def count_paths(node):
        if node == end:
            return 1
        paths = 0
        for neighbour in graph[node]:
            paths += count_paths(neighbour)
        return paths

    return count_paths(start)


print("1:", dfs(graph, "you", "out"))
print(
    "2:", dfs(graph, "svr", "fft") * dfs(graph, "fft", "dac") * dfs(graph, "dac", "out")
)
