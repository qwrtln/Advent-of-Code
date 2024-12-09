# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      20.3 ms ±   1.5 ms    [User: 18.1 ms, System: 2.1 ms]
#   Range (min … max):    18.4 ms …  27.7 ms    143 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):      60.8 ms ±   5.2 ms    [User: 47.9 ms, System: 12.2 ms]
#   Range (min … max):    55.1 ms …  76.0 ms    51 runs
#
puzzle = [line for line in open("inputs/04.txt").read().strip().split("\n")]

WORD = "XMAS"


def find_horizontal(puzzle):
    result = 0
    for line in puzzle:
        result += line.count(WORD) + line.count(WORD[::-1])
    return result


def find_vertical(puzzle):
    result = 0
    for line in ["".join([row[i] for row in puzzle]) for i in range(len(puzzle[0]))]:
        result += line.count(WORD) + line.count(WORD[::-1])
    return result


def find_diagonal(puzzle):
    result = 0
    # right diagonal
    for y in range(0, len(puzzle) - len(WORD) + 1):
        for x in range(0, len(puzzle[0]) - len(WORD) + 1):
            if (
                puzzle[y][x]
                + puzzle[y + 1][x + 1]
                + puzzle[y + 2][x + 2]
                + puzzle[y + 3][x + 3]
            ) in (WORD, WORD[::-1]):
                result += 1
    # left diagonal
    for y in range(len(puzzle) - 1, len(WORD) - 2, -1):
        for x in range(0, len(puzzle[0]) - len(WORD) + 1):
            if (
                puzzle[y][x]
                + puzzle[y - 1][x + 1]
                + puzzle[y - 2][x + 2]
                + puzzle[y - 3][x + 3]
            ) in (WORD, WORD[::-1]):
                result += 1
    return result


def find_cross(puzzle):
    result = 0
    for y, line in enumerate(puzzle[1 : len(puzzle) - 1], start=1):
        for x, char in enumerate(line[1 : len(line) - 1], start=1):
            if (
                char == "A"
                and f"{puzzle[y + 1][x + 1]}A{puzzle[y - 1][x - 1]}" in ("SAM", "MAS")
                and f"{puzzle[y + 1][x - 1]}A{puzzle[y - 1][x + 1]}" in ("SAM", "MAS")
            ):
                result += 1
    return result


result_1 = find_horizontal(puzzle) + find_vertical(puzzle) + find_diagonal(puzzle)
result_2 = find_cross(puzzle)
print("1:", result_1)
print("2:", result_2)
