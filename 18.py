import operator

puzzle = [line for line in open("inputs/18.txt").read().strip().split("\n")]

vert_dict = {
    "R": "-",#"→",
    "L": "-",#"←",
    "U": "|",#"↑",
    "D": "|",#"↓",
}

diag_dict = {
    "RD": "7",#"↘",
    "DR": "L",#"↘",
    "RU": "J",#"↗",
    "UR": "F",#"↗",
    "LU": "L",#"↖",
    "UL": "7",#"↖",
    "LD": "F",#"↙",
    "DL": "J",#"↙",
}

position = (0, 0)
dug = {}
last_dir = None
for line in puzzle:
    d, num, color = line.split()
    steps = int(num)
    y, x = position
    for i in range(1, steps + 1):
        if last_dir and i == 1:
            dug[*position] = diag_dict[f"{last_dir}{d}"]
        match d:
            case "R":
                dug[(y, x + i)] = vert_dict[d]
                position = (y, x + i)
            case "L":
                dug[(y, x - i)] = vert_dict[d]
                position = (y, x - i)
            case "U":
                dug[(y - i, x)] = vert_dict[d]
                position = (y - i, x)
            case "D":
                dug[(y + i, x)] = vert_dict[d]
                position = (y + i, x)
    last_dir = d


dug[(0, 0)] = diag_dict["UR"]  # Magic!
d = dug.keys()
min_y = min(d)[0]
max_y = max(d)[0]
min_x = min(d, key=operator.itemgetter(1))[1]
max_x = max(d, key=operator.itemgetter(1))[1]

changing_turns = {
    "F": "J",
    "L": "7",
}

in_trench = 0
points_in = set()
# https://en.wikipedia.org/wiki/Scanline_rendering
for y in range(min_y, max_y + 1):
    inside = False
    last_corner = None
    for x in range(min_x, max_x + 1):
        if (y, x) not in dug and inside:
            points_in.add((y, x))
            in_trench += 1
        elif (y, x) in dug:
            char = dug[(y, x)]
            if char == "|":
                inside = not inside
            elif char in changing_turns:
                last_corner = char
            elif last_corner and char == changing_turns[last_corner]:
                inside = not inside

trench = ""
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if (y, x) in dug:
            trench += dug[(y, x)]
        elif (y, x) in points_in:
            trench += "d"
        else:
            trench += "."
    trench += "\n"
# print(trench)
print(len(dug) + in_trench)
