import pathlib

import tqdm
import numpy as np


puzzle = pathlib.Path("inputs/05.txt").read_text().splitlines(False)


def get_maps(lines):
    maps = dict()
    for line in lines:
        if "map:" in line:
            name = line.split("map:")[0]
            maps[name] = []
        elif line:
            maps[name].append([int(r) for r in line.split(" ")])
    return maps


def get_batch_next(value_batch, ranges):
    result = value_batch.copy()
    for target, start, count in ranges:
        where = np.logical_and(start <= value_batch, value_batch < start + count)
        values = target + value_batch[where] - start
        result[where] = values
    return result


seed_ranges = [int(s) for s in puzzle[0].split(":")[1].strip().split(" ")]
min_result = 613341484876
maps = get_maps(puzzle[2:])

BATCHSIZE = 2**16
for seed_start, seed_range in zip(seed_ranges[::2], seed_ranges[1::2]):
    print(seed_start, seed_range)
    for batch in tqdm.tqdm(range(int(seed_range / BATCHSIZE) + 1)):
        seeds = np.arange(
            seed_start + batch * BATCHSIZE,
            min(seed_start + (batch + 1) * BATCHSIZE, seed_start + seed_range),
        )
        values = seeds
        for name, ranges in maps.items():
            values = get_batch_next(values, ranges)
        min_result = min(min_result, values.min())

print("\n", min_result)
