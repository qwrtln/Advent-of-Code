# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     478.4 ms ±  16.8 ms    [User: 467.8 ms, System: 10.3 ms]
#   Range (min … max):   452.9 ms … 500.7 ms    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     147.5 ms ±   7.9 ms    [User: 124.0 ms, System: 23.0 ms]
#   Range (min … max):   140.4 ms … 171.6 ms    20 runs
#
import functools

puzzle = open("inputs/19.txt").read().strip().split("\n")

PATTERNS = [p for p in puzzle[0].split(", ")]
DESIGNS = puzzle[2:]


@functools.cache
def ways_design_possible(design):
    if not design:
        return 1
    ways = 0
    for pattern in PATTERNS:
        if design.startswith(pattern):
            ways += ways_design_possible(design[len(pattern) :])
    return ways


ways = [ways_design_possible(d) for d in DESIGNS]
print("1:", sum(bool(w) for w in ways))
print("2:", sum(ways))
