import string

from collections import defaultdict

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
    for y, x in neighbours:
        if puzzle[y][x] != ".":
            symbols.append(puzzle[y][x])
    return symbols


def find_neighbouring_gear(neighbours, puzzle):
    gears = []
    for y, x in neighbours:
        if puzzle[y][x] == "*":
            return (y, x)


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    puzzle = add_borders(puzzle)
    # print("\n".join(puzzle))

    result_1 = 0
    result_2 = 0

    gears_w_neighbours = defaultdict(list)

    for number, point in find_numbers(puzzle):
        neighbours = find_number_neighbours(number, point)

        symbols = find_neighbouring_symbols(neighbours, puzzle)
        if symbols:
            result_1 += int(number)

        gear = find_neighbouring_gear(neighbours, puzzle)
        if gear:
            gears_w_neighbours[gear].append(int(number))

    for numbers in gears_w_neighbours.values():
        if len(numbers) == 2:
            result_2 += numbers[0] * numbers[1]

    print(f"1: {result_1}")
    print(f"2: {result_2}")
