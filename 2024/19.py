# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     519.0 ms ±  15.3 ms    [User: 507.2 ms, System: 10.9 ms]
#   Range (min … max):   492.7 ms … 545.5 ms    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     190.6 ms ±  11.4 ms    [User: 164.2 ms, System: 25.7 ms]
#   Range (min … max):   179.7 ms … 222.4 ms    16 runs
#
import functools

puzzle = open("inputs/19.txt").read().strip().split("\n")

PATTERNS = set(p for p in puzzle[0].split(", "))
DESIGNS = puzzle[2:]


@functools.cache
def is_design_possible(design):
    if design in PATTERNS:
        return True
    for i in range(1, len(design)):
        prefix, rest = design[:i], design[i:]
        if prefix in PATTERNS and is_design_possible(rest):
            return True
    return False


@functools.cache
def ways_design_possible(design):
    if not design:
        return 1
    ways = 0
    for pattern in PATTERNS:
        if design.startswith(pattern):
            ways += ways_design_possible(design[len(pattern) :])
    return ways


result_1 = 0
result_2 = 0
for d in DESIGNS:
    if is_design_possible(d):
        result_1 += 1
        result_2 += ways_design_possible(d)
print("1:", result_1)
print("2:", result_2)
