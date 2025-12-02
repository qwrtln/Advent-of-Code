import math

puzzle = [line for line in open("inputs/02.txt").read().strip().split(",")]


def is_mirror(n):
    length = int(math.log10(n)) + 1
    if length % 2 == 1:
        return False
    half = 10 ** (length // 2)
    return n // half == n % half


def is_invalid(n):
    number = str(n)
    for i in range(1, len(number) // 2 + 1):
        a, b = number[:i], number[i:]
        if a not in b:
            return False
        if b.replace(a, "") == "":
            return True
    return False


result_1 = 0
result_2 = 0
for number in puzzle:
    start, stop = number.split("-")
    for i in range(int(start), int(stop) + 1):
        if is_mirror(i):
            result_1 += i
        if is_invalid(i):
            result_2 += i

print("1:", result_1)
print("2:", result_2)
