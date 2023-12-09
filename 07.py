import bisect

from collections import Counter


cards_values = {card: i for i, card in enumerate("23456789TJQKA")}
cards_w_joker_values = {**cards_values, **{"J": -1}}


def get_rank(hand):
    return [
        [1, 1, 1, 1, 1],
        [2, 1, 1, 1],
        [2, 2, 1],
        [3, 1, 1],
        [3, 2],
        [4, 1],
        [5],
    ].index([c[1] for c in Counter(hand).most_common(5)])


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
    puzzle = [l for l in open("inputs/07.txt").read().strip().split("\n")]

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
