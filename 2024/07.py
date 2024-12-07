import itertools
import operator

puzzle = [line for line in open("inputs/07.txt").read().strip().split("\n")]


def parse_puzzle(puzzle):
    numbers = {}
    for line in puzzle:
        result, nums = line.split(": ")
        numbers[int(result)] = [int(n) for n in nums.split(" ")]
    return numbers


def is_target_possible(target, nums, operations):
    current = nums[0]
    for oper in itertools.product(operations, repeat=len(nums) - 1):
        for op, num in zip(oper, nums[1:]):
            current = op(current, num)
        if current == target:
            return True
        current = nums[0]
    return False


def calculate_result(numbers, operations):
    result = 0
    for target, nums in numbers.items():
        if is_target_possible(target, nums, operations):
            result += target
    return result


numbers = parse_puzzle(puzzle)

operations = [operator.add, operator.mul]
print("1:", calculate_result(numbers, operations))

operations.append(lambda a, b: int(str(a) + str(b)))
print("2:", calculate_result(numbers, operations))
