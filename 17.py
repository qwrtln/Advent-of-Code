import heapq
import itertools

import networkx as nx

puzzle = [line for line in open("inputs/17-sample.txt").read().strip().split("\n")]

for line in puzzle:
    print(line)


def needs_to_turn(visited):
    y1, x1 = visited[0]
    return all([x == x1 for (_, x) in visited]) or all([y == y1 for (_, y) in visited])


def create_graph(puzzle):
    height = len(puzzle)
    width = len(puzzle[0])
    graph = {}
    for y in range(height):
        for x in range(width):
            graph[(y, x)] = {}
            for (yd, xd) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                xn = x + xd
                yn = y + yd
                if 0 <= xn < width and 0 <= yn < height:
                    graph[(y, x)][(yn, xn)] = int(puzzle[yn][xn])
    return graph

graph = create_graph(puzzle)
# from pprint import pprint
# pprint(graph)
ng = nx.Graph(graph)
print(len(puzzle)*len(puzzle[0]))
print(ng)
# @nx._dispatch(edge_attrs="weight", preserve_node_attrs="heuristic")
def astar_path(G, source, target, heuristic=None, weight="weight"):
    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    if heuristic is None:
        def heuristic(u, v):
            return 0

    push = heapq.heappush
    pop = heapq.heappop
    weight = nx.algorithms.shortest_paths.weighted._weight_function(G, weight)

    G_succ = G._adj  # For speed-up (and works for both directed and undirected graphs)

    # The queue stores priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    # Add a counter to the queue to prevent the underlying heap from
    # attempting to compare the nodes themselves. The hash breaks ties in the
    # priority and is guaranteed unique for all nodes in the graph.
    c = itertools.count()
    queue = [(0, next(c), source, 0, None)]

    # Maps enqueued nodes to distance of discovered paths and the
    # computed heuristics to target. We avoid computing the heuristics
    # more than once and inserting the node into the queue too many times.
    enqueued = {}
    # Maps explored nodes to parent closest to the source.
    explored = {}

    while queue:
        # Pop the smallest item from queue.
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            # Do not override the parent of starting node
            if explored[curnode] is None:
                continue

            # Skip bad paths that were enqueued before finding a better one
            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent

        for neighbor, w in G_succ[curnode].items():
            cost = weight(curnode, neighbor, w)
            if cost is None:
                continue
            ncost = dist + cost
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                # if qcost <= ncost, a less costly path from the
                # neighbor to the source was already determined.
                # Therefore, we won't attempt to push this neighbor
                # to the queue
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")

result = 0
for (y, x) in astar_path(ng, (0, 0), (len(puzzle) -1, len(puzzle[0])-1)):
    result += int(puzzle[y][x])
print(result)

