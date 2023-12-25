import itertools

import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D


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


min_x = min(stones, key=lambda x: x[0][0])[0][0]
min_y = min(stones, key=lambda x: x[0][1])[0][1]
min_z = min(stones, key=lambda x: x[0][2])[0][2]

max_x = max(stones, key=lambda x: x[0][0])[0][0]
max_y = max(stones, key=lambda x: x[0][1])[0][1]
max_z = max(stones, key=lambda x: x[0][2])[0][2]

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
for i, s in enumerate(stones, start=1):
    (x, y, z), (dx, dy, dz) = s
    x -= min_x
    y -= min_y
    z -= min_z

    x /= max_x
    y /= max_y
    z /= max_z

    # dx /= max_x
    # dy /= max_y
    # dz /= max_z

    print(dx)

    print(f"Plotting {i}...")

    # ax = fig.add_subplot(projection='3d')
    x = np.linspace(x, x + 11 * dx, 10)
    y = np.linspace(y, y + 11 * dy, 10)
    z = np.linspace(z, z + 11 * dz, 10)
    for a in x:
        print(a)
    ax.plot(x, y, z, label=f"{i}")
    # ax.legend()

    # input("Give me one better")
# plt.axis("off")
plt.show()
