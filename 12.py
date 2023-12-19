import re
import functools


puzzle = [l for l in open("inputs/12-moje.txt").read().strip().split("\n")]


# def find_consecutive(springs):
#     return tuple([len(s) for s in springs.split(".") if s])
#
#
# def find_unknown(springs):
#     return [i for i, s in enumerate(springs) if s == "?"]

counter = 0

@functools.cache
def parse(springs, consecutive, result=0, depth=0):
    global counter
    counter += 1
    current_counter = counter
    depth += 1
    log_prefix = "  " * (depth - 1)
    print(f"{log_prefix}{springs=}, {consecutive=}, {result=} called {counter} times! {depth=}")
    if springs == ".":
        print(f"{log_prefix}ZERO {current_counter=}")
        return 0
    
    if (
        len(consecutive) == 1
        and springs.count("#") == consecutive[0]
        and re.fullmatch("\#+\.*", springs)
    ):
        print(f"{log_prefix}ONE {current_counter=}")
        return 1

    if springs.startswith("."):
        return result + parse(springs[1:], consecutive, result, depth)

    if springs.startswith("?"):
        rest = springs[1:]
        result += parse(f".{rest}", consecutive, result, depth)
        result += parse(f"#{rest}", consecutive, result, depth)
        print(f"{log_prefix}?-start RETURNING {result} {current_counter=}")
        return result

    if springs.startswith("#"):
        prefix = springs[:consecutive[0]]
        if prefix == "#" * consecutive[0] and springs[consecutive[0]] not in ("#", "?"):
            print(f"{log_prefix}it is a match! {springs=} {consecutive=} {result=}")
            return result + parse(springs[consecutive[0]:], consecutive[1:], result, depth)
        else:
            if other_char := re.search(r"[^\#]", prefix):
                index = other_char.start()
                if prefix[index] == ".":
                    result += parse(springs[index:], consecutive, result)
                else:
                    result += parse(springs.replace("?", "#", 1), consecutive, result, depth)
                    result += parse(springs.replace("?", ".", 1), consecutive, result, depth)
                    print(f"{log_prefix}#-start RETURNING {result} {current_counter=}")
                    return result
    print(f"{log_prefix}RETURNING {result} {current_counter=}")
    return result


result_1 = 0
for i, line in enumerate(puzzle, start=1):
    springs, nums = line.split()
    consecutiveness = tuple([int(n) for n in nums.split(",")])
    print("============================")
    print("Springs:")
    print(line)
    counter = 0
    result = parse(springs, consecutiveness)
    print(f"{line}: {result=}")
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
