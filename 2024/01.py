# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      16.1 ms ±   1.4 ms    [User: 14.1 ms, System: 2.0 ms]
#   Range (min … max):    14.2 ms …  22.3 ms    167 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):      42.9 ms ±   3.9 ms    [User: 33.0 ms, System: 9.7 ms]
#   Range (min … max):    39.2 ms …  57.0 ms    71 runs
#
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
