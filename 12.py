import re
import functools


puzzle = [l for l in open("inputs/12-moje.txt").read().strip().split("\n")]


def find_consecutive(springs):
    return tuple([len(s) for s in springs.split(".") if s])


def find_unknown(springs):
    return [i for i, s in enumerate(springs) if s == "?"]


@functools.cache
def parse(springs, consecutive, result=0):
    print(f"{springs} {consecutive} {result}")
    if springs == "#":
        print("Reached end spring")
        return result + 1
    elif springs == ".":
        print("Reached end broken")
        return result

    if springs[0] == "?":
        print("? <- we're branching")
        result += parse("." + springs[1:], consecutive[1:], result)
        result += parse("#" + springs[1:], consecutive, result)

    if (
        len(consecutive) == 1
        and springs.count("#") == consecutive[0]
        and (
            re.fullmatch("\.+\#+\.*", springs)
            or re.fullmatch("\#+\.+", springs)
            or re.fullmatch("\.+\#+", springs)
        )
    ):
        print("Final segment")
        print(f"Recursion about to return {result + 1}")
        return result + 1

    print(f"Recursion about to return {result}")
    return result


result_1 = 0
for i, line in enumerate(puzzle, start=1):
    springs, nums = line.split()
    consecutiveness = tuple([int(n) for n in nums.split(",")])
    print("============================")
    print("Springs:")
    print(line)

    result = parse(springs, consecutiveness)
    print(f"End {result=}")
    # springs = "?".join([springs for _ in range(5)])
    # consecutiveness *= 5
    #
    # print(springs, consecutiveness)
    # unknown = find_unknown(springs)
    # missing_springs = sum(consecutiveness) - springs.count("#")
    # missing_broken = springs.count("?") - missing_springs
    # assert missing_springs + missing_broken == springs.count("?")
    #
    # for ind, r in enumerate(itertools.product("#.", repeat=springs.count("?")), start=1):
    #
    #     if sum(consecutiveness) != r.count("#") + springs.count("#"):
    #         continue
    #
    #     replacement_index = 0
    #     assumed_springs = ""
    #     for index, char in enumerate(springs):
    #         if char == "?":
    #             assumed_springs += r[replacement_index]
    #             replacement_index += 1
    #         else:
    #             assumed_springs += char
    #     if find_consecutive(assumed_springs) == consecutiveness:
    #         result += 1
    # print(f"{ind}: {result}")
    result_1 += result
    print(f"{i}/{len(puzzle)}: {result_1}")
    input("============================")
print(result)
