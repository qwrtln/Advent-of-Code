import collections
import contextlib
import string

puzzle = [w for w in open("inputs/15.txt").read().strip().split(",")]

MULTIPLICAND = 17
DIVISOR = 256
BOXES = [collections.OrderedDict() for _ in range(DIVISOR)]

def HASH(word):
    value = 0
    for char in word:
        value += ord(char)
        value *= MULTIPLICAND
        value %= DIVISOR
    return value


result_1 = 0
result_2 = 0
for word in puzzle:
    result_1 += HASH(word)
    
    label = "".join([c for c in word if c in string.ascii_letters])
    box_number = HASH(label)
    if "-" in word:
        with contextlib.suppress(KeyError):
            del BOXES[box_number][label]
    else:
        BOXES[box_number][label] = int(word[-1])

for box_number, box in enumerate(BOXES, 1):
    for slot_number, focal_length in enumerate(box.values(), 1):
        result_2 += box_number * slot_number * focal_length

print("1:", result_1)
print("2:", result_2)
