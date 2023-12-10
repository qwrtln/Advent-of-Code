puzzle = [l for l in open("inputs/10.txt").read().strip().split("\n")]
horizontal = "." * (len(puzzle[0]) + 2)
puzzle = [f".{l}." for l in puzzle]
puzzle = [horizontal, *puzzle, horizontal]

print("\n".join(puzzle))
print("=======================================")

nei_chars = {
    (0, -1): "LF-S",
    (0, 1): "-7JS",
    (-1, 0): "|F7S",
    (1, 0): "|LJS",
}

legal_neis = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "F": [(0, 1), (1, 0)],
    "7": [(0, -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
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


def print_position(puzzle, seen, y, x):
    visited = ""
    for j in range(len(puzzle)):
        for i in range(len(puzzle[0])):
            if (j, i) == (y, x):
                visited += "#"
            elif (j, i) in seen:
                visited += puzzle[j][i]
            else:
                visited += "."
        visited += "\n"
    print(visited)
    return visited


start = find_start(puzzle)


# def fill(puzzle, y, x, color_1, color_2):
#     def fill(y, x):
#         print("================================================")
#         print(f"{x=}, {y=}, {width=}, {height=}")
#         print(puzzle[y])
#         input(f"{len(puzzle[y])=}")
#         if 0 <= x < width and 0 <= y < height and puzzle[y][x] == color_1:
#             puzzle[y] = puzzle[y][:x] + color_2 + puzzle[y][x+1:]
#             print(puzzle[y])
#             fill(y - 1, x)
#             fill(y + 1, x)
#             fill(y, x - 1)
#             fill(y, x + 1)
#     width = len(puzzle[0])
#     height = len(puzzle)
#     fill(y, x)
    # return puzzle

path = dfs(puzzle, start)
loop = print_position(puzzle, path, *start)
print("1:", len(path) // 2)

# flooded = fill(loop.split("\n"), 0, 0, ".", "O")
# print("\n".join(flooded))


