puzzle = [line for line in open("inputs/01.txt").read().strip().split("\n")]

left = []
right = []
for line in puzzle:
    num_left, num_right = line.split()
    left.append(int(num_left))
    right.append(int(num_right))

left.sort()
right.sort()

distance = 0
for num_left, num_right in zip(left, right):
    distance += abs(num_left - num_right)

print("1:", distance)

similarity = 0
for number in left:
    count = right.count(number)
    similarity += count * number

print("2:", similarity)
