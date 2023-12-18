import shapely


puzzle = [line for line in open("inputs/18.txt").read().strip().split("\n")]


position_1 = position_2 = (0, 0)
points_1 = [position_1]
points_2 = [position_2]
for line in puzzle:
    direction_1, num_1, color = line.split()
    steps_1 = int(num_1)
    y_1, x_1 = position_1
    match direction_1:
        case "R":
            new_point = (y_1, x_1 + steps_1)
        case "L":
            new_point = (y_1, x_1 - steps_1)
        case "U":
            new_point = (y_1 - steps_1, x_1)
        case "D":
            new_point = (y_1 + steps_1, x_1)
    points_1.append(new_point)
    position_1 = new_point

    *num_2, direction_2 = color[2:-1]
    steps_2 = int("".join(num_2), 16)
    direction_2 = {"0": "R", "1": "D", "2": "L", "3": "U"}[direction_2]
    y_2, x_2 = position_2
    match direction_2:
        case "R":
            new_point = (y_2, x_2 + steps_2)
        case "L":
            new_point = (y_2, x_2 - steps_2)
        case "U":
            new_point = (y_2 - steps_2, x_2)
        case "D":
            new_point = (y_2 + steps_2, x_2)
    points_2.append(new_point)
    position_2 = new_point


def calculate_area(points):
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    polygon = shapely.Polygon(points)
    return int(polygon.area + polygon.length / 2 + 1)


print("1:", calculate_area(points_1))
print("2:", calculate_area(points_2))
