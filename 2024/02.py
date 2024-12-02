puzzle = [line for line in open("inputs/02.txt").read().strip().split("\n")]


def levels_safe(levels):
    diffs = [levels[n] - levels[n - 1] for n in range(1, len(levels))]
    return all(d in range(1, 4) for d in diffs) or all(d in range(-3, 0) for d in diffs)


def disregard_one(levels):
    for i in range(len(levels)):
        if levels_safe([*levels[:i], *levels[i + 1 :]]):
            return True
    return False


result_1 = 0
result_2 = 0
for line in puzzle:
    levels = [int(n) for n in line.split()]
    result_1 += levels_safe(levels)
    result_2 += disregard_one(levels)

print("1:", result_1)
print("2:", result_2)
