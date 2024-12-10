import queue

puzzle = [list(line) for line in open("inputs/10.txt").read().strip().split("\n")]


WIDTH = len(puzzle[0])
HEIGHT = len(puzzle)


# for line in puzzle:
#     print("".join(line))


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
            and puzzle[y + dy][x + dx] != "."
            and (int(puzzle[y + dy][x + dx]) - int(puzzle[y][x])) == 1
        ):
            yield y + dy, x + dx


def find_path(point, puzzle, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()
    path.append(point)
    visited.add(point)
    y, x = point
    if puzzle[y][x] == "9":
        yield path
    for neighbour in get_passable_neighbours((y, x)):
        if neighbour not in visited:
            yield from find_path(neighbour, puzzle, path, visited)


def calculate_trailhead_scores(puzzle):
    result = 0
    for s in find_starting_points(puzzle):
        result += len(list(find_path(s, puzzle)))
    return result


print("1:", calculate_trailhead_scores(puzzle))
