puzzle = [line for line in open("inputs/04.txt").read().strip().split("\n")]

WORD = "XMAS"


def _transpose(l1):
    l2 = ["".join([row[i] for row in l1]) for i in range(len(l1[0]))]
    return l2


def find_horizontal(puzzle):
    result = 0
    for line in puzzle:
        result += line.count(WORD)
        result += line.count(WORD[::-1])
    return result


def find_vertical(puzzle):
    result = 0
    for line in _transpose(puzzle):
        result += line.count(WORD)
        result += line.count(WORD[::-1])
    return result


def find_diagonal(puzzle):
    result = 0
    for y in range(0, len(puzzle) - len(WORD) + 1):
        for x in range(0, len(puzzle[0]) - len(WORD) + 1):
            if (
                puzzle[y][x] == WORD[0]
                and puzzle[y + 1][x + 1] == WORD[1]
                and puzzle[y + 2][x + 2] == WORD[2]
                and puzzle[y + 3][x + 3] == WORD[3]
            ):
                result += 1

            if (
                puzzle[y][x] == WORD[3]
                and puzzle[y + 1][x + 1] == WORD[2]
                and puzzle[y + 2][x + 2] == WORD[1]
                and puzzle[y + 3][x + 3] == WORD[0]
            ):
                result += 1
    for y in range(len(puzzle) - 1, len(WORD) - 2, -1):
        for x in range(0, len(puzzle[0]) - len(WORD) + 1):
            if (
                puzzle[y][x] == WORD[3]
                and puzzle[y - 1][x + 1] == WORD[2]
                and puzzle[y - 2][x + 2] == WORD[1]
                and puzzle[y - 3][x + 3] == WORD[0]
            ):
                result += 1

            if (
                puzzle[y][x] == WORD[0]
                and puzzle[y - 1][x + 1] == WORD[1]
                and puzzle[y - 2][x + 2] == WORD[2]
                and puzzle[y - 3][x + 3] == WORD[3]
            ):
                result += 1
    return result


def find_cross(puzzle):
    result = 0
    for y, line in enumerate(puzzle[1 : len(puzzle) - 1], start=1):
        for x, char in enumerate(line[1 : len(line) - 1], start=1):
            if char == "A":
                if (
                    (puzzle[y + 1][x + 1] == "S" and puzzle[y - 1][x - 1] == "M")
                    or (puzzle[y + 1][x + 1] == "M" and puzzle[y - 1][x - 1] == "S")
                ) and (
                    (puzzle[y + 1][x - 1] == "S" and puzzle[y - 1][x + 1] == "M")
                    or (puzzle[y + 1][x - 1] == "M" and puzzle[y - 1][x + 1] == "S")
                ):
                    result += 1
    return result


result_1 = find_horizontal(puzzle) + find_vertical(puzzle) + find_diagonal(puzzle)
result_2 = find_cross(puzzle)
print("1:", result_1)
print("2:", result_2)
