import functools


puzzle = [line for line in open("inputs/12.txt").read().strip().split("\n")]


@functools.cache
def parse(springs, consecutive):
    result = 0

    if not springs:
        if not consecutive:
            return 1
        return 0

    if not consecutive:
        if "#" not in springs:
            return 1
        return 0

    if springs.startswith(".") or springs.startswith("?"):
        result += parse(
            springs[1:], consecutive
        )  # dots in the beginning can be omitted

    if springs.startswith("#") or springs.startswith("?"):
        if (
            (consecutive[0] <= len(springs))
            and (
                "." not in springs[: consecutive[0]]
            )  #  any str with given length of #s and ?s
            and (
                len(springs) == consecutive[0] or springs[consecutive[0]] != "#"
            )  # group cannot end with a hashtag
        ):
            result += parse(springs[consecutive[0] + 1 :], consecutive[1:])

    return result


result_1 = 0
result_2 = 0
for i, line in enumerate(puzzle, start=1):
    springs, nums = line.split()
    consecutiveness = tuple([int(n) for n in nums.split(",")])
    result_1 += parse(springs, consecutiveness)
    r2 = parse("?".join([springs for _ in range(5)]), consecutiveness * 5)
    result_2 += r2
    print(f"{i}/{len(puzzle)}: {r2}")

# LOW = 30303874173432
# HIGH = 2231084203746644906
print("1:", result_1)
print("2:", result_2)
# assert HIGH > result_2 > LOW, result_2
