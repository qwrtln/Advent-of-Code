with open("inputs/10.txt") as f:
    maze = [line.strip() for line in f.readlines()]

for y_init, line in enumerate(maze):
    x_init = line.find("S")
    if x_init > -1:
        break

maze_x = len(line)
maze_y = len(maze)
x = x_init
y = y_init


def possible_moves(x, y, direction=False):
    possibilities = []
    if x + 1 < maze_x and maze[y][x] in "S-LF" and maze[y][x + 1] in "-J7S":
        possibilities.append(((x + 1, y), "R"))
    if x > 0 and maze[y][x] in "S-7J" and maze[y][x - 1] in "-LFS":
        possibilities.append(((x - 1, y), "L"))
    if y + 1 < maze_y and maze[y][x] in "S|7F" and maze[y + 1][x] in "|LJS":
        possibilities.append(((x, y + 1), "D"))
    if y > 0 and maze[y][x] in "S|LJ" and maze[y - 1][x] in "|F7S":
        possibilities.append(((x, y - 1), "U"))
    return possibilities if direction else [pos for pos, _ in possibilities]


move1, move2 = possible_moves(x_init, y_init, True)
pos = move2[0]
prev_pos = (x_init, y_init)
dist = 0
loop = [prev_pos]
while pos != (x_init, y_init):
    dist += 1
    loop.append(pos)
    next1, next2 = possible_moves(*pos)
    pos, prev_pos = (next1 if next2 == prev_pos else next2), pos


S_DECODER = {"DU": "|", "RL": "-", "LU": "J", "RU": "L", "LD": "7", "RD": "F"}
maze = [list(line) for line in maze]
maze[y_init][x_init] = S_DECODER[move1[1] + move2[1]]
area = 0
for y, line in enumerate(maze):
    inside = False
    for x, _ in enumerate(line):
        if (x, y) in loop:
            if maze[y][x] in "|LJ":
                inside = not inside
        elif inside:
            # maze[y][x] = 'x'
            area += 1

maze = "\n".join(["".join(line) for line in maze])
# print(maze)
print(area)
