# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     408.0 ms ±  20.9 ms    [User: 391.2 ms, System: 15.2 ms]
#   Range (min … max):   388.5 ms … 461.9 ms    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#  Time (mean ± σ):      1.207 s ±  0.049 s    [User: 1.168 s, System: 0.037 s]
#  Range (min … max):    1.158 s …  1.325 s    10 runs
#
import heapq

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
DIRECTIONS = (NORTH, SOUTH, EAST, WEST)

maze = [list(line) for line in open("inputs/16.txt").read().strip().split("\n")]


def get_endpoints(maze):
    start, end = None, None
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == "S":
                start = (y, x)
            elif maze[y][x] == "E":
                end = (y, x)
    return start, end


def passable(point, maze):
    y, x = point
    return 0 <= y < len(maze) and 0 <= x < len(maze[0]) and maze[y][x] != "#"


def dijkstra(maze, start, end):
    distances = {}
    best_seats = set()
    best_cost = 1e9

    q = [(0, [start], EAST)]
    distances[(start, EAST)] = 0

    while q:
        distance, path, old_direction = heapq.heappop(q)
        current = path[-1]

        if distance > best_cost:
            continue

        if current == end:
            if distance < best_cost:
                best_cost = distance
                best_seats = set(path)
            elif distance == best_cost:
                best_seats.update(path)
            continue

        for direction in DIRECTIONS:
            y, x = current
            dy, dx = direction
            y_n, x_n = y + dy, x + dx
            if passable((y_n, x_n), maze):
                new_distance = distance + (1 if direction == old_direction else 1001)
                new_point = ((y_n, x_n), direction)
                old_distance = distances.get(new_point, 1e9)
                if new_distance <= old_distance:
                    if new_distance < old_distance:
                        distances[new_point] = new_distance
                    heapq.heappush(q, (new_distance, path + [(y_n, x_n)], direction))

    return best_cost, len(best_seats)


start, end = get_endpoints(maze)
cost, seats = dijkstra(maze, start, end)
print("1:", cost)
print("2:", seats)
