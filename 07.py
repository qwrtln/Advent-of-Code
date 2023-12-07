import bisect

from collections import Counter

from common import get_puzzle


cards = "AKQJT98765432"[::-1]
cards_values = {}

for i in range(len(cards)):
    cards_values[cards[i]] = i

cards_w_joker_values = {**cards_values, **{"J": -1}}


def get_rank(hand):
    match [c[1] for c in Counter(hand).most_common(5)]:
        case [1, 1, 1, 1, 1]:
            return 0  # high card
        case [2, 1, 1, 1]:
            return 1  # pair
        case [2, 2, 1]:
            return 2  # two pair
        case [3, 1, 1]:
            return 3  # three of a kind
        case [3, 2]:
            return 4  # full house
        case [4, 1]:
            return 5  # four of a kind
        case [5]:
            return 6  # five of a kind


def hand_value(hand):
    return [get_rank(hand)] + [cards_values[c] for c in hand]


def hand_w_joker_value(hand):
    counts = Counter(hand)
    joker_count = counts["J"]
    if not joker_count or joker_count == 5:
        return [get_rank(hand)] + [cards_w_joker_values[c] for c in hand]

    del counts["J"]
    card_to_replace = counts.most_common()[0][0]
    new_hand = hand.replace("J", card_to_replace)
    return [get_rank(new_hand)] + [cards_w_joker_values[c] for c in hand]

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
