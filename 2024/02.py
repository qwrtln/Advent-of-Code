# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      15.2 ms ±   1.1 ms    [User: 12.8 ms, System: 2.3 ms]
#   Range (min … max):    13.4 ms …  19.2 ms    180 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):      77.9 ms ±   6.1 ms    [User: 65.6 ms, System: 11.9 ms]
#   Range (min … max):    72.2 ms …  94.0 ms    39 runs
#
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
