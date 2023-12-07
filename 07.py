import bisect

from common import get_puzzle


cards = "AKQJT98765432"[::-1]
cards_values = {}

for i in range(len(cards)):
    cards_values[cards[i]] = i

cards_w_joker_values = {**cards_values, **{"J": -1}}


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
    return [value] + [cards_values[c] for c in hand]


def hand_w_joker_value(hand):
    counts = sorted([hand.count(c) for c in set(hand)], reverse=True)
    joker_count = hand.count("J")
    value = None
    match counts:
        case [1, 1, 1, 1, 1]:
            value = 0 + joker_count
        case [2, 1, 1, 1]:
            if joker_count:
                value = 3
            else:
                value = 1
        case [2, 2, 1]:
            if joker_count == 2:
                value = 5
            elif joker_count == 1:
                value = 4
            else:
                value = 2
        case [3, 1, 1]:
            if joker_count:
                value = 5
            else:
                value = 3
        case [3, 2]:
            if joker_count in (2, 3):
                value = 6
            elif joker_count == 1:
                value = 5
            else:
                value = 4
        case [4, 1]:
            if joker_count:
                value = 6
            else:
                value = 5
        case [5]:
            value = 6
    return [value] + [cards_w_joker_values[c] for c in hand]


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    hands_1 = []
    hands_2 = []
    for hand in puzzle:
        bisect.insort(hands_1, hand, key=lambda h: hand_value(h.split()[0]))
        bisect.insort(hands_2, hand, key=lambda h: hand_w_joker_value(h.split()[0]))

    result_1 = 0
    result_2 = 0

    for index, (line_1, line_2) in enumerate(zip(hands_1, hands_2), start=1):
        result_1 += index * int(line_1.split()[1])
        result_2 += index * int(line_2.split()[1])

    print("1:", result_1)
    print("2:", result_2)
