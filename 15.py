puzzle = [w for w in open("inputs/15.txt").read().strip().split(",")]

MULTIPLICAND = 17
DIVISOR = 256

result_1 = 0
for word in puzzle:
    current_value = 0
    for char in word:
        current_value += ord(char)
        current_value *= MULTIPLICAND
        current_value %= DIVISOR
    result_1 += current_value

print("1:", result_1)
