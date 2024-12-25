import operator

OPERATORS = {" AND ": operator.__and__, " OR ": operator.__or__, " XOR ": operator.xor}


def operation_performed(oper, key1, key2, target, values):
    if key1 in values and key2 in values:
        values[target] = oper(values[key1], values[key2])
        return True
    return False


def perform_operations(memory, values):
    todo = []
    for operation in memory:
        oper, key1, key2, target = operation
        if not operation_performed(oper, key1, key2, target, values):
            todo.append(operation)
    if todo:
        perform_operations(todo, values)


def parse_input(puzzle):
    puzzle = open(puzzle).read().strip().split("\n")
    values = {}
    memory = []
    parsing_values = True
    for line in puzzle:
        if line == "":
            parsing_values = False
            continue
        if parsing_values:
            gate, value = line.split(": ")
            values[gate] = int(value)
        else:
            operation, target = line.split(" -> ")
            for o in OPERATORS:
                if o in operation:
                    key1, key2 = operation.split(o)
                    memory.append((OPERATORS[o], key1, key2, target))
                    break

    return memory, values


def registry_to_dec(registry, values):
    return sum(
        n[1] * 2**i
        for i, n in enumerate(
            sorted(
                [n for n in values.items() if n[0].startswith(registry)],
                key=lambda a: int(a[0].strip(registry)),
            )
        )
    )


memory, values = parse_input("inputs/24.txt")
perform_operations(memory, values)
print("1:", registry_to_dec("z", values))
