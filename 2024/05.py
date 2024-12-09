# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     146.1 ms ±   9.8 ms    [User: 142.6 ms, System: 3.3 ms]
#   Range (min … max):   135.9 ms … 170.0 ms    20 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):      84.9 ms ±   6.2 ms    [User: 71.1 ms, System: 13.1 ms]
#   Range (min … max):    79.6 ms … 105.0 ms    36 runs
#
import functools
from collections import defaultdict

puzzle = [line for line in open("inputs/05.txt").read().strip().split("\n")]

RULES = []
RULES_DICT = defaultdict(list)
UPDATES = []
for line in puzzle:
    if "|" in line:
        r1, r2 = line.split("|")
        RULES.append((int(r1), int(r2)))
        RULES_DICT[int(r1)].append(int(r2))
    elif "," in line:
        UPDATES.append(list(map(int, line.split(","))))


def is_ordering_correct(pages, rules):
    for idx, page in enumerate(pages):
        for remaining in pages[idx + 1 :]:
            if (remaining, page) in rules:
                return False
    return True


@functools.cmp_to_key
def custom_sort(a, b):
    if b in RULES_DICT[a]:
        return -1
    if a in RULES_DICT[b]:
        return 1
    return 0


result_1 = 0
result_2 = 0
for pages in UPDATES:
    if is_ordering_correct(pages, RULES):
        result_1 += pages[len(pages) // 2]
    else:
        pages.sort(key=custom_sort)
        result_2 += pages[len(pages) // 2]

print("1:", result_1)
print("2:", result_2)
