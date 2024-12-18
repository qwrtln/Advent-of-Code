# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      4.628 s ±  0.314 s    [User: 4.611 s, System: 0.006 s]
#   Range (min … max):    4.392 s …  5.298 s    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     731.3 ms ±  12.0 ms    [User: 702.9 ms, System: 30.4 ms]
#   Range (min … max):   709.1 ms … 750.9 ms    10 runs
#
import collections

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


def find_path(start_point, corrupted):
    queue = collections.deque()
    seen = {start_point}
    queue.append([start_point])
    while queue:
        path = queue.popleft()
        y, x = path[-1]
        if (y, x) == (HEIGHT - 1, WIDTH - 1):
            return path[1:]
        for neighbour in get_passable_neighbours((y, x), corrupted):
            if neighbour not in seen:
                queue.append(path + [neighbour])
                seen.add(neighbour)
    return []


def find_blockade(path, corrupted, position):
    for i in range(position + 1, len(corrupted)):
        current_point = corrupted[i - 1]
        if current_point in path:
            path = find_path((0, 0), corrupted[:i])
            if not path:
                y, x = corrupted[i - 1]
                return f"{x},{y}"


position = 1024
path = find_path((0, 0), CORRUPTED[:position])
print("1:", len(path))
print("2:", find_blockade(path, CORRUPTED, position))
