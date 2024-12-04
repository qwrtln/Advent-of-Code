import itertools
import sys
import time

from typing import Tuple, List


from common import read_file


class Head:
    x: int
    y: int
    name: str

    def __init__(self, name: str) -> None:
        self.x = 0
        self.y = 0
        self.name = name

    def move(self, direction: chr) -> None:
        match direction:
            case "R":
                self.y += 1
            case "L":
                self.y -= 1
            case "U":
                self.x += 1
            case "D":
                self.x -= 1

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def __sub__(self, head: "Head") -> Tuple[int, int]:
        return self.x - head.x, self.y - head.y


NO_MOVE_DIFFS = list(itertools.product([-1, 0, 1], repeat=2))


class Tail(Head):
    def follow_head(self, head: Head) -> None:
        dx, dy = head - self
        if (dx, dy) in NO_MOVE_DIFFS:
            return
        elif dx == 0:
            self.y += dy // 2
        elif dy == 0:
            self.x += dx // 2
        elif abs(dx) == 1:
            self.x += dx
            self.y += dy // 2
        elif abs(dy) == 1:
            self.y += dy
            self.x += dx // 2
        elif abs(dx) == abs(dy) == 2:
            self.x += dx // 2
            self.y += dy // 2
        else:
            input(f"ERROR!!! ILLEGAL POSITION: {dx=} {dy=} {self.name=} {head.name=}")


def print_position(knots: List[Head]) -> None:
    board_size = 30
    templates = []
    positions = {}
    for tail in knots[1:]:
        positions[tail.position] = tail.name
    positions[knots[0].position] = knots[0].name

    for row in range(-board_size, board_size):
        template = ""
        for col in range(-board_size, board_size):
            next_symbol = "."
            if (row, col) in positions:
                next_symbol = positions[(row, col)]
            template += next_symbol
        templates.append(template)

    print("\n".join(templates[::-1]), end="\r")


def move_knots(knots: List[Head], direction: str) -> None:
    knots[0].move(direction)
    current_tail = knots[0]
    for tail in knots[1:]:
        tail.follow_head(current_tail)
        current_tail = tail


if __name__ == "__main__":
    puzzle = read_file("09b").split("\n")[:-1]
    knots = [Head("H")]
    knots += [Tail(str(i + 1)) for i in range(9)]
    visited_positions = set([knots[-1].position])
    visualize = False
    try:
        if sys.argv[1]:
            visualize = True
    except IndexError:
        pass
    for index, line in enumerate(puzzle):
        direction, times = line.split(" ")
        for i in range(int(times)):
            move_knots(knots, direction)
            visited_positions.add(knots[-1].position)
            if visualize:
                print_position(knots)
                time.sleep(0.2)
    print(len(visited_positions))
