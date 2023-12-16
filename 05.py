import string


from common import get_puzzle


def get_seed_ranges(line):
    numbers = [int(n) for n in line.split(": ")[1].split()]
    return list(zip(*[iter(numbers)] * 2))


if __name__ == "__main__":
    puzzle = [line for line in open("inputs/05.txt").read().strip().split("\n")]

    seeds = [(s, s + r - 1) for s, r in get_seed_ranges(puzzle[0])]
    processed_seeds = []

    for line in puzzle[3:]:
        if line == "" or line[0] not in string.digits:
            if line != "":
                seeds = [*seeds, *processed_seeds]
                processed_seeds = []
                print(line)
            continue

        destination, source, mapping_length = [int(n) for n in line.split()]
        seeds_left_to_process = []

        for start, end in seeds:
            overlap = range(
                max(start, source),
                min(end, source + mapping_length) + 1,
            )
            if overlap:
                new_range_start = min(overlap) + destination - source
                new_range_length = max(overlap) - min(overlap)
                processed_seeds.append(
                    (new_range_start, new_range_start + new_range_length)
                )
                if min(overlap) > start:
                    seeds_left_to_process.append((start, min(overlap)))
                if max(overlap) + 1 < end:
                    seeds_left_to_process.append((max(overlap) + 1, end))
            else:
                seeds_left_to_process.append((start, end))
        seeds = seeds_left_to_process

    print(min(s[0] for s in [*seeds, *processed_seeds]))
