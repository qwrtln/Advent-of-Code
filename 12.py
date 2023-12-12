import itertools


puzzle = [l for l in open("inputs/12.txt").read().strip().split("\n")]


def find_consecutive(springs):
    return [len(s) for s in springs.split(".") if s]

def find_unknown(springs):
    return [i for i, s in enumerate(springs) if s == "?"]


result = 0
for line in puzzle:
    # print(line)
    springs, nums = line.split()
    consecutiveness = [int(n) for n in nums.split(",")]
    # print(consecutiveness)
    unknown = find_unknown(springs)
    missing_springs = sum(consecutiveness) - springs.count("#")
    missing_broken = springs.count("?") - missing_springs
    assert missing_springs + missing_broken == springs.count("?")

    for r in itertools.product("#.", repeat=springs.count("?")):
        # print(r)
        if sum(consecutiveness) != r.count("#") + springs.count("#"):
            # print("That's impossible!")
            continue
        # print("Good one")
        replacement_index = 0
        assumed_springs = ""
        for index, char in enumerate(springs):
            if char == "?":
                assumed_springs += r[replacement_index]
                replacement_index += 1
            else:
                assumed_springs += char
        if find_consecutive(assumed_springs) == consecutiveness:
            result += 1
    # input(f"=======================: {result}")
print(result)
        
