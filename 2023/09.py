import itertools

puzzle = [l for l in open("inputs/09.txt").read().strip().split("\n")]

result_1 = 0
result_2 = 0
for line in puzzle:
    numbers = [int(n) for n in line.split()]
    last_nums = [numbers[-1]]
    first_nums = [numbers[0]]
    while any(numbers):
        numbers = [j - i for i, j in itertools.pairwise(numbers)]
        last_nums.append(numbers[-1])
        first_nums.append(numbers[0])

    result_1 += sum(last_nums)

    *_, extra_left = itertools.accumulate(
        first_nums[::-1], lambda a, b: b - a, initial=0
    )
    result_2 += extra_left

print("1:", result_1)
print("2:", result_2)
