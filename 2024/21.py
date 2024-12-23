import collections
import functools
import itertools

puzzle = open("inputs/21.txt").read().strip().split("\n")

NUMERIC_GRAPH = {
    # 789
    # 456
    # 123
    #  0A
    "0": {"^": "2", ">": "A"},
    "1": {">": "2", "^": "4"},
    "2": {"<": "1", ">": "3", "^": "5", "v": "0"},
    "3": {"<": "2", "^": "6", "v": "A"},
    "4": {"^": "7", "v": "1", ">": "5"},
    "5": {"^": "8", ">": "6", "v": "2", "<": "4"},
    "6": {"^": "9", "<": "5", "v": "3"},
    "7": {">": "8", "v": "4"},
    "8": {">": "9", "v": "5", "<": "7"},
    "9": {"<": "8", "v": "6"},
    "A": {"<": "0", "^": "3"},
    "LIMIT": 9,
}

DIRECTIONAL_GRAPH = {
    #  ^A
    # <v>
    "^": {">": "A", "v": "v"},
    "v": {"<": "<", "^": "^", ">": ">"},
    "<": {">": "v"},
    ">": {"^": "A", "<": "v"},
    "A": {"<": "^", "v": ">"},
    "LIMIT": 2,
}


def move(current, target, graph, *, suffix="A"):
    queue = collections.deque()
    seen = collections.defaultdict(int)
    shortest = 1e9
    results = []
    queue.append([(None, current)])
    while queue:
        path = queue.popleft()
        current = path[-1][1]
        if current == target:
            if len(path) < shortest:
                shortest = len(path)
                results = []
            if len(path) == shortest:
                results.append("".join(d for d, _ in path[1:]) + suffix)
        for direction, neighbour in graph[current].items():
            if seen[neighbour] < graph["LIMIT"]:
                queue.append(path + [(direction, neighbour)])
                seen[neighbour] += 1
    return results


@functools.cache
def move_num(current, target):
    return move(current, target, NUMERIC_GRAPH)


@functools.cache
def move_dir(current, target):
    return move(current, target, DIRECTIONAL_GRAPH)


def verify_pressed_keys(path, graph):
    current = "A"
    result = ""
    for keys in path.split("A"):
        for key in keys:
            current = graph[current][key]
        result += current
    return result


def numeric_to_possibilities(numeric, start="A"):
    possibilities = []
    for digit in numeric:
        possibilities.append(move(start, digit, NUMERIC_GRAPH))
        start = digit
    return possibilities


def possibilities_to_dir(possibilities, start="A"):
    ranges = [range(len(p)) for p in possibilities]
    results = set()
    for c in itertools.product(*ranges):
        result = ""
        for i, arr in zip(c, possibilities):
            result += arr[i]
        results.add(result)

    final_results = set()
    shortest = 1e9
    for r in results:
        possibilities = []
        for mark in r:
            possibilities.append(move(start, mark, DIRECTIONAL_GRAPH))
            start = mark
        ranges = [range(len(p)) for p in possibilities]
        for c in itertools.product(*ranges):
            result = ""
            for i, arr in zip(c, possibilities):
                result += arr[i]
            if len(result) < shortest:
                shortest = len(result)
                final_results = set()
            if len(result) == shortest:
                final_results.add(result)
    return final_results


def dirs_to_dirs(dirs):
    for d in dirs:
        yield from dir_to_dirs(d)


@functools.cache
def dir_to_dirs(dir):
    possibilities = []
    shortest = 1e9
    start = "A"
    for mark in dir:
        possibilities.append(move_dir(start, mark))
        start = mark
    ranges = [range(len(p)) for p in possibilities]
    for c in itertools.product(*ranges):
        result = ""
        for i, arr in zip(c, possibilities):
            result += arr[i]
        if len(result) < shortest:
            shortest = len(result)
        if len(result) == shortest:
            yield result


def calculate_complexity(line):
    numeric = int(line.strip("A"))
    possibilities = numeric_to_possibilities(line)
    results = possibilities_to_dir(possibilities)
    shortest = 1e9
    for final in dirs_to_dirs(results):
        if len(final) < shortest:
            shortest = len(final)
    return numeric * shortest


result = 0
for line in puzzle:
    result += calculate_complexity(line)
print(result)

# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
