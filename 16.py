import enum
import queue


puzzle = [line for line in open("inputs/16.txt").read().strip().split("\n")]

WIDTH = range(len(puzzle[0]))
HEIGHT = range(len(puzzle))


class Direction(enum.Enum):
    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()


VERTICAL = (Direction.UP, Direction.DOWN)
HORIZONTAL = (Direction.RIGHT, Direction.LEFT)

movement = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.RIGHT: (0, 1),
    Direction.LEFT: (0, -1),
}

energized = set()
visited_with_directions = set()

start = (0, 0), Direction.RIGHT
beam = queue.Queue()
beam.put(start)


def find_beam_energy(y, x, direction):
    energized = set()
    visited_with_directions = set()

    start = (y, x), direction
    beam = queue.Queue()
    beam.put(start)

    def enqueue_tile(beam, y, x, direction):
        to_put = (y, x), direction
        if x in WIDTH and y in HEIGHT and to_put not in visited_with_directions:
            visited_with_directions.add(to_put)
            beam.put(to_put)

    while not beam.empty():
        ((y, x), direction) = beam.get()
        tile = puzzle[y][x]
        energized.add((y, x))
        if (
            tile == "."
            or (tile == "|" and direction in VERTICAL)
            or (tile == "-" and direction in HORIZONTAL)
        ):
            yd, xd = movement[direction]
            enqueue_tile(beam, y + yd, x + xd, direction)
        elif tile == "|" and direction in HORIZONTAL:
            enqueue_tile(beam, y + 1, x, Direction.DOWN)
            enqueue_tile(beam, y - 1, x, Direction.UP)
        elif tile == "-" and direction in VERTICAL:
            enqueue_tile(beam, y, x + 1, Direction.RIGHT)
            enqueue_tile(beam, y, x - 1, Direction.LEFT)
        elif tile == "/":
            if direction == Direction.RIGHT:
                enqueue_tile(beam, y - 1, x, Direction.UP)
            elif direction == Direction.DOWN:
                enqueue_tile(beam, y, x - 1, Direction.LEFT)
            elif direction == Direction.UP:
                enqueue_tile(beam, y, x + 1, Direction.RIGHT)
            elif direction == Direction.LEFT:
                enqueue_tile(beam, y + 1, x, Direction.DOWN)
        elif tile == "\\":
            if direction == Direction.RIGHT:
                enqueue_tile(beam, y + 1, x, Direction.DOWN)
            elif direction == Direction.DOWN:
                enqueue_tile(beam, y, x + 1, Direction.RIGHT)
            elif direction == Direction.UP:
                enqueue_tile(beam, y, x - 1, Direction.LEFT)
            elif direction == Direction.LEFT:
                enqueue_tile(beam, y - 1, x, Direction.UP)
        else:
            assert False, "Impossible beam encounter!"
    return len(energized)


print("1:", find_beam_energy(0, 0, Direction.RIGHT))


def get_start_points(puzzle):
    corners = [
        ((0, 0), Direction.RIGHT),
        ((0, 0), Direction.DOWN),
        ((0, len(WIDTH) - 1), Direction.LEFT),
        ((0, len(WIDTH) - 1), Direction.DOWN),
        ((len(HEIGHT) - 1, 0), Direction.UP),
        ((len(HEIGHT) - 1, 0), Direction.RIGHT),
        ((len(HEIGHT) - 1, len(WIDTH) - 1), Direction.LEFT),
        ((len(HEIGHT) - 1, len(WIDTH) - 1), Direction.UP),
    ]
    top = [((0, x), Direction.DOWN) for x in range(1, len(WIDTH))]
    bottom = [((len(HEIGHT) - 1, x), Direction.UP) for x in range(1, len(WIDTH))]
    left = [((y, 0), Direction.RIGHT) for y in range(1, len(HEIGHT))]
    right = [((y, len(WIDTH) - 1), Direction.LEFT) for y in range(1, len(HEIGHT))]
    return [*corners, *top, *bottom, *left, *right]


print(
    "2:",
    max([find_beam_energy(y, x, dir) for ((y, x), dir) in get_start_points(puzzle)]),
)
