import collections


puzzle = [line for line in open("inputs/17.txt").read().strip().split("\n")]

GRAPH = [[int(d) for d in row] for row in puzzle]
# for row in puzzle:
#     GRAPH.append([int(d) for d in row])

INFINITY = 999999999
<<<<<<< HEAD
LEFT = "L"
DOWN = "D"
RIGHT = "R"
UP = "U"
DIRECTIONS = {
    # direction: (dy, dx)
    LEFT: (0, -1),
    DOWN: (1, 0),
    RIGHT: (0, 1),
    UP: (-1, 0),
}
OPPOSITES = {
    frozenset([LEFT, RIGHT]),
    frozenset([UP, DOWN]),
=======
LEFT = 'L'
DOWN = 'D'
RIGHT = 'R'
UP = 'U'
DIRECTIONS = {
	# direction: (dy, dx)
	LEFT:  ( 0, -1),
	DOWN:  ( 1,  0),
	RIGHT: ( 0,  1),
	UP:    (-1,  0),
}
OPPOSITES = {
	frozenset([LEFT, RIGHT]),
	frozenset([UP, DOWN]),
>>>>>>> 29da3a6 (Add Milo's solution to day 17)
}
STEP_LIMIT = 3


def neighbors(y, x, direction, steps):
<<<<<<< HEAD
    for neighbor_direction, (dy, dx) in DIRECTIONS.items():
        ny, nx = y + dy, x + dx

        if frozenset([direction, neighbor_direction]) in OPPOSITES:
            continue
        if not 0 <= ny < len(GRAPH):
            continue
        if not 0 <= nx < len(GRAPH[0]):
            continue

        neighbor_steps = 1
        if direction == neighbor_direction:
            if steps >= STEP_LIMIT:
                continue
            neighbor_steps = steps + 1

        yield ny, nx, neighbor_direction, neighbor_steps


def core():
    Y0 = X0 = 0
    DIRECTION0 = STEPS0 = None

    cost = collections.defaultdict(lambda: INFINITY)
    cost[(Y0, X0, DIRECTION0, STEPS0)] = 0

    to_visit = {(Y0, X0, DIRECTION0, STEPS0)}

    while to_visit:
        coords = to_visit.pop()
        y, x, direction, steps = coords

        for neighbor_coords in neighbors(*coords):
            ny, nx, _, _ = neighbor_coords
            cost_candidate = cost[coords] + GRAPH[ny][nx]
            if cost_candidate < cost[neighbor_coords]:
                cost[neighbor_coords] = cost_candidate
                to_visit.add(neighbor_coords)

    Y1, X1 = len(GRAPH) - 1, len(GRAPH[0]) - 1
    print(
        min(
            cost[Y1, X1, direction, steps]
            for direction in DIRECTIONS
            for steps in range(max(len(GRAPH), len(GRAPH[0])))
        )
    )


if __name__ == "__main__":
    core()
    # STEP_LIMIT = 1
    # core()
    # STEP_LIMIT = INFINITY
    # core()
=======
	for neighbor_direction, (dy, dx) in DIRECTIONS.items():
		ny, nx = y + dy, x + dx
		
		if frozenset([direction, neighbor_direction]) in OPPOSITES:
			continue
		if not 0 <= ny < len(GRAPH):
			continue
		if not 0 <= nx < len(GRAPH[0]):
			continue
		
		neighbor_steps = 1
		if direction == neighbor_direction:
			if steps >= STEP_LIMIT:
				continue
			neighbor_steps = steps + 1
			
		yield ny, nx, neighbor_direction, neighbor_steps


def core():
	Y0 = X0 = 0
	DIRECTION0 = STEPS0 = None
	
	cost = collections.defaultdict(lambda: INFINITY)
	cost[(Y0, X0, DIRECTION0, STEPS0)] = 0
	
	to_visit = {(Y0, X0, DIRECTION0, STEPS0)}
	
	while to_visit:
		coords = to_visit.pop()
		y, x, direction, steps = coords
		
		for neighbor_coords in neighbors(*coords):
			ny, nx, _, _ = neighbor_coords
			cost_candidate = cost[coords] + GRAPH[ny][nx]
			if cost_candidate < cost[neighbor_coords]:
				cost[neighbor_coords] = cost_candidate
				to_visit.add(neighbor_coords)
	
	Y1, X1 = len(GRAPH) - 1, len(GRAPH[0]) - 1
	print(min(
		cost[Y1, X1, direction, steps]
		for direction in DIRECTIONS
		for steps in range(max(len(GRAPH), len(GRAPH[0])))
	))


if __name__ == "__main__":
	core()
	# STEP_LIMIT = 1
	# core()
	# STEP_LIMIT = INFINITY
	# core()
>>>>>>> 29da3a6 (Add Milo's solution to day 17)
