# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      3.953 s ±  0.067 s    [User: 3.788 s, System: 0.154 s]
#   Range (min … max):    3.887 s …  4.104 s    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):      4.903 s ±  0.105 s    [User: 4.663 s, System: 0.219 s]
#   Range (min … max):    4.761 s …  5.117 s    10 runs
#
import collections

puzzle = open("inputs/22.txt").read().strip().split("\n")

ITERATIONS = 2000
PRUNE = 16777216


def generate_next(secret):
    secret = ((secret << 6) ^ secret) % PRUNE
    secret = ((secret >> 5) ^ secret) % PRUNE
    secret = ((secret << 11) ^ secret) % PRUNE
    return secret % PRUNE


def calculate_candidate_result(candidate, secret_prices):
    return sum(p.get(candidate, 0) for p in secret_prices.values())


def parse_secret(secret):
    previous_price = secret % 10
    deltas = []
    delta_prices = {}
    all_deltas = collections.defaultdict(set)

    for _ in range(ITERATIONS):
        secret = generate_next(secret)
        price = secret % 10
        delta = price - previous_price

        if len(deltas) == 4:
            deltas = [*deltas[1:], delta]
            t_deltas = tuple(deltas)
            all_deltas[price].add(t_deltas)
            if t_deltas not in delta_prices:
                delta_prices[t_deltas] = price
        elif delta is not None:
            deltas.append(delta)

        previous_price = price

    return all_deltas, delta_prices, secret


def find_best_candidate(sequences, secret_prices):
    max_result = 0
    candidates = (
        sequences[9] & sequences[8] & sequences[7] & sequences[6] & sequences[5]
    )
    for candidate in candidates:
        result = calculate_candidate_result(candidate, secret_prices)
        if result > max_result:
            max_result = result
    return max_result


def parse_secrets(puzzle):
    sequences = collections.defaultdict(set)
    secret_prices = {}
    result = 0
    for line in puzzle:
        secret_deltas, delta_prices, secret = parse_secret(int(line))
        for price, deltas in secret_deltas.items():
            sequences[price].update(deltas)
        secret_prices[int(line)] = delta_prices
        result += secret
    return sequences, secret_prices, result


sequences, secret_prices, result_1 = parse_secrets(puzzle)
print("1:", result_1)
print("2:", find_best_candidate(sequences, secret_prices))
