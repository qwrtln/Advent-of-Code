puzzle = [line for line in open("inputs/03.txt").read().strip().split("\n")]


def joltage(pack, target_length):
    budget = len(pack) - target_length
    digits = []
    for current in pack:
        while digits and current > digits[-1] and budget > 0:
            digits.pop()
            budget -= 1
        digits.append(current)
    return int("".join(digits[:target_length]))


result_1 = 0
result_2 = 0
for line in puzzle:
    result_1 += joltage(line, target_length=2)
    result_2 += joltage(line, target_length=12)

print("1:", result_1)
print("2:", result_2)
