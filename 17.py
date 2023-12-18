import collections
import enum
import queue


puzzle = [line for line in open("inputs/17.txt").read().strip().split("\n")]


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


def dijkstra(graph, start):
    distances = {}
    for d in Direction:
        for c in range(11):
            distances = {**distances, **{(*node, c, d): float("inf") for node in graph}}
        distances[(*start, 0, d)] = 0
    distances[(*start, 0, None)] = 0

    q = set()
    q.add(
        (0, start, 0, None)
    )  # distance, starting point, steps in direction, direction

    while q:
        (distance, current_node, steps, source_direction) = q.pop()

        for neighbour, (distance, target_direction) in graph[current_node].items():
            new_steps = steps + 1 if source_direction == target_direction else 1
            if (
                (source_direction == target_direction and new_steps <= 10)
                or (source_direction != target_direction and steps >= 4)
                or source_direction is None
            ):
                old_distance = distances[(*neighbour, new_steps, target_direction)]
                new_distance = (
                    distances[(*current_node, steps, source_direction)] + distance
                )
                if new_distance < old_distance:
                    to_put = (new_distance, neighbour, new_steps, target_direction)
                    q.add(to_put)
                    distances[(*neighbour, new_steps, target_direction)] = new_distance
    return distances


dij = dijkstra(graph, (0, 0))
target = (HEIGHT - 1, WIDTH - 1)
results = []
for k, v in dij.items():
    y, x, _, _ = k
    if y == HEIGHT - 1 and x == WIDTH - 1 and v != float("inf"):
        results.append(v)
print(min(results))
