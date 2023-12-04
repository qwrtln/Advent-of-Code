from collections import defaultdict

from common import get_puzzle


def find_line_score(line):
    values = line.split(":")[1]
    winning, gotten = values.split("|")
    winning = set(int(n.strip()) for n in winning.strip().split())
    gotten = set(int(n.strip()) for n in gotten.strip().split())
    matches = len(winning & gotten)
    return 2 ** (matches - 1) if matches else 0, matches


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    result_1 = 0
    result_2 = 0
    copies = defaultdict(lambda: 0)
    for card_no, line in enumerate(puzzle.split("\n"), start=1):
        copies[card_no] += 1
        score, matches = find_line_score(line)
        result_1 += score
        for i in range(card_no + 1, card_no + matches + 1):
            copies[i] += copies[card_no]

    print("1:", result_1)
    print("2:", sum(copies.values()))
