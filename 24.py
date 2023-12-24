import itertools


puzzle = [line for line in open("inputs/24.txt").read().strip().split("\n")]


# X_MIN = Y_MIN = 7
X_MIN = Y_MIN = 200000000000000
# X_MAX = Y_MAX = 27
X_MAX = Y_MAX = 400000000000000

stones = []
for line in puzzle:
    position, velocity = line.split(" @ ")
    pos = [int(p) for p in position.split(", ")]
    v = [int(v) for v in velocity.split(", ")]
    stones.append((pos, v))


def calculate_line(x, y, dx, dy):
    a = dy / dx
    b = y - a * x
    return a, b


def already_crossed(x0, x, dx):
    if dx < 0:
        return x0 > x
    elif dx > 0:
        return x0 < x


result = 0
for i, (s1, s2) in enumerate(itertools.combinations(stones, 2), start=1):
    (x1, y1, _), (dx1, dy1, _) = s1
    (x2, y2, _), (dx2, dy2, _) = s2
    a1, b1 = calculate_line(x1, y1, dx1, dy1)
    a2, b2 = calculate_line(x2, y2, dx2, dy2)
    try:
        x0 = (b2 - b1) / (a1 - a2)
    except ZeroDivisionError:
        continue
    y0 = a1 * x0 + b1
    if (
        X_MIN <= x0 <= X_MAX
        and Y_MIN <= y0 <= Y_MAX
        and not already_crossed(x0, x1, dx1)
        and not already_crossed(x0, x2, dx2)
    ):
        result += 1

print("1:", result)
