import math

from collections import Counter

from common import get_puzzle

BALLS = Counter(red=12, green=13, blue=14)


def get_game_id(line: str) -> int:
    game = line.split(":")[0]
    return int(game.split()[1])


def make_set(game_set: str) -> Counter:
    return Counter(
        {
            color: int(num)
            for num, color in [balls.split() for balls in game_set.split(", ")]
        }
    )


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    result_1 = 0
    result_2 = 0
    for line in puzzle.split("\n"):
        game_sets = [make_set(s) for s in line.split(":")[1].split("; ")]
        if all([s <= BALLS for s in game_sets]):
            result_1 += get_game_id(line)
        maxes = Counter()
        for s in game_sets:
            maxes |= s
        result_2 += math.prod(maxes.values())

    print("Part 1:", result_1)
    print("Part 2:", result_2)
