from functools import cmp_to_key

with open("inputs/07.txt") as f:
    input = [line.strip() for line in f.readlines()]

cards = [line.split() for line in input]

order_rank = [[5], [1, 4], [2, 3], [1, 1, 3], [1, 2, 2], [1, 1, 1, 2], [1, 1, 1, 1, 1]]


def counts(lst):
    return {letter: lst.count(letter) for letter in set(lst)}


card_rank = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def joker_order(hand):
    joker_count = hand.count("J")
    letter_counts = counts(hand)
    if 0 < joker_count < 5:
        letter_counts = {
            count: letter for letter, count in letter_counts.items() if letter != "J"
        }
        letter = letter_counts[max(letter_counts.keys())]
        hand = hand.replace("J", letter, joker_count)
        letter_counts = counts(hand)
    order = sorted(list(letter_counts.values()))
    print(order)
    return order


def compare(hand1_bid, hand2_bid):
    hand1, _ = hand1_bid
    hand2, _ = hand2_bid
    order1_rank = order_rank.index(joker_order(hand1))
    order2_rank = order_rank.index(joker_order(hand2))
    if order1_rank < order2_rank:
        return -1
    elif order1_rank > order2_rank:
        return 1
    else:
        for c1, c2 in zip(hand1, hand2):
            if card_rank.index(c1) < card_rank.index(c2):
                return -1
            if card_rank.index(c1) > card_rank.index(c2):
                return 1


cards = sorted(cards, key=cmp_to_key(compare), reverse=True)

winnings = 0
for i, card in enumerate(cards, 1):
    winnings += i * int(card[1])
# print(cards)
print(winnings)
