from common import get_puzzle


def traverse(directions, nodes):
    steps = 0
    current_node = "AAA"
    while True:
        for direction in directions:
            steps += 1
            to_go = 1 if direction == "R" else 0
            current_node = nodes[current_node][to_go]
            if current_node == "ZZZ":
                return steps


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    directions = puzzle[0]
    nodes = {}
    for line in puzzle[2:]:
        key, dest = line.split(" = (")
        p1, p2 = dest[:-1].split(", ")
        nodes[key] = (p1, p2)

    print(traverse(directions, nodes))
