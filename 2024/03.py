# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      14.3 ms ±   1.2 ms    [User: 11.4 ms, System: 2.7 ms]
#   Range (min … max):    12.4 ms …  18.6 ms    174 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):      91.3 ms ±   6.8 ms    [User: 74.4 ms, System: 16.3 ms]
#   Range (min … max):    83.4 ms … 106.2 ms    28 runs
#
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
