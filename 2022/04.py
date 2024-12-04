from typing import Set


from common import read_file


def make_set(elf: str) -> Set[int]:
    start, end = [int(e) for e in elf.split("-")]
    return set(range(start, end + 1))


if __name__ == "__main__":
    puzzle = read_file("04").split("\n")[:-1]
    subsets = 0
    for line in puzzle:
        elf1, elf2 = [make_set(e) for e in line.split(",")]
        if elf1 & elf2:
            subsets += 1
    print(subsets)
