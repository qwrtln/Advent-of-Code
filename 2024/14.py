import collections
import functools
import io
import itertools
from dataclasses import dataclass

from PIL import Image


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

    def move(self, times=1):
        width, height = get_dimentions().values
        self.position.x += self.velocity.x * times
        self.position.y += self.velocity.y * times
        self.position.x %= width
        self.position.y %= height


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


def render(robots):
    image = Image.new("1", get_dimentions().values, color=0)
    pixels = image.load()
    for x, y in ((r.position.x, r.position.y) for r in robots):
        pixels[x, y] = 1
    return image


def calculate_quads(robots):
    quad_count = collections.defaultdict(int)
    for r in robots:
        if quad := assign_robot_to_quad(r):
            quad_count[quad] += 1

    result = 1
    for count in quad_count.values():
        result *= count
    return result


def main():
    puzzle = [line for line in open("inputs/14.txt").read().strip().split("\n")]
    robots = [parse_robot(line) for line in puzzle]

    sizes = 0
    avg_size = 0
    times_to_move = 100
    assumed_entropy = 0.8
    for i in itertools.count(start=1):
        for r in robots:
            r.move()
        if i == times_to_move:
            print("1:", calculate_quads(robots))

        image = render(robots)
        buffer = io.BytesIO()
        image.save(buffer, format="png")
        size = len(buffer.getvalue())
        if i < times_to_move:
            sizes += size
            avg_size = sizes / i
        elif size / avg_size < assumed_entropy:
            print("2:", i)
            break


if __name__ == "__main__":
    main()
