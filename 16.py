import enum
import queue


puzzle = [line for line in open("inputs/16.txt").read().strip().split("\n")]

WIDTH = range(len(puzzle[0]))
HEIGHT = range(len(puzzle))


class Direction(enum.StrEnum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"


VERTICAL = (Direction.UP, Direction.DOWN)
HORIZONTAL = (Direction.RIGHT, Direction.LEFT)

movement = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "RIGHT": (0, 1),
    "LEFT": (0, -1),
}

energized = set()
visited_with_directions = set()

start = (0, 0), Direction.RIGHT
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
            # enqueue_tile(beam, y - 1, x, Direction.UP)
        elif direction == Direction.DOWN:
            enqueue_tile(beam, y, x + 1, Direction.RIGHT)
            # enqueue_tile(beam, y, x - 1, Direction.LEFT)
        elif direction == Direction.UP:
            enqueue_tile(beam, y, x - 1, Direction.LEFT)
            # enqueue_tile(beam, y, x + 1, Direction.RIGHT)
        elif direction == Direction.LEFT:
            enqueue_tile(beam, y - 1, x, Direction.UP)
            # enqueue_tile(beam, y + 1, x, Direction.DOWN)
    else:
        assert False, "Impossible beam encounter!"


print("1:", len(energized))
