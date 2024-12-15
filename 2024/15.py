# Benchmark: CPython (3.12.7)
#  Time (mean ± σ):      93.7 ms ±   5.0 ms    [User: 82.2 ms, System: 11.1 ms]
#  Range (min … max):    89.1 ms … 106.6 ms    31 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     202.9 ms ±  13.1 ms    [User: 177.4 ms, System: 25.6 ms]
#   Range (min … max):   192.5 ms … 241.8 ms    15 runs
#
import bisect
import collections
import queue

DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def parse_puzzle(file):
    puzzle = open(file).read().strip().split("\n")
    warehouse = []
    robot = (0, 0)
    index = 0
    for i, line in enumerate(puzzle, start=1):
        if "@" in line:
            robot = (index, line.index("@"))
            warehouse.append(list(line.replace("@", ".")))
        elif line != "":
            warehouse.append(list(line))
        else:
            index = i
            break
    movements = []
    for line in puzzle[index:]:
        movements.extend(list(line))
    return warehouse, movements, robot


def handle_movement(robot, movement, warehouse):
    dy, dx = DIRECTIONS[movement]
    r_y, r_x = robot
    y_n, x_n = r_y + dy, r_x + dx
    if warehouse[y_n][x_n] == ".":
        return (y_n, x_n)
    elif warehouse[y_n][x_n] == "#":
        return robot
    else:
        y_first, x_first = (y_n, x_n)
        while warehouse[y_n][x_n] == "O":
            y_n, x_n = y_n + dy, x_n + dx
        if warehouse[y_n][x_n] == "#":
            return robot
        warehouse[y_n][x_n] = "O"
        warehouse[y_first][x_first] = "."
        return (y_first, x_first)


def parse_widened_puzzle(file):
    puzzle = open(file).read().strip().split("\n")
    warehouse = []
    index = 0
    movements = []
    for y in range(len(puzzle)):
        line = []
        if puzzle[y] == "":
            index = y + 1
            break
        for x in range(len(puzzle[y])):
            if puzzle[y][x] == ".":
                line.extend([".", "."])
            elif puzzle[y][x] == "#":
                line.extend(["#", "#"])
            elif puzzle[y][x] == "@":
                line.extend(["@", "."])
            elif puzzle[y][x] == "O":
                line.extend(["[", "]"])
        warehouse.append(line)

    for line in puzzle[index:]:
        movements.extend(list(line))

    def find_robot(warehouse):
        for y in range(len(warehouse)):
            for x in range(len(warehouse[y])):
                if warehouse[y][x] == "@":
                    warehouse[y][x] = "."
                    return (y, x)

    return warehouse, movements, find_robot(warehouse)


def get_full_box(y, x, part):
    if part == "[":
        return (y, x), (y, x + 1)
    return (y, x - 1), (y, x)


def find_boxes_to_move(y, x, movement, warehouse):
    box = get_full_box(y, x, warehouse[y][x])
    boxes = set()
    q = queue.Queue()
    q.put(box)
    while not q.empty():
        box = q.get()
        boxes.add(box)
        new_coords = []
        if movement in "<>":
            dy, dx = {"<": (0, -1), ">": (1, 1)}[movement]
            y_n, x_n = box[dy][0], box[dy][1] + dx
            if warehouse[y_n][x_n] in "[]":
                new_coords.append((y_n, x_n))
        elif movement in "^v":
            dy = {"^": -1, "v": 1}[movement]
            for y, x in box:
                y_n, x_n = y + dy, x
                if warehouse[y_n][x_n] in "[]":
                    new_coords.append((y_n, x_n))
        for y, x in new_coords:
            q.put(get_full_box(y, x, warehouse[y][x]))
    return boxes


def are_boxes_movable(boxes, movement, warehouse):
    edge_indices = collections.defaultdict(list)
    dy, dx, reverse = {
        "^": (-1, 0, 1),
        "v": (1, 0, -1),
        "<": (0, -1, 1),
        ">": (0, 1, -1),
    }[movement]
    if dy != 0:
        for box in boxes:
            for y, x in box:
                bisect.insort(edge_indices[x], y)
        for x, col in edge_indices.items():
            for y in col[::reverse]:
                if y + dy not in col:
                    if warehouse[y + dy][x] != ".":
                        return False
    else:
        for box in boxes:
            for y, x in box:
                bisect.insort(edge_indices[y], x)
        for y, col in edge_indices.items():
            for x in col[::reverse]:
                if x + dx not in col:
                    if warehouse[y][x + dx] != ".":
                        return False
    return True


def move_boxes(boxes, movement, warehouse):
    for box in boxes:
        for y, x in box:
            warehouse[y][x] = "."
    dy, dx = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}[movement]
    for box in boxes:
        (y_1, x_1), (y_2, x_2) = box
        warehouse[y_1 + dy][x_1 + dx] = "["
        warehouse[y_2 + dy][x_2 + dx] = "]"


def handle_widened_movement(robot, movement, warehouse):
    dy, dx = DIRECTIONS[movement]
    r_y, r_x = robot
    y_n, x_n = r_y + dy, r_x + dx
    if warehouse[y_n][x_n] == ".":
        return (y_n, x_n)
    elif warehouse[y_n][x_n] == "#":
        return robot
    else:
        boxes_cluster = find_boxes_to_move(y_n, x_n, movement, warehouse)
        if are_boxes_movable(boxes_cluster, movement, warehouse):
            move_boxes(boxes_cluster, movement, warehouse)
            return (y_n, x_n)
        return robot


def calculate_result(warehouse, box):
    result = 0
    for y in range(len(warehouse)):
        for x in range(len(warehouse[y])):
            if warehouse[y][x] == box:
                result += 100 * y + x
    return result


def solve_part_1(file):
    warehouse, movements, robot = parse_puzzle(file)
    for m in movements:
        robot = handle_movement(robot, m, warehouse)
    return calculate_result(warehouse, "O")


def solve_part_2(file):
    warehouse, movements, robot = parse_widened_puzzle(file)
    for m in movements:
        robot = handle_widened_movement(robot, m, warehouse)
    return calculate_result(warehouse, "[")


if __name__ == "__main__":
    print("1:", solve_part_1("inputs/15.txt"))
    print("2:", solve_part_2("inputs/15.txt"))
