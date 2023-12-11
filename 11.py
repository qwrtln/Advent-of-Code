import itertools


puzzle = [l for l in open("inputs/11.txt").read().strip().split("\n")]

empty_rows_index = [i for i, row in enumerate(puzzle) if set(row) == {"."}]
empty_cols_index = [
    x for x in range(len(puzzle[0])) if set(l[x] for l in puzzle) == {"."}
]


def solve(puzzle, empty_factor):
    galaxies = set()
    for y, x in [(y, x) for y in range(len(puzzle)) for x in range(len(puzzle[0]))]:
        if puzzle[y][x] == "#":
            galaxies.add((y, x))

    result = 0
    for (y1, x1), (y2, x2) in itertools.combinations(galaxies, 2):
        result += abs(x2 - x1)
        for c in empty_cols_index:
            if c in range(x1, x2, 1 if x1 < x2 else -1):
                result += empty_factor - 1

        result += abs(y2 - y1)
        for r in empty_rows_index:
            if r in range(y1, y2, 1 if y1 < y2 else -1):
                result += empty_factor - 1

    return result


print("1:", solve(puzzle, empty_factor=2))
print("2:", solve(puzzle, empty_factor=10**6))
