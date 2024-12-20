# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     585.8 ms ±  26.4 ms    [User: 571.2 ms, System: 12.0 ms]
#   Range (min … max):   559.7 ms … 645.5 ms    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     161.1 ms ±   7.3 ms    [User: 140.4 ms, System: 20.5 ms]
#   Range (min … max):   154.8 ms … 181.4 ms    16 runs
#
import functools

puzzle = open("inputs/19.txt").read().strip().split("\n")

PATTERNS = set(p for p in puzzle[0].split(", "))
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
