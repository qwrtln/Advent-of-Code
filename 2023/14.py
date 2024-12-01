import copy


puzzle = [line for line in open("inputs/14.txt").read().strip().split("\n")]

CYCLES = 1000000000


def tilt_vertical(puzzle, north=True):
    cols = ["".join([r[i] for r in puzzle]) for i in range(len(puzzle[0]))]
    sorted_cols = []
    for col in cols:
        sorted_cols.append(
            "#".join(["".join(sorted(li, reverse=north)) for li in col.split("#")])
        )
    return ["".join([c[i] for c in sorted_cols]) for i in range(len(sorted_cols[0]))]


def tilt_horizontal(puzzle, west=True):
    sorted_rows = []
    for row in puzzle:
        sorted_rows.append(
            "#".join(["".join(sorted(li, reverse=west)) for li in row.split("#")])
        )
    return sorted_rows


def cycle(puzzle):
    puzzle = tilt_vertical(puzzle, north=True)
    puzzle = tilt_horizontal(puzzle, west=True)
    puzzle = tilt_vertical(puzzle, north=False)
    puzzle = tilt_horizontal(puzzle, west=False)
    return puzzle


def calculate_load(puzzle):
    result = 0
    cols = ["".join([r[i] for r in puzzle]) for i in range(len(puzzle[0]))]
    for col in cols:
        for index, row in enumerate(range(len(col), 0, -1)):
            if col[index] == "O":
                result += row
    return result


print("1:", calculate_load(tilt_vertical(copy.copy(puzzle))))

cycles = []
part_2_puzzle = copy.copy(puzzle)
while puzzle not in cycles:
    cycles.append(puzzle)
    puzzle = cycle(puzzle)

cycle_offset = cycles.index(puzzle)
cycle_length = len(cycles) - cycle_offset
for _ in range(cycle_offset + (CYCLES - cycle_offset) % cycle_length):
    part_2_puzzle = cycle(part_2_puzzle)

print("2:", calculate_load(part_2_puzzle))
