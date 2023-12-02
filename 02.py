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



if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    result = 0
    for line in puzzle.split("\n"):
        sets = line.split(":")[1].split("; ")
        possible = []
        for s in sets:
            possible.append(is_set_possible(s.strip()))
        if False not in possible:
            result += get_game_id(line)

    print(result)
