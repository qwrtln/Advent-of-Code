# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     14.230 s ±  0.161 s    [User: 14.210 s, System: 0.002 s]
#   Range (min … max):   13.972 s … 14.440 s    10 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):      1.940 s ±  0.164 s    [User: 1.919 s, System: 0.015 s]
#   Range (min … max):    1.758 s …  2.266 s    10 runs
#
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
