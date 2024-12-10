# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      28.4 ms ±   2.1 ms    [User: 25.7 ms, System: 2.7 ms]
#   Range (min … max):    25.5 ms …  35.8 ms    98 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):     129.0 ms ±  10.3 ms    [User: 113.1 ms, System: 15.2 ms]
#   Range (min … max):   120.5 ms … 154.1 ms    21 runs
#
import collections

puzzle = [list(line) for line in open("inputs/10.txt").read().strip().split("\n")]


WIDTH = len(puzzle[0])
HEIGHT = len(puzzle)


def find_starting_points(puzzle):
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] == "0":
                yield y, x


def get_passable_neighbours(point):
    y, x = point
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if (
            0 <= y + dy < HEIGHT
            and 0 <= x + dx < WIDTH
            and (int(puzzle[y + dy][x + dx]) - int(puzzle[y][x])) == 1
        ):
            yield y + dy, x + dx


def find_path_score(point, puzzle, visited=None):
    if visited is None:
        visited = set()
    visited.add(point)
    y, x = point
    if puzzle[y][x] == "9":
        yield 1
    for neighbour in get_passable_neighbours((y, x)):
        if neighbour not in visited:
            yield from find_path_score(neighbour, puzzle, visited)


def find_all_paths(start_point, puzzle):
    queue = collections.deque()
    seen = set([start_point])
    queue.append([start_point])
    while queue:
        path = queue.popleft()
        y, x = path[-1]
        if puzzle[y][x] == "9":
            yield 1  # or path[1:] for the actual path
        for neighbour in get_passable_neighbours((y, x)):
            queue.append(path + [neighbour])
            seen.add(neighbour)
    return seen


print("1:", sum(sum(find_path_score(s, puzzle)) for s in find_starting_points(puzzle)))
print("2:", sum(sum(find_all_paths(s, puzzle)) for s in find_starting_points(puzzle)))
