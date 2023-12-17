import collections
import enum
import queue

# import itertools
from pprint import pprint


# puzzle = [line for line in open("inputs/17-sample.txt").read().strip().split("\n")]

puzzle = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".split("\n")


HEIGHT = len(puzzle)
WIDTH = len(puzzle[0])


class Direction(enum.Enum):
    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()


def create_graph(puzzle):
    graph = {}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            graph[(y, x)] = {}
            for yd, xd, direction in [
                (-1, 0, Direction.UP),
                (1, 0, Direction.DOWN),
                (0, 1, Direction.RIGHT),
                (0, -1, Direction.LEFT),
            ]:
                xn = x + xd
                yn = y + yd
                if 0 <= xn < WIDTH and 0 <= yn < HEIGHT:
                    graph[(y, x)][(yn, xn)] = (int(puzzle[yn][xn]), direction)
    return graph


graph = create_graph(puzzle)
# pprint(graph)


def dijkstra(graph, start):
    distances = {}
    for d in Direction:
        for c in range(4):
            distances = {**distances, **{(*node, c, d): float("inf") for node in graph}}
        distances[(*start, 0, d)] = 0
    distances[(*start, 0, None)] = 0
    # paths = collections.defaultdict(list)
    # visited = set()

    q = queue.PriorityQueue()
    q.put((0, start, 0, None))

    while not q.empty():
        (distance, current_node, steps, source_direction) = q.get()

        # visited.add(current_node)

        for neighbour, (distance, target_direction) in graph[current_node].items():
            new_steps = 0
            if source_direction == target_direction:
                new_steps += 1
            # old_direction_count = directions[target_direction]
            # new_directions = collections.defaultdict(lambda: 0)
            # new_directions[target_direction] = old_direction_count + 1
            # if neighbour not in visited:
            old_distance = distances[(*neighbour, new_steps, target_direction)]
            new_distance = (
                distances[(*current_node, steps, source_direction)] + distance
            )
            if new_distance < old_distance and new_steps <= 3:
                print(f"{new_distance=}")
                to_put = (new_distance, neighbour, new_steps, target_direction)
                print(f"{to_put=}")
                q.put(to_put)
                distances[(*neighbour, new_steps, target_direction)] = new_distance
    return distances


dij = dijkstra(graph, (0, 0))
target = (HEIGHT - 1, WIDTH - 1)
HIGH = 1035
# print(dij)
print(dij[target])
