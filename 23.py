import copy
import queue
import time
import os


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
    # for (yd, xd), turn in unidirections.items():
    #     yn, xn = y + yd, x + xd
    #     if puzzle[y][x] == turn:
    #         return [(yn, xn)]
    neis = []
    for (yd, xd), turn in unidirections.items():
        yn, xn = y + yd, x + xd
        if puzzle[yn][xn] in (".", *list(unidirections.values())):
            neis.append((yn, xn))
    return neis


def longest_path(puzzle, start, end, visited=None):
    if visited is None:
        visited = set()

    q = queue.Queue()
    q.put((start, [start]))
    while not q.empty():
        current, path = q.get()
        visited.add(current)
        if current == end:
            # print(f"{path=}")
            return len(path) - 1, path

        neis = [n for n in get_neighbours(puzzle, *current) if n not in visited]
        # assert len(neis) in (1, 2, 3), f"Must have 1, 2 or 3 neis! {len(neis)}"
        if len(neis) > 1:
            sublength, subpath = max(
                [longest_path(puzzle, n, end, visited) for n in neis]
            )
            return len(path) + sublength, path + subpath
        elif len(neis) == 1:
            neighbour = neis[0]
            new_path = copy.copy(path)
            new_path.append(neighbour)
            q.put((neighbour, new_path))
        else:
            print(f"Dead end! {len(path)=} {len(visited)=}")
            return 0, []

    return visited


start = (0, puzzle[0].index("."))
end = (len(puzzle) - 1, puzzle[-1].index("."))
result, path = longest_path(puzzle, start, end)

print("2:", result)
HIGH = 9364
LOWW = 5140


def draw(puzzle, path):
    GREEN = "\033[31m"
    BASE = "\033[0m"
    result = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            p = (y, x)
            if p in path:
                last_y = y
                last_x = x
                result += GREEN + "O" + BASE
                # result += "O"
            else:
                result += puzzle[y][x]
        result += "\n"
    # r = result.split("\n")
    # return "\n".join(r[last_y - 30:last_y+30]), last_y, last_x
    return result


print(draw(puzzle, path))

# for i in range(3355, len(path) + 1):
#     d, y, x = draw(puzzle, [path[i]])
#     print(d)
#     input(f"Step {i}, ({y}, {x})")
#     # time.sleep(0.1)
#     os.system("clear")


assert LOWW < result < HIGH
