import copy
import itertools


puzzle = [line for line in open("inputs/13.txt").read().strip().split("\n\n")]


def is_symmetrical(elements, index):
    to_check = elements[: index + 1]
    first, *remaining, last = to_check
    while remaining:
        if first != last:
            return False
        first, *remaining, last = remaining
    return first == last


def find_elements_differing_by_one_character(elements):
    diffs = 0
    candidates = {}
    pairs = itertools.combinations(range(len(elements)), 2)
    diff_index = 0
    for i_1, i_2 in pairs:
        for i_diff, (a, b) in enumerate(zip(elements[i_1], elements[i_2])):
            if a != b:
                diff_index = i_diff
                diffs += 1
        if diffs == 1:
            candidates[(i_1, i_2)] = diff_index
        diffs = 0
    return candidates


def find_axis(elements):
    first, *remaining, last = elements
    from_beginning = []
    to_end = []
    if first in remaining:
        from_beginning = [
            i for i, x in enumerate(remaining, 1) if x == first and i % 2 == 1
        ]
    if last in remaining:
        to_end = [
            i
            for i, x in enumerate(remaining, 1)
            if x == last and (len(elements) - i) % 2 == 0
        ]
    results = []
    for candidate in from_beginning:
        if is_symmetrical(elements, candidate):
            index = candidate // 2 + 1
            results.append(index)
    for candidate in to_end:
        if is_symmetrical(elements[::-1], len(elements) - candidate - 1):
            to_add = (len(elements) - candidate) / 2
            assert to_add == int(to_add), f"Can't be uneven! {to_add}"
            results.append(int(candidate + to_add))
    return results


def toggle_character(elements, i_el, i_char):
    char_toggle = {
        "#": ".",
        ".": "#",
    }
    element = elements[i_el]
    new_element = (
        element[:i_char] + char_toggle[element[i_char]] + element[i_char + 1 :]
    )
    elements[i_el] = new_element
    return elements


def calculate_hall_score(hall):
    rows = hall.split("\n")
    cols = ["".join([r[i] for r in rows]) for i in range(len(rows[0]))]
    sym_row = find_axis(rows)
    sym_col = find_axis(cols)
    if sym_row and sym_col:
        assert False, "Two axes, impossible!"
    elif not sym_row and not sym_col:
        assert False, "No symmetry, impossible!"
    elif sym_col:
        # assert are_cols_symmetric(sym_col, hall), f"No col symmetry at {i}"
        return sym_col[0]
    elif sym_row:
        # assert are_rows_symmetric(sym_row, hall), f"No row symmetry at {i}"
        return sym_row[0] * 100
    assert False, "Should never get here"


def calculate_new_hall_score(hall, old_score):
    rows = hall.split("\n")
    cols = ["".join([r[i] for r in rows]) for i in range(len(rows[0]))]
    sym_row = find_axis(rows)
    sym_col = find_axis(cols)
    possible_scores = []
    for r in sym_row:
        possible_scores.append(r * 100)
    for c in sym_col:
        possible_scores.append(c)
    new_score = [s for s in possible_scores if s != old_score]
    assert len(new_score) <= 1, f"Should be at most one new score! {new_score=}"
    if new_score:
        return new_score[0]
    return 0


def make_hall_from_cols(cols):
    rows = ["".join([c[i] for c in cols]) for i in range(len(cols[0]))]
    return "\n".join(rows)


result_1 = 0
result_2 = 0
for hall in puzzle:
    rows = hall.split("\n")
    cols = ["".join([r[i] for r in rows]) for i in range(len(rows[0]))]
    hall_score_1 = calculate_hall_score(hall)
    result_1 += hall_score_1

    possibilities = set()
    smudge_r_candidates = find_elements_differing_by_one_character(rows)
    for (r1, r2), index in smudge_r_candidates.items():
        for r in (r1, r2):
            new_rows = toggle_character(copy.copy(rows), r, index)
            new_hall = "\n".join(new_rows)
            possibilities.add(calculate_new_hall_score(new_hall, hall_score_1))

    smudge_c_candidates = find_elements_differing_by_one_character(cols)
    for (c1, c2), index in smudge_c_candidates.items():
        for c in (c1, c2):
            new_cols = toggle_character(copy.copy(cols), c, index)
            new_hall = make_hall_from_cols(new_cols)
            possibilities.add(calculate_new_hall_score(new_hall, hall_score_1))

    possibilities.discard(0)
    assert (
        len(possibilities) == 1
    ), f"Should be exactly one result {possibilities=}\n{hall_score_1=}"
    (new_result,) = possibilities
    result_2 += new_result


print("1:", result_1)
print("2:", result_2)
