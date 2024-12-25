puzzle = open("inputs/17.txt").read().strip().split("\n")


def convert_combo(operand, registers):
    if operand in range(4):
        return operand
    if operand == 4:
        return registers["A"]
    if operand == 5:
        return registers["B"]
    if operand == 6:
        return registers["C"]
    raise ValueError(f"{operand} is impossible")


def adv_0(operand, registers):
    registers["A"] //= 2 ** convert_combo(operand, registers)


def bxl_1(operand, registers):
    registers["B"] ^= operand


def bst_2(operand, registers):
    registers["B"] = convert_combo(operand, registers) % 8


def jnz_3(operand, index, registers):
    return operand if registers["A"] else index + 2


def bxc_4(_, registers):
    registers["B"] ^= registers["C"]


def out_5(operand, registers):
    return convert_combo(operand, registers) % 8


def bdv_6(operand, registers):
    registers["B"] = registers["A"] // 2 ** convert_combo(operand, registers)


def cdv_7(operand, registers):
    registers["C"] = registers["A"] // 2 ** convert_combo(operand, registers)


OPCODE_MAPPING = {
    0: adv_0,
    1: bxl_1,
    2: bst_2,
    3: jnz_3,
    4: bxc_4,
    5: out_5,
    6: bdv_6,
    7: cdv_7,
}


def run_program(a, program):
    program = list(map(int, program.split(",")))
    index = 0
    output = []
    registers = {"A": a, "B": 0, "C": 0}
    while index < len(program):
        opcode, operand = program[index], program[index + 1]
        instruction = OPCODE_MAPPING[opcode]
        if opcode == 3:
            index = instruction(operand, index, registers)
        else:
            index += 2
        if opcode == 5:
            output.append(instruction(operand, registers))
        elif opcode != 3:
            instruction(operand, registers)
    return ",".join(str(o) for o in output)


A = int(puzzle[0].split(": ")[-1])
program = puzzle[4].split(": ")[-1]
print("1:", run_program(A, program))


# def optimized_program(A):
#     while A:
#         yield ((((A & 7) ^ 1) ^ 4) ^ (A >> ((A & 7) ^ 1))) & 7
#         A >>= 3
