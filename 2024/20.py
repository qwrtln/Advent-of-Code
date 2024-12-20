# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     54.190 s ±  0.148 s    [User: 54.049 s, System: 0.046 s]
#   Range (min … max):   53.948 s … 54.424 s    10 runs
#
puzzle = [list(line) for line in open("inputs/20.txt").read().strip().split("\n")]


WIDTH = len(puzzle[0])
HEIGHT = len(puzzle)

start, end = (0, 0), (0, 0)
for y in range(WIDTH):
    for x in range(HEIGHT):
        if puzzle[y][x] == "S":
            start = (y, x)
        elif puzzle[y][x] == "E":
            end = (y, x)


def find_path(start, end, puzzle):
    current = start
    path = [start]
    while True:
        y, x = current
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if 1 <= y + dy < HEIGHT - 1 and 1 <= x + dx < WIDTH - 1:
                if puzzle[y + dy][x + dx] != "#" and (y + dy, x + dx) not in path:
                    current = (y + dy, x + dx)
                    path.append(current)
                    if current == end:
                        return path[1:]


def enable_cheat_mode(path, start, puzzle, *, radius=2):
    y, x = start
    targets = []
    cheats = set()
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if abs(dx) + abs(dy) <= radius:
                y_n, x_n = y + dy, x + dx
                if (
                    1 <= y + dy < HEIGHT - 1
                    and 1 <= x + dx < WIDTH - 1
                    and puzzle[y_n][x_n] in ".E"
                    and (y_n, x_n) != (y, x)
                ):
                    targets.append((y_n, x_n))

    for target in targets:
        skip_start = path.index(start)
        skip_end = path.index(target)
        y_2, x_2 = target
        new_path_length = (
            len(path[:skip_start])
            + len(path[skip_end + 1 :])
            + abs(y_2 - y)
            + abs(x_2 - x)
        )
        new_cheat = (new_path_length, start, target)
        if len(path) - new_path_length > 0 and new_cheat not in cheats:
            cheats.add(new_cheat)
            yield new_cheat


def find_cheats_saving(path, point, puzzle, threshold=100, *, radius=2):
    result = 0
    for cheat in enable_cheat_mode(path, point, puzzle, radius=radius):
        new_len, *_ = cheat
        saved = len(path) - new_len
        if saved >= threshold:
            result += 1
    return result


result_1 = 0
result_2 = 0
path = [start, *find_path(start, end, puzzle)]
for point in path:
    result_1 += find_cheats_saving(path, point, puzzle)
    result_2 += find_cheats_saving(path, point, puzzle, radius=20)

print("1:", result_1)
print("2:", result_2)
