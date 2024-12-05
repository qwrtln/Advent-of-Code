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
