import bisect

puzzle = [line for line in open("inputs/05.txt").read().strip().split("\n")]

ranges = []
ingredienst = False
result_1 = 0
for line in puzzle:
    if ingredienst:
        if any(start <= int(line) <= end for start, end in ranges):
            result_1 += 1
    elif line == "":
        ingredienst = True
    else:
        start, end = line.split("-")
        bisect.insort(ranges, (int(start), int(end)))

print("1:", result_1)

non_overlapping = []
for start, end in ranges:
    if non_overlapping and start <= non_overlapping[-1][1]:
        non_overlapping[-1] = (non_overlapping[-1][0], max(end, non_overlapping[-1][1]))
    else:
        non_overlapping.append((start, end))

print("2:", sum(end - start + 1 for (start, end) in non_overlapping))
