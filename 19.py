puzzle = open("inputs/19-sample.txt").read().strip()

workflows, parts = puzzle.split("\n\n")

MIN = 1
MAX = 4001


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


def parse_part_1(parts, workflows):
    successes = []
    for part in parts:
        processed = False
        current_workflow = "in"
        while not processed:
            workflow = workflows[current_workflow]
            current_workflow = parse_instruction(workflow, part)
            if current_workflow == "A":
                successes.append(part)
            if current_workflow in ("A", "R"):
                processed = True
                current_workflow = "in"

    result = 0
    for part in successes:
        for v in part.values():
            result += v
    return result


workflows = parse_workflows(workflows.split("\n"))
parts = parse_parts(parts.split("\n"))

# print("1:", parse_part_1(parts, workflows))

from pprint import pprint
# pprint(workflows)


def parse_condition(condition):
    if ">" in condition:
        rating, score = condition.split(">")
        return {rating: range(int(score) + 1, MAX)}
    elif "<" in condition:
        rating, score = condition.split("<")
        return {rating: range(MIN, int(score))}


def find_paths_to_success(label, workflows):
    print(f"Func start! {label=}")
    instructions = workflows[label]
    print(instructions)

    paths = []
    current_path = {label: []}
    print(f"{current_path=}:")
    for index, instr in enumerate(instructions):
        if "A" in instr:
            if len(instr) > 1:
                condition, _ = instr.split(":")
                current_path[label].append(parse_condition(condition))
            else:
                current_path[label] = {True}
        elif ":" in instr:
            condition, new_label = instr.split(":")
            parsed_condition = parse_condition(condition)
            current_path[label].append(
                parsed_condition.update(find_paths_to_success(new_label, workflows))
            )
        elif "R" in instr:
            pass  # TBC

    pprint(current_path)
    input()
    return current_path


for label in workflows:
    find_paths_to_success(label, workflows)
