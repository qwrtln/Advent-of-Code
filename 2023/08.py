import math
import pathlib


def traverse(directions, nodes, current_node):
    steps = 0
    while True:
        for d in directions:
            steps += 1
            current_node = nodes[current_node][("L", "R").index(d)]
            if current_node.endswith("Z"):
                return steps


if __name__ == "__main__":
    puzzle = pathlib.Path("inputs/08.txt").read_text().splitlines(False)

    directions = puzzle[0]
    nodes = {
        key: (dest[:-1].split(", "))
        for key, dest in [l.split(" = (") for l in puzzle[2:]]
    }

    print("1:", traverse(directions, nodes, "AAA"))

    starting_nodes = [n for n in nodes.keys() if n.endswith("A")]
    all_steps = [traverse(directions, nodes, s) for s in starting_nodes]
    print("2:", math.lcm(*all_steps))
