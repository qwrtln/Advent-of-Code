import itertools


def is_key(item):
    return item[0] == "#####"


def key_matches_lock(key, lock):
    for k_col, l_col in zip(key, lock):
        if k_col.count("#") > l_col.count("."):
            return False
    return True


def count_key_lock_matches(keys, locks):
    return sum(key_matches_lock(k, l) for k, l in itertools.product(keys, locks))


def transpose(item):
    return ["".join(r) for r in list(zip(*item))]


def parse_puzzle(puzzle):
    keys, locks, item = [], [], []
    for line in open(puzzle).read().strip().split("\n"):
        if line == "":
            keys.append(transpose(item)) if is_key(item) else locks.append(
                transpose(item)
            )
            item = []
            continue
        item.append(line)
    keys.append(transpose(item)) if is_key(item) else locks.append(transpose(item))
    return keys, locks


keys, locks = parse_puzzle("inputs/25.txt")
print("1:", count_key_lock_matches(keys, locks))
