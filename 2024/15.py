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
    for index, line in enumerate(puzzle):
        if "@" in line:
            robot = (index, line.index("@"))
            warehouse.append(list(line.replace("@", ".")))
        elif line != "":
            warehouse.append(list(line))
        else:
            index += 1
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
        return (y_n, x_n), warehouse
    elif warehouse[y_n][x_n] == "#":
        return robot, warehouse
    else:
        potentially_movable = []
        while warehouse[y_n][x_n] == "O":
            potentially_movable.append((y_n, x_n))
            y_n, x_n = y_n + dy, x_n + dx
        if warehouse[y_n][x_n] == "#":
            return robot, warehouse
        y_first, x_first = potentially_movable[0]
        robot = (y_first, x_first)
        warehouse[y_n][x_n] = "O"
        warehouse[y_first][x_first] = "."
        return robot, warehouse


def plot_warehouse(warehouse, robot, last_movement=None):
    if last_movement:
        print("Last movement:", last_movement)
    result = ""
    for y in range(len(warehouse)):
        for x in range(len(warehouse[y])):
            if (y, x) == robot:
                result += "@"
            else:
                result += warehouse[y][x]
        result += "\n"
    print(result)


def calculate_result(warehouse, box):
    result = 0
    for y in range(len(warehouse)):
        for x in range(len(warehouse[y])):
            if warehouse[y][x] == box:
                result += 100 * y + x
    return result


def main():
    warehouse, movements, robot = parse_puzzle("inputs/15.txt")

    for m in movements:
        robot, warehouse = handle_movement(robot, m, warehouse)
        # plot_warehouse(warehouse, robot, m)
    result_1 = calculate_result(warehouse, "O")
    print("1:", result_1)


if __name__ == "__main__":
    main()
