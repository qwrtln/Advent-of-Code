import queue

puzzle = [line for line in open("inputs/21.txt").read().strip().split("\n")]

HEIGHT = len(puzzle)
WIDTH = len(puzzle[0])

def find_start(puzzle):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if puzzle[y][x] == "S":
                return (y, x)


def get_neighbours(puzzle, y, x):
    for yd, xd in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yn, xn = y + yd, x + xd
        if 0 <= yn < HEIGHT and 0 <= xn < WIDTH and puzzle[yn][xn] != "#":
            yield (yn, xn)


def bfs(puzzle, start, limit):
    frontier = queue.Queue()
    distance_map = {start: 0}

    frontier.put((start, 0))
    while not frontier.empty():
        current, distance = frontier.get()
        for neighbour in get_neighbours(puzzle, *current):
            if neighbour not in distance_map and distance < limit:
                distance_map[neighbour] = distance + 1
                frontier.put((neighbour, distance + 1))
    return distance_map

    
start = find_start(puzzle)
distance_map = bfs(puzzle, start, 64)
print("1:", len([v for v in distance_map.values() if v % 2 == 0]))

# def visualise(distance_map, puzzle):
#     result = ""
#     for y in range(HEIGHT):
#         for x in range(WIDTH):
#             if (y, x) in distance_map and distance_map[(y, x)] % 2 == 0:
#                 result += "O"
#             else:
#                 result += puzzle[y][x]
#         result += "\n"
#     return result
#
# print(visualise(distance_map, puzzle))
