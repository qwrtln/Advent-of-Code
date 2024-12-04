from common import read_file

if __name__ == "__main__":

    puzzle_input = read_file("01")
    elves = [e for e in puzzle_input.split("\n\n") if e]
    calories_carried = []
    for elf in elves:
        calories = [int(c) for c in elf.split("\n")]
        calories_carried.append(sum(calories))
    print(sum(sorted(calories_carried)[-3:]))
