from common import get_puzzle


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    score = 0
    for line in puzzle.split("\n"):
        values = line.split(":")[1]
        winning, gotten = values.split("|")
        winning = set(int(n.strip()) for n in winning.strip().split())
        gotten = set(int(n.strip()) for n in gotten.strip().split())
        overlaps = len(winning & gotten)
        points = 2 ** (overlaps - 1) if overlaps > 0 else 0
        score += points

    print(score)
