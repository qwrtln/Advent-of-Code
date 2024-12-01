from common import get_puzzle


def find_ways(times, dists):
    result = 1
    solutions = 0
    for time, dist in zip(times, dists):
        for i in range(1, time):
            if i * (time - i) > dist:
                solutions += 1
        result *= solutions
        solutions = 0
    return result


if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=False)

    times = [int(t) for t in puzzle[0].split(":")[1].strip().split()]
    dists = [int(t) for t in puzzle[1].split(":")[1].strip().split()]

    single_time = int("".join(str(t) for t in times))
    single_dist = int("".join(str(d) for d in dists))

    print("1:", find_ways(times, dists))
    print("2:", find_ways([single_time], [single_dist]))
