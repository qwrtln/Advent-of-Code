import string

from common import get_puzzle


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    seeds = [(int(s), False) for s in puzzle[0].split(": ")[1].split()]

    for line in puzzle[1:]:
        if line == "" or line[0] not in string.digits:
            if line != "":
                seeds = [(s, False) for s, _ in seeds]
            continue

        destination, source, length = [int(n) for n in line.split()]

        for index, (current_seed, remapped) in enumerate(seeds):
            if current_seed in range(source, source + length) and not remapped:
                current_seed += destination - source
                seeds[index] = (current_seed, True)

    print(min(s[0] for s in seeds))
