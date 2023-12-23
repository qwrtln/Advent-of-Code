import copy
import queue


puzzle = [line for line in open("inputs/23.txt").read().strip().split("\n")]

HEIGHT = len(puzzle)
WIDTH = len(puzzle[0])


unidirections = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">",
}


def find_manifold(puzzle, y, x):
    manifold = []
    for (yd, xd), turn in unidirections.items():
        yn, xn = y + yd, x + xd
        if puzzle[yn][xn] == turn:
            manifold.append((yn, xn))
    return manifold if len(manifold) == 2 else None


def get_neighbours(puzzle, y, x):
    for (yd, xd), turn in unidirections.items():
        yn, xn = y + yd, x + xd
        if puzzle[y][x] == turn:
            return [(yn, xn)]
    neis = []
    for (yd, xd), turn in unidirections.items():
        yn, xn = y + yd, x + xd
        if puzzle[yn][xn] in (".", turn):
            neis.append((yn, xn))
    return neis


def longest_path(puzzle, start, end):
    visited = set()
    q = queue.Queue()
    q.put((start, [start]))
    while not q.empty():
        current, path = q.get()
        visited.add(current)
        if current == end:
            return len(path) - 1, path

        if manifold := find_manifold(puzzle, *current):
            length_1, path_1 = longest_path(puzzle, manifold[0], end)
            length_2, path_2 = longest_path(puzzle, manifold[1], end)
            if length_1 > length_2:
                return len(path) + length_1, path + path_1
            return len(path) + length_2, path + path_2

        neis = [n for n in get_neighbours(puzzle, *current) if n not in visited]

        for neighbour in neis:
            if neighbour not in visited:
                new_path = copy.copy(path)
                new_path.append(neighbour)
                q.put((neighbour, new_path))

    return visited


start = (0, puzzle[0].index("."))
end = (len(puzzle) - 1, puzzle[-1].index("."))
result, path = longest_path(puzzle, start, end)

print("1:", result)


def draw(puzzle, path):
    result = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            p = (y, x)
            if p in path:
                result += "O"
            else:
                result += puzzle[y][x]
        result += "\n"
    return result


# print(draw(puzzle, path))
