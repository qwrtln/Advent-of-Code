from operator import itemgetter

from common import get_puzzle


WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def find_words(line: str) -> str:
    words = []
    for w in WORDS.keys():
        i_left = line.find(w)
        if i_left != -1:
            words.append((w, i_left))
        i_right = line.rfind(w)
        if i_right != -1 and i_right != i_left:
            words.append((w, i_right))

    if len(words) > 1:
        words.sort(key=itemgetter(1))
        words = [words[0], words[-1]]

    return words


def find_digits(digit_left: int, digit_right: int, line: str, words: list):
    first, second = None, None
    if len(words) == 2:
        if digit_left > words[0][1]:
            first = WORDS[words[0][0]]
        if digit_right < words[1][1]:
            second = WORDS[words[1][0]]
    elif len(words) == 1:
        if digit_left > words[0][1]:
            first = WORDS[words[0][0]]
        elif digit_right < words[0][1]:
            second = WORDS[words[0][0]]
    return first, second


def get_number(line: str) -> int:
    digit_left = None
    digit_right = None
    first = None
    second = None

    words = find_words(line)

    for char in line:
        try:
            first = int(char)
            digit_left = line.find(char)
            break
        except ValueError:
            pass

    for char in line[::-1]:
        try:
            second = int(char)
            digit_right = line.rfind(char)
            break
        except ValueError:
            pass

    try:
        first_w, second_w = find_digits(digit_left, digit_right, line, words)
        first = first_w if first_w is not None else first
        second = second_w if second_w is not None else second
    except TypeError:
        if len(words) == 2:
            first = WORDS[words[0][0]]
            second = WORDS[words[1][0]]
        elif len(words) == 1:
            first = second = WORDS[words[0][0]]

    return 10 * first + second


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    number = 0

    for line in puzzle:
        number += get_number(line)

    print(number)
