import string

from common import get_puzzle


def add_borders(puzzle):
    lines = puzzle.split("\n")
    output = []
    horizontal = "." * (len(lines[0]) + 2)
    output = [f".{l}." for l in lines]
    return [horizontal, *output, horizontal]


def find_numbers(puzzle):
    number = ""
    starting_point = (0, 0)
    for y in range(len(puzzle[0])):
        for x in range(len(puzzle)):
            if puzzle[y][x] in string.digits:
                if number == "":
                    starting_point = (y, x)
                number += puzzle[y][x]
            elif number != "":
                yield number, starting_point
                number = ""


def find_number_neighbours(number, starting_point):
    y, x = starting_point
    upper = [(y - 1, i) for i in range(x - 1, x + 1 + len(number))]
    lower = [(y + 1, i) for i in range(x - 1, x + 1 + len(number))]
    return [*upper, (y, x - 1), (y, x + len(number)), *lower]


def find_neighbouring_symbols(neighbours, puzzle):
    symbols = []
    for (y, x) in neighbours:
        if puzzle[y][x] != ".":
            symbols.append(puzzle[y][x])
    return symbols


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    puzzle = add_borders(puzzle)
    # print("\n".join(puzzle))

    result = 0

    for number, point in find_numbers(puzzle):
        neighbours = find_number_neighbours(number, point)
        symbols = find_neighbouring_symbols(neighbours, puzzle)
        if symbols:
            # input(f"{number} has neighbouring {symbols=}, so adding it")
            result += int(number)
        # else:
        #     input(f"{number} has no neighbouring symbols")

    print(result)
