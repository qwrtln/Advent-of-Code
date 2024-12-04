from queue import LifoQueue
from typing import Deque, Dict

from common import read_file


def find_row_with_stacks(puzzle: str) -> int:
    for row, line in enumerate(puzzle.split("\n"), 1):
        chars = [c for c in line]
        if line[1] == "1":
            return row


def find_number_of_stacks(puzzle: str, row: int) -> int:
    line = puzzle.split("\n")[row - 1]
    numbers = line.strip().split(" ")
    while True:
        try:
            numbers.remove("")
        except ValueError:
            break
    return max(int(n) for n in numbers)


def create_stack(puzzle: str, row: int, stack_number: int) -> Deque:
    start_point = row - 2
    line = puzzle.split("\n")[row - 1]
    column = line.find(str(stack_number))
    q = LifoQueue()
    lines = puzzle.split("\n")
    while True:
        try:
            crate = lines[start_point][column]
        except IndexError:
            print(start_point, column)
            return None
        if crate == " ":
            break
        q.put(crate)
        if start_point == 0:
            break
        start_point -= 1
    return q


def perform_stack_movement(stacks: Dict[int, Deque], rule: str) -> None:
    rules = rule.split(" ")
    how_many, from_, to = int(rules[1]), int(rules[3]), int(rules[5])
    stack_from = stacks[from_]
    stack_to = stacks[to]
    crates_to_move = []
    for i in range(how_many):
        crates_to_move.append(stack_from.get())
    for crate in crates_to_move[::-1]:
        stack_to.put(crate)


if __name__ == "__main__":
    puzzle = read_file("05")
    row = find_row_with_stacks(puzzle)
    num_of_stacks = find_number_of_stacks(puzzle, row)
    stacks = {}
    for i in range(1, num_of_stacks + 1):
        stacks[i] = create_stack(puzzle, row, i)

    moves_start = row + 1
    move_rules = puzzle.split("\n")[moves_start:-1]
    for rule in move_rules:
        perform_stack_movement(stacks, rule)

    crates = "".join([s.get() for s in stacks.values()])
    print(crates)
