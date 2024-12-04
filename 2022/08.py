from enum import Enum
from typing import List, Set, Tuple


from common import read_file


class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


def find_edge_points(
    coordinate: int, direction: Direction, edge_size: int
) -> Tuple[Tuple[int, int], int, int, int]:
    if direction == Direction.RIGHT:
        initial_max_height = (coordinate, 0)
        start_point = 1
        end_point = edge_size - 1
        step = 1
    elif direction == Direction.LEFT:
        initial_max_height = (coordinate, -1)
        start_point = edge_size - 1
        end_point = 0
        step = -1
    elif direction == Direction.DOWN:
        initial_max_height = (0, coordinate)
        start_point = 1
        end_point = edge_size - 1
        step = 1
    elif direction == Direction.UP:
        initial_max_height = (-1, coordinate)
        start_point = edge_size - 1
        end_point = 0
        step = -1
    return initial_max_height, start_point, end_point, step


def find_visible_trees_in_row(
    puzzle: List[str], row: int, direction: Direction
) -> Set[Tuple[int, int]]:
    trees_visible = set()

    initial_max_size, start_point, end_point, step = find_edge_points(
        row, direction, len(puzzle)
    )
    max_size_row, max_size_col = initial_max_size

    max_height = int(puzzle[max_size_row][max_size_col])
    for i in range(start_point, end_point, step):
        current_height = int(puzzle[row][i])
        if current_height > max_height:
            trees_visible.add((row, i))
            max_height = current_height

    return trees_visible


def find_visible_trees_in_col(
    puzzle: List[str], col: int, direction: Direction
) -> Set[Tuple[int, int]]:
    trees_visible = set()

    initial_max_size, start_point, end_point, step = find_edge_points(
        col, direction, len(puzzle)
    )
    max_size_row, max_size_col = initial_max_size

    max_height = int(puzzle[max_size_row][max_size_col])
    for i in range(start_point, end_point, step):
        current_height = int(puzzle[i][col])
        if current_height > max_height:
            trees_visible.add((i, col))
            max_height = current_height

    return trees_visible


def calculate_tree_score(coordinates: Tuple[int, int], puzzle: List[str]) -> int:
    left, right, up, down = 1, 1, 1, 1
    row, col = coordinates
    height = int(puzzle[row][col])
    for i in range(col + 1, len(puzzle)):
        if int(puzzle[row][i]) >= height or i == len(puzzle) - 1:
            break
        right += 1
    for i in range(col - 1, -1, -1):
        if int(puzzle[row][i]) >= height or i == 0:
            break
        left += 1
    for i in range(row + 1, len(puzzle)):
        if int(puzzle[i][col]) >= height or i == len(puzzle) - 1:
            break
        down += 1
    for i in range(row - 1, -1, -1):
        if int(puzzle[i][col]) >= height or i == 0:
            break
        up += 1
    return left * right * up * down


if __name__ == "__main__":
    puzzle = read_file("08").split("\n")[:-1]
    visible_count = 4 * (len(puzzle) - 1)

    visible_trees = set()

    for coordinate in range(1, len(puzzle) - 1):
        visible_trees.update(
            find_visible_trees_in_row(puzzle, coordinate, Direction.LEFT)
        )
        visible_trees.update(
            find_visible_trees_in_row(puzzle, coordinate, Direction.RIGHT)
        )
        visible_trees.update(
            find_visible_trees_in_col(puzzle, coordinate, Direction.UP)
        )
        visible_trees.update(
            find_visible_trees_in_col(puzzle, coordinate, Direction.DOWN)
        )

    max_score = 0
    for tree in visible_trees:
        score = calculate_tree_score(tree, puzzle)
        row, col = tree
        max_score = score if score > max_score else max_score
    print(max_score)
