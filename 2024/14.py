import collections
import functools
from dataclasses import dataclass


@dataclass
class Velocity:
    x: int
    y: int


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Robot:
    position: Position
    velocity: Velocity


@dataclass
class _Dimentions:
    width: int
    height: int

    @property
    def values(self):
        return self.width, self.height

    @property
    def quads(self):
        return self.width // 2, self.height // 2


@functools.lru_cache(maxsize=1)
def get_dimentions():
    return _Dimentions(0, 0)


def parse_values(values):
    x, y = values[2:].split(",")
    return int(x), int(y)


def parse_robot(line):
    position_line, velocity_line = line.split(" ")
    velocity = Velocity(*parse_values(velocity_line))
    position = Position(*parse_values(position_line))
    dimentions = get_dimentions()
    if position.x + 1 > dimentions.width:
        dimentions.width = position.x + 1
    if position.y + 1 > dimentions.height:
        dimentions.height = position.y + 1
    return Robot(position, velocity)


def move_robot(robot, times):
    width, height = get_dimentions().values
    robot.position.x += robot.velocity.x * times
    robot.position.y += robot.velocity.y * times
    robot.position.x %= width
    robot.position.y %= height


def assign_robot_to_quad(robot):
    quad_x, quad_y = get_dimentions().quads
    if robot.position.x < quad_x and robot.position.y < quad_y:
        return 1
    if robot.position.x > quad_x and robot.position.y < quad_y:
        return 2
    if robot.position.x > quad_x and robot.position.y > quad_y:
        return 3
    if robot.position.x < quad_x and robot.position.y > quad_y:
        return 4


def main():
    puzzle = [line for line in open("inputs/14.txt").read().strip().split("\n")]
    robots = [parse_robot(line) for line in puzzle]

    times_to_move = 100
    for r in robots:
        move_robot(r, times_to_move)

    quad_count = collections.defaultdict(int)
    for r in robots:
        if quad := assign_robot_to_quad(r):
            quad_count[quad] += 1

    result = 1
    for count in quad_count.values():
        result *= count
    print("1:", result)


if __name__ == "__main__":
    main()
