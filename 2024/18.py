# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     994.3 ms ±  25.3 ms    [User: 990.6 ms, System: 1.8 ms]
#   Range (min … max):   957.4 ms … 1027.6 ms    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     287.3 ms ±  11.1 ms    [User: 260.3 ms, System: 29.7 ms]
#   Range (min … max):   274.0 ms … 301.6 ms    10 runs
#
import collections
import itertools

puzzle = open("inputs/18.txt").read().strip().split("\n")


CORRUPTED = []

for line in puzzle:
    x_r, y_y = line.split(",")
    x, y = int(x_r), int(y_y)
    CORRUPTED.append((y, x))

WIDTH = max(p[1] for p in CORRUPTED) + 1
HEIGHT = max(p[0] for p in CORRUPTED) + 1


def get_passable_neighbours(point, corrupted):
    y, x = point
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if (
            0 <= y + dy < HEIGHT
            and 0 <= x + dx < WIDTH
            and (y + dy, x + dx) not in corrupted
        ):
            yield y + dy, x + dx


def find_path(start, end, corrupted):
    queue = collections.deque()
    seen = {start}
    queue.append([start])
    while queue:
        path = queue.popleft()
        y, x = path[-1]
        if (y, x) == end:
            return path[1:]
        for neighbour in get_passable_neighbours((y, x), corrupted):
            if neighbour not in seen:
                queue.append(path + [neighbour])
                seen.add(neighbour)
    return []


def find_bypass(path, obstacle, corrupted):
    neighbours = [n for n in get_passable_neighbours(obstacle, corrupted) if n in path]
    bypass = []
    for p1, p2 in itertools.combinations(neighbours, 2):
        if bypass := find_path(p1, p2, corrupted):
            break
    if not bypass:
        return []
    path.extend(bypass)
    return path


def find_blockade(start, end, path, corrupted, position):
    for i in range(position + 1, len(corrupted)):
        current_point = corrupted[i - 1]
        if current_point in path:
            if bypass := find_bypass(path, current_point, corrupted[:i]):
                path = bypass
            else:
                path = find_path(start, end, corrupted[:i])
                if not path:
                    y, x = corrupted[i - 1]
                    return f"{x},{y}"


position = 1024
start, end = (0, 0), (HEIGHT - 1, WIDTH - 1)
path = find_path(start, end, CORRUPTED[:position])
print("1:", len(path))
print("2:", find_blockade(start, end, path, CORRUPTED, position))
