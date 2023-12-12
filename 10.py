import pathlib

import shapely


puzzle = [l for l in open("inputs/10-last.txt").read().strip().split("\n")]
replacement = {
    "F": "┌",
    "L": "└",
    "7": "┐",
    "J": "┘",
    "-": "─",
    "|": "│",
}
replaced_puzzle = []
for l in puzzle:
    for letter, char in replacement.items():
        l = l.replace(letter, char)
    replaced_puzzle.append(l)

puzzle = replaced_puzzle

horizontal = "." * (len(puzzle[0]) + 2)
puzzle = [f".{l}." for l in puzzle]
puzzle = [horizontal, *puzzle, horizontal]

print("Raw puzzle:")
print("\n".join(puzzle))
print("=======================================")

nei_chars = {
    (0, -1): "└┌─S",
    (0, 1): "┐┘─S",
    (-1, 0): "│┌┐S",
    (1, 0): "│└┘S",
}

legal_neis = {
    "│": [(1, 0), (-1, 0)],
    "─": [(0, 1), (0, -1)],
    "└": [(-1, 0), (0, 1)],
    "┌": [(0, 1), (1, 0)],
    "┐": [(0, -1), (1, 0)],
    "┘": [(0, -1), (-1, 0)],
    "S": nei_chars.keys(),
}


def find_start(puzzle):
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if puzzle[y][x] == "S":
                return y, x


def get_neighbour(puzzle, y, x):
    legal = legal_neis[puzzle[y][x]]
    for y_l, x_l in legal:
        if puzzle[y + y_l][x + x_l] in nei_chars[(y_l, x_l)]:
            yield (y + y_l, x + x_l)


def dfs(puzzle, start_point):
    seen = set()
    stack = [start_point]
    while stack:
        current = stack.pop()
        if current in seen:
            assert False, "repetition is not possible"
        seen.add(current)
        y, x = current
        neis = list(get_neighbour(puzzle, y, x))
        try:
            next_point = next(n for n in neis if n not in seen)
        except StopIteration:
            return seen
        stack.append(next_point)

    assert False, "empty stack is not possible"


def print_position(puzzle, seen, contained, y, x):
    visited = ""
    for j in range(len(puzzle)):
        for i in range(len(puzzle[0])):
            if (j, i) in seen:
                visited += puzzle[j][i]
            elif contained and (j, i) in contained:
                visited += "C"
            else:
                visited += "."
        visited += "\n"
    print(visited[:-1])
    return visited[:-1]


start = find_start(puzzle)


path = dfs(puzzle, start)
print("Just the loop:")
loop = print_position(puzzle, path, None, *start)
print("=======================================")
# print("1:", len(path) // 2)


def get_surrounding_neighbours(puzzle, y, x):
    for i, j in nei_chars.keys():
        y_n = y + i
        x_n = x + j
        if (
            y_n >= 0
            and x_n >= 0
            and y_n < len(puzzle)
            and x_n < len(puzzle[0])
            and puzzle[y_n][x_n] == "."
        ):
            yield y_n, x_n


def dfs_surroundings(puzzle, start_point):
    seen = set()
    stack = [start_point]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        y, x = current
        for n in list(get_surrounding_neighbours(puzzle, y, x)):
            if n not in seen:
                stack.append(n)

    return seen


def print_surroundings(puzzle, surroundings):
    to_print = ""
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if (y, x) in surroundings:
                to_print += "."
            else:
                to_print += " "
        to_print += "\n"
    return to_print[:-1]


surroundings = dfs_surroundings(loop.split("\n"), (0, 0))
# print(surroundings)
print("Surroundings:")
print(print_surroundings(puzzle, surroundings))
print("=======================================")
candidates = []
for y in range(len(puzzle)):
    for x in range(len(puzzle[0])):
        if (y, x) not in path and (y, x) not in surroundings:
            candidates.append((y, x))

print("Candidates:", len(candidates))
print(candidates)
print(print_surroundings(puzzle, candidates))
print("=======================================")

result_2 = 0
print(f"X={len(puzzle[0])}")
print(f"Y={len(puzzle)}")
for y, x in candidates:
    passed_walls_right = 0
    passed_walls_left = 0
    for i in range(x + 1, len(puzzle[0])):
        if (y, i) in path:
            if puzzle[y][i] in "┌┘│└┐":
                passed_walls_right += 1

    for i in range(x - 1, 0, -1):
        if (y, i) in path:
            if puzzle[y][i] in "┌┘│└┐":
                passed_walls_left += 1
    # print(f"{passed_walls=}")
    # input("=======================================")
    if passed_walls_left % 2 == 0 or passed_walls_right % 2 == 0:
        result_2 += 1





print(result_2)
LOW = 345
HIGH = 616
WRONG = [497]
# assert LOW < result_2 <HIGH

# print_position(puzzle, surroundings, None, *(0,0))
# loop = print_position(puzzle, path, None, *start)
# surroundings = dfs_surroundings(loop, (0, 0))
# print(surroundings)
# print_position(puzzle, [], surroundings, *start)
# result_2 = 0
# contained = []
# for y in range(len(puzzle)):
#     for x in range(len(puzzle[0])):
#         if (y, x) not in path:
#             if  ring.contains(shapely.Point(y, x)):
#                 contained.append((y, x))
#                 result_2 += 1
#
# print_position(puzzle, path, contained, *start)
# print(result_2)
# flooded = fill(loop.split("\n"), 0, 0, ".", "O")
# print("\n".join(flooded))
