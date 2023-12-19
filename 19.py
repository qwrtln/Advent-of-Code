puzzle = open("inputs/19.txt").read().strip()

workflows, parts = puzzle.split("\n\n")
processed_parts = {
    "A": [],
    "R": [],
}


def parse_workflows(raw):
    workflows = {}
    for line in raw:
        index = line.index("{")
        name, rest = line[:index], line[index + 1 : -1]
        workflows[name] = rest.split(",")
    return workflows


def parse_parts(raw):
    parts = []
    for line in raw:
        ratings = line[1:-1].split(",")
        part = {
            category.split("=")[0]: int(category.split("=")[1]) for category in ratings
        }
        parts.append(part)
    return parts


def instruction_satisfied(instruction, part):
    if "<" in instruction:
        to_compare, target = instruction.split(":")
        to_compare = to_compare.split("<")
        label, value = to_compare[0], int(to_compare[1])
        if part[label] < value:
            return True, target
        return False, None
    elif ">" in instruction:
        to_compare, target = instruction.split(":")
        to_compare = to_compare.split(">")
        label, value = to_compare[0], int(to_compare[1])
        if part[label] > value:
            return True, target
        return False, None
    return True, instruction


def parse_instruction(workflow, part):
    for instruction in workflow:
        satisfied, target = instruction_satisfied(instruction, part)
        if satisfied:
            return target
    assert False, f"Unhandled case:\n{workflow=}\n{part=}"


workflows = parse_workflows(workflows.split("\n"))
parts = parse_parts(parts.split("\n"))


for part in parts:
    processed = False
    current_workflow = "in"
    while not processed:
        workflow = workflows[current_workflow]
        current_workflow = parse_instruction(workflow, part)
        if current_workflow in ("A", "R"):
            processed_parts[current_workflow].append(part)
            processed = True
            current_workflow = "in"

result_1 = 0
for part in processed_parts["A"]:
    for v in part.values():
        result_1 += v
print("1:", result_1)
