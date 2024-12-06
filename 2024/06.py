import enum

puzzle = [list(line) for line in open("inputs/06.txt").read().strip().split("\n")]

HEIGHT = len(puzzle)
WIDTH = len(puzzle[0])


class Direction(enum.IntEnum):
    UP = 0
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()


def find_start(puzzle):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if puzzle[y][x] == "^":
                return y, x


def move_in_direction(y, x, direction):
    match direction:
        case Direction.UP:
            y -= 1
        case Direction.RIGHT:
            x += 1
        case Direction.DOWN:
            y += 1
        case Direction.LEFT:
            x -= 1
    return y, x


def is_looped(y, x, puzzle):
    visited = set()
    direction = Direction.UP

    while True:
        state = (y, x, direction)
        if state in visited:
            return True
        visited.add(state)

        y_n, x_n = move_in_direction(y, x, direction)
        if y_n not in range(HEIGHT) or x_n not in range(WIDTH):
            return False

        if puzzle[y_n][x_n] == "#":
            direction = (direction + 1) % 4
        else:
            y, x = y_n, x_n


def find_path(y, x, puzzle):
    visited = set()
    direction = Direction.UP
    while True:
        y_n, x_n = move_in_direction(y, x, direction)
        if y_n not in range(HEIGHT) or x_n not in range(WIDTH):
            return visited
        if puzzle[y_n][x_n] in "^.":
            visited.add((y_n, x_n))
        elif puzzle[y_n][x_n] == "#":
            direction = (direction + 1) % 4
            y_n, x_n = move_in_direction(y, x, direction)
            visited.add((y_n, x_n))
        y, x = y_n, x_n


def count_cycles(y_s, x_s, path, puzzle):
    result = 0
    for y, x in path:
        puzzle[y][x] = "#"
        if is_looped(y_s, x_s, puzzle):
            result += 1
        puzzle[y][x] = "."
    return result


y, x = find_start(puzzle) or (0, 0)
path = find_path(y, x, puzzle)

print("1:", len(path))
print("2:", count_cycles(y, x, path, puzzle))
