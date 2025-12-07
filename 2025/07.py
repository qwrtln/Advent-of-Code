import collections
import functools

puzzle = [line for line in open("inputs/07.txt").read().strip().split("\n")]


def count_splits(puzzle, y, x):
    result = 0
    beams = collections.defaultdict(set)
    beams[y].add(x)
    while True:
        for x in beams[y]:
            match puzzle[y + 1][x]:
                case ".":
                    beams[y + 1].add(x)
                case "^":
                    result += 1
                    beams[y + 1].update([x + 1, x - 1])
        y += 1
        if y + 1 == len(puzzle):
            return result


def count_paths(puzzle, y, x):
    @functools.cache
    def find_result(y, x):
        if y == len(puzzle) - 1:
            return 1
        return (
            find_result(y + 1, x)
            if puzzle[y + 1][x] == "."
            else find_result(y + 1, x + 1) + find_result(y + 1, x - 1)
        )

    return find_result(y, x)


starting_point = (1, puzzle[0].index("S"))
print("1:", count_splits(puzzle, *starting_point))
print("2:", count_paths(puzzle, *starting_point))
