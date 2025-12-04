puzzle = [line for line in open("inputs/04.txt").read().strip().split("\n")]


def get_neighbours(y, x, puzzle):
    for dy, dx in [
        (1, 1),
        (1, 0),
        (1, -1),
        (0, 1),
        (0, -1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
    ]:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < len(puzzle[0]) and 0 <= new_y < len(puzzle):
            yield (new_y, new_x)


def remove_rolls(puzzle, previously_removed):
    removed_count = 0
    newly_removed = set()
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if puzzle[y][x] == "." or (y, x) in previously_removed:
                continue
            rolls = 0
            for yn, xn in get_neighbours(y, x, puzzle):
                if (yn, xn) not in previously_removed:
                    rolls += puzzle[yn][xn] == "@"
            if rolls < 4:
                newly_removed.add((y, x))
                removed_count += 1
    return removed_count, newly_removed


removed = set()
result_1, newly_removed = remove_rolls(puzzle, removed)
print("1:", result_1)

result_2 = result_1
while newly_removed:
    removed |= newly_removed
    current_result, newly_removed = remove_rolls(puzzle, removed)
    result_2 += current_result


print("2:", result_2)
