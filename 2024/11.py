# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     108.0 ms ±   8.3 ms    [User: 98.3 ms, System: 9.4 ms]
#   Range (min … max):   100.0 ms … 133.9 ms    27 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):     212.4 ms ±  13.2 ms    [User: 185.0 ms, System: 26.7 ms]
#   Range (min … max):   201.3 ms … 251.3 ms    14 runs
#
import functools

stones = open("inputs/11.txt").read().strip().split("\n")[0].split()


@functools.cache
def parse_stone(stone, limit, depth=0):
    if depth == limit:
        return 1
    depth += 1
    if stone == "0":
        return parse_stone("1", limit, depth)
    elif len(stone) % 2 == 0:
        half = len(stone) // 2
        left = stone[:half].lstrip("0")
        right = stone[half:].lstrip("0")
        return parse_stone(left or "0", limit, depth) + parse_stone(
            right or "0", limit, depth
        )
    return parse_stone(str(int(stone) * 2024), limit, depth)


print("1:", sum(parse_stone(s, 25) for s in stones))
print("2:", sum(parse_stone(s, 75) for s in stones))
