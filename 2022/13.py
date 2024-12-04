import ast
import string

from functools import cmp_to_key


from common import read_file


def pair_cmp(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif right < left:
            return -1
    elif isinstance(left, list) and isinstance(right, list):
        li, ri = iter(left), iter(right)
        left_stop, right_stop = False, False
        while True:
            try:
                l = next(li)
            except StopIteration:
                left_stop = True
            try:
                r = next(ri)
            except StopIteration:
                right_stop = True
            if left_stop and not right_stop:
                return 1
            elif not left_stop and right_stop:
                return -1
            elif left_stop and right_stop:
                break
            result = pair_cmp(l, r)
            if result != 0:
                return result
    elif isinstance(left, list) and isinstance(right, int):
        return pair_cmp(left, [right])
    elif isinstance(left, int) and isinstance(right, list):
        return pair_cmp([left], right)
    return 0


if __name__ == "__main__":
    puzzle = read_file("13").split("\n")[:-1]

    pairs = (len(puzzle) + 1) // 3
    in_order = []
    for i in range(pairs):
        left = ast.literal_eval(puzzle[3 * i])
        right = ast.literal_eval(puzzle[3 * i + 1])
        if pair_cmp(left, right) == 1:
            in_order.append(i + 1)
    print("Pairs in order:", sum(in_order))

    puzzle_to_sort = [ast.literal_eval(p) for p in puzzle if p != ""] + [[[2]], [[6]]]
    result = sorted(puzzle_to_sort, key=cmp_to_key(pair_cmp), reverse=True)
    i2 = result.index([[2]]) + 1
    i6 = result.index([[6]]) + 1
    print("Decoder key:", i2 * i6)
