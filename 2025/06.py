import operator

puzzle = [line for line in open("inputs/06.txt").read().split("\n")][:-1]

OPERATION_MAP = {
    "*": operator.mul,
    "+": operator.add,
}

OPERATIONS = [OPERATION_MAP[o] for o in puzzle[-1].strip().split(" ") if o]


def left_to_right(puzzle):
    cols = [1 if OPERATIONS[i] == operator.mul else 0 for i in range(len(OPERATIONS))]
    for line in puzzle[:-1]:
        numbers = [int(n) for n in line.split(" ") if n]
        for i, num in enumerate(numbers):
            cols[i] = OPERATIONS[i](cols[i], num)
    return sum(cols)


def right_to_left(puzzle):
    def do_operation(start, puzzle):
        operation = OPERATION_MAP[puzzle[-1][start]]
        end = start + 1
        try:
            while puzzle[-1][end] == " ":
                end += 1
        except IndexError:
            end = len(puzzle[-1]) + 1
        result = 1 if operation == operator.mul else 0
        for i in range(start, end - 1):
            number = 0
            for row in puzzle[:-1]:
                if row[i] != " ":
                    number = 10 * number + int(row[i])
            result = operation(result, number)
        return result, end

    result = 0
    index = 0
    for _ in range(len(OPERATIONS)):
        current_result, index = do_operation(index, puzzle)
        result += current_result
    return result


print("1:", left_to_right(puzzle))
print("2:", right_to_left(puzzle))
