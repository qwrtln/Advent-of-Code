puzzle = [line for line in open("inputs/14.txt").read().strip().split("\n")]


cols = ["".join([r[i] for r in puzzle]) for i in range(len(puzzle[0]))]
result_1 = 0
for col in cols:
    sorted_col = "#".join(["".join(sorted(li, reverse=True)) for li in col.split("#")])
    for index, row in enumerate(range(len(sorted_col), 0, -1)):
        if sorted_col[index] == "O":
            result_1 += row

print("1:", result_1)
