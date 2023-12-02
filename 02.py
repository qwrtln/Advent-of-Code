import math

from common import get_puzzle

WORDS = {"red": 12, "green": 13, "blue": 14}


def get_game_id(line: str) -> int:
    game = line.split(":")[0]
    return int(game.split(" ")[1])


def is_set_possible(s: str) -> bool:
    balls = s.split(", ")
    for ball in balls:
        num, color = ball.split(" ")
        if int(num) > WORDS[color]:
            return False
    return True


def check_maxes(s: str, maxes: dict[str, int]):
    balls = s.split(", ")
    for ball in balls:
        num, color = ball.split(" ")
        if int(num) > maxes[color]:
            maxes[color] = int(num)


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    game_ids = 0
    powers = 0
    for line in puzzle.split("\n"):
        possible = []
        maxes = {"red": 0, "green": 0, "blue": 0}
        sets = line.split(":")[1].split("; ")
        for s in sets:
            possible.append(is_set_possible(s.strip()))
            check_maxes(s.strip(), maxes)
        if False not in possible:
            game_ids += get_game_id(line)
        powers += math.prod(maxes.values())

    print("Part 1:", game_ids)
    print("Part 2:", powers)
