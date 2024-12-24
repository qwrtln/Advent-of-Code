# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      42.6 ms ±   1.8 ms    [User: 33.6 ms, System: 9.0 ms]
#   Range (min … max):    40.0 ms …  50.1 ms    71 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     170.3 ms ±   9.0 ms    [User: 150.9 ms, System: 19.1 ms]
#   Range (min … max):   163.0 ms … 191.4 ms    18 runs
#
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


def move(current, target, graph):
    queue = collections.deque()
    seen = collections.defaultdict(int)
    shortest = float("inf")
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
                results.append("".join(d for d, _ in path[1:]))
        for direction, neighbour in graph[current].items():
            if seen[neighbour] < graph["LIMIT"]:
                queue.append(path + [(direction, neighbour)])
                seen[neighbour] += 1
    return results


def is_zigzag(moves):
    if len(moves) != 3:
        return False
    a, b, c = list(moves)
    return a == c and a != b


def prepopulate_graph(graph):
    paths = collections.defaultdict(dict)
    for start, end in itertools.product(
        [k for k in graph.keys() if k != "LIMIT"], repeat=2
    ):
        paths[start][end] = [m for m in move(start, end, graph) if not is_zigzag(m)]
    return paths


@functools.lru_cache(maxsize=1)
def numeric_cache():
    return prepopulate_graph(NUMERIC_GRAPH)


@functools.lru_cache(maxsize=1)
def directional_cache():
    return prepopulate_graph(DIRECTIONAL_GRAPH)


def remap_directions(keys, previous="A", index=0, current_moves=""):
    results = []
    if index == len(keys):
        results.append(current_moves)
        # input("Done!")
        return results
    for moves in directional_cache()[previous][keys[index]]:
        for r in remap_directions(
            keys, keys[index], index + 1, current_moves + moves + "A"
        ):
            # print(r, "<-", index)
            results.append(r)
    return results


@functools.cache
def find_shortest_sequence(keys, depth):
    if depth == 0:
        return len(keys)
    result = 0
    sequences = keys.split("A")
    for moves in sequences[:-1]:
        shortest = float("inf")
        for sequence in remap_directions(moves + "A"):
            length = find_shortest_sequence(sequence, depth - 1)
            if length < shortest:
                shortest = length
        result += shortest
    if sequences[-1]:
        shortest = float("inf")
        for sequence in remap_directions(sequences[-1] + "A"):
            length = find_shortest_sequence(sequence, depth - 1)
            if length < shortest:
                shortest = length
        result += shortest
    return result


def numeric_to_directions(keys, start="A"):
    result = []
    for k in keys:
        result.append([f"{c}A" for c in numeric_cache()[start][k]])
        start = k
    return result


def build_possible_sequences(possibilities):
    ranges = [range(len(p)) for p in possibilities]
    for c in itertools.product(*ranges):
        result = ""
        for i, arr in zip(c, possibilities):
            result += arr[i]
        yield result


result_1 = 0
result_2 = 0
for line in puzzle:
    numeric = int(line.strip("A"))
    possibilities = numeric_to_directions(line)
    result_1 += (
        min(
            find_shortest_sequence(s, depth=2)
            for s in build_possible_sequences(possibilities)
        )
        * numeric
    )
    result_2 += (
        min(
            find_shortest_sequence(s, depth=25)
            for s in build_possible_sequences(possibilities)
        )
        * numeric
    )
print("1:", result_1)
print("2:", result_2)
