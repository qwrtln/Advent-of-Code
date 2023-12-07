from common import get_puzzle


cards = "AKQJT98765432"[::-1]
card_values = {}

for i in range(len(cards)):
    card_values[cards[i]] = i


def hand_value(hand):
    counts = sorted([hand.count(c) for c in set(hand)], reverse=True)
    value = None
    match counts:
        case [1, 1, 1, 1, 1]:
            value = 0  # high card
        case [2, 1, 1, 1]:
            value = 1  # pair
        case [2, 2, 1]:
            value = 2  # two pair
        case [3, 1, 1]:
            value = 3  # three of a kind
        case [3, 2]:
            value = 4  # full house
        case [4, 1]:
            value = 5  # four of a kind
        case [5]:
            value = 6  # five of a kind
    return [value] + [card_values[c] for c in hand]

if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=True)

    hands = sorted(puzzle, key=lambda h: hand_value(h.split()[0]))
    result = 0
    for index, line in enumerate(hands, start=1):
        result += index * int(line.split()[1])
    print(result)
