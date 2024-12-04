from collections import deque
from string import ascii_lowercase
from typing import List, Tuple


from common import read_file


HEIGHT_SCORES = {letter: i for i, letter in enumerate(ascii_lowercase)}
HEIGHT_SCORES["S"] = 0
HEIGHT_SCORES["E"] = len(ascii_lowercase) - 1


def find_point(puzzle: List[str], point: chr) -> Tuple[int, int]:
    for y, row in enumerate(puzzle):
        if point in row:
            return row.index(point), y


def node_passable(puzzle: List[str], x: int, y: int, x2: int, y2: int) -> bool:
    from_score = HEIGHT_SCORES[puzzle[y][x]]
    to_score = HEIGHT_SCORES[puzzle[y2][x2]]
    # return from_score >= to_score - 1
    return to_score >= from_score - 1


def bfs(puzzle: List[str], start_point: Tuple[int, int]):
    height = len(puzzle)
    width = len(puzzle[0])
    queue = deque([[start_point]])
    seen = set([start_point])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if puzzle[y][x] == "a":
            return path[1:]
        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (
                0 <= x2 < width
                and 0 <= y2 < height
                and (x2, y2) not in seen
                and node_passable(puzzle, x, y, x2, y2)
            ):
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
    return seen


if __name__ == "__main__":

    puzzle = read_file("12").split("\n")[:-1]
    start_point = find_point(puzzle, "S")
    end_point = find_point(puzzle, "E")
    path = bfs(puzzle, end_point)
    print(len(path))
    visited = ""
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if (x, y) == start_point:
                visited += "S"
            elif (x, y) == end_point:
                visited += "E"
            elif (x, y) in path:
                visited += "#"
            else:
                visited += "."
        visited += "\n"
    # print(visited)
