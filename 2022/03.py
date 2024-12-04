from string import ascii_letters


from common import read_file


PRIORITIES = {l: i for i, l in enumerate(ascii_letters, 1)}


if __name__ == "__main__":
    puzzle = read_file("03").split("\n")[:-1]
    score = 0
    groups = len(puzzle) // 3
    for i in range(groups):
        bp1, bp2, bp3 = puzzle[i * 3], puzzle[i * 3 + 1], puzzle[i * 3 + 2]
        common = next(iter(set(bp1) & set(bp2) & set(bp3)))
        score += PRIORITIES[common]
    print(score)
