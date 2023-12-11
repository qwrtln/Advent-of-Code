import itertools


puzzle = [l for l in open("inputs/11.txt").read().strip().split("\n")]


expanded_rows = []
for row in puzzle:
    expanded_rows.append(row)
    if set(row) == {"."}:
        expanded_rows.append(row)
        

expanded_columns = []
for x in range(len(expanded_rows[0])):
    col = "".join(l[x] for l in expanded_rows)
    expanded_columns.append(col)
    if set(col) == {"."}:
        expanded_columns.append(col)


expanded_puzzle = []
for y in range(len(expanded_columns[0])):
    expanded_puzzle.append("".join([l[y] for l in expanded_columns]))


puzzle = expanded_puzzle
galaxies = set()
for y in range(len(puzzle)):
    for x in range(len(puzzle[0])):
        if puzzle[y][x] == "#":
            galaxies.add((y, x))

result_1 = 0
for (y1, x1), (y2, x2) in itertools.combinations(galaxies, 2):
    result_1 += abs(y2 - y1) + abs(x2 - x1)

print(result_1)
