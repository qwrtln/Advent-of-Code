puzzle = [l for l in open("inputs/10.txt").read().strip().split("\n")]
horizontal = "." * (len(puzzle[0]) + 2)
puzzle = [f".{l}." for l in puzzle]
puzzle = [horizontal, *puzzle, horizontal]

nei_chars = {
    (0, -1): "LF-S",
    (0, 1): "7J-S",
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


def dfs(puzzle, start_point):
    def _get_neighbour(puzzle, y, x):
        for y_l, x_l in legal_neis[puzzle[y][x]]:
            if puzzle[y + y_l][x + x_l] in nei_chars[(y_l, x_l)]:
                yield (y + y_l, x + x_l)

    seen = set()
    stack = [start_point]
    while stack:
        current = stack.pop()
        if current in seen:
            assert False, "repetition is not possible"
        seen.add(current)
        try:
            next_point = next(
                n for n in _get_neighbour(puzzle, *current) if n not in seen
            )
        except StopIteration:
            return seen
        stack.append(next_point)
    assert False, "empty stack is not possible"


path = dfs(puzzle, find_start(puzzle))
print("1:", len(path) // 2)

changing_turns = {
    "F": "J",
    "L": "7",
}
result_2 = 0
# https://en.wikipedia.org/wiki/Scanline_rendering
for y in range(1, len(puzzle) - 1):
    inside = False
    last_corner = None
    if "S" in puzzle[y]:
        puzzle[y] = puzzle[y].replace("S", "L")  # Magic!!!
    for x in range(1, len(puzzle[0]) - 1):
        char = puzzle[y][x]
        if (y, x) not in path and inside:
            result_2 += 1
        elif (y, x) in path:
            if char == "|":
                inside = not inside
            elif char in changing_turns.keys():
                last_corner = char
            elif last_corner and char == changing_turns[last_corner]:
                inside = not inside

print("2:", result_2)
