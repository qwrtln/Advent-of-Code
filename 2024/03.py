import re

puzzle = [line for line in open("inputs/03.txt").read().strip().split("\n")]

result_1 = 0
result_2 = 0
enabled = True
for line in puzzle:
    matches = re.findall(r"(mul\([0-9]+,[0-9]+\))|(do\(\))|(don't\(\))", line)
    for m in matches:
        if m[1]:
            enabled = True
        elif m[2]:
            enabled = False
        else:
            num1, num2 = m[0][4:-1].split(",")
            result_1 += int(num1) * int(num2)
            if enabled:
                result_2 += int(num1) * int(num2)
print("1:", result_1)
print("2:", result_2)
