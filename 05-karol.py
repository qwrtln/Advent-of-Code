import bisect
import dataclasses
import pathlib
import re

MAP_NAME = re.compile(r"^(\w+)-to-(\w+) map:$")


@dataclasses.dataclass(frozen=True)
class AlmanacMapping:
    src: range
    dst: range

    def __lt__(self, other):
        return self.src.start < other.src.start


class AlmanacMap:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.elements: list[AlmanacMapping] = []

    def __str__(self):
        return f"{self.src}-to-{self.dst}"

    def __repr__(self):
        return self.__str__()

    def get_element(self, idx):
        # print(f"Looking for {idx} in {self.elements}")
        for element in self.elements:
            if idx in element.src:
                return element
        return None

    def last_element(self):
        return self.elements[-1].src.stop

    def add_mapping(
        self, dst_range_start: int, src_range_start: int, range_length: int
    ):
        mapping = AlmanacMapping(
            src=range(src_range_start, src_range_start + range_length),
            dst=range(dst_range_start, dst_range_start + range_length),
        )
        bisect.insort(self.elements, mapping)

    def finalize_mapping(self):
        # Fill "holes" with empty mappings
        idx = 0
        new_elements = []

        for element in self.elements:
            if idx in element.src:
                # src starts from index, move it to end
                new_elements.append(element)
                idx = element.src.stop
            else:
                # generate dummy mapping
                try:
                    dummy_end = element.src.start
                    dummy_mapping = AlmanacMapping(
                        src=range(idx, dummy_end),
                        dst=range(idx, dummy_end),
                    )
                    new_elements.append(dummy_mapping)
                    new_elements.append(element)
                    idx = element.src.stop
                except IndexError:
                    pass

        assert set(new_elements).issuperset(self.elements)

    def get_subranges(self, src_ranges: list[range]):
        item = None
        while src_ranges:
            item = src_ranges.pop(0)

            current_range = self.get_element(item.start)
            if current_range is None:
                # case when we're after our table
                yield item
                continue

            if item.stop in current_range.src:
                # case when our set is a subset
                yield range(item.start, item.stop)
            else:
                # if range overlaps, return first part and calculate other
                offset = current_range.src.stop - item.start
                yield range(item.start, item.start + offset)
                src_ranges.append(range(item.start + offset, item.stop))

    def get_dst_ranges(self, src_ranges: list[range]):
        while src_ranges:
            src_range = src_ranges.pop(0)

            current_element = None
            for element in self.elements:
                if src_range.start in element.src:
                    current_element = element
                    break

            if current_element is None:
                yield src_range
                continue

            offset = current_element.src.index(src_range.start)
            yield range(
                current_element.dst.start + offset,
                current_element.dst.start + offset + len(src_range),
            )


def find_location_range(almanacs, src_ranges):
    for almanac in almanacs:
        # print(f"{sum(len(x) for x in src_ranges)=}")

        # print(f"{src_ranges=}")
        subranges = list(almanac.get_subranges(src_ranges))
        # print(f"{subranges=}")
        dst_ranges = list(almanac.get_dst_ranges(subranges))
        # print(f"{dst_ranges=}")
        src_ranges = dst_ranges
        # print("-" * 40)

    return dst_ranges


def parse_map(text):
    map_name = text.pop(0)
    match = MAP_NAME.match(map_name)
    if not match:
        return
    almanac = AlmanacMap(*match.groups())

    # process mapping
    line = text.pop(0)
    # print(f'{almanac=}')
    while line:
        dst_range_start, src_range_start, range_length = [
            int(x) for x in line.split(" ")
        ]
        almanac.add_mapping(
            dst_range_start=dst_range_start,
            src_range_start=src_range_start,
            range_length=range_length,
        )

        if text:
            line = text.pop(0)
        else:
            almanac.finalize_mapping()
            break

    return almanac


def solve(path: str):
    text = pathlib.Path(path).read_text().splitlines(False)

    seeds_line = text.pop(0)
    _ = text.pop(0)
    assert not _
    match_seeds = re.findall(r"\s*(\d+)", seeds_line)
    initial_seeds = [int(x) for x in match_seeds]
    # print(initial_seeds)
    # print(text)

    almanacs = []

    while text:
        almanacs.append(parse_map(text))

    # pt2
    seed_ranges = []
    while initial_seeds:
        start = initial_seeds.pop(0)
        length = initial_seeds.pop(0)
        seed_ranges.append(range(start, start + length))

    # print(f"Seeds: {len(seed_ranges)}")

    dst_ranges = find_location_range(almanacs, seed_ranges)
    # print(dst_ranges)

    minimal = 0xFFFFFFFF
    for rng in dst_ranges:
        minimal = min(rng.start, minimal)

    return minimal


def main():
    assert solve("inputs/05-sample.txt") == 46
    print(solve("inputs/05.txt"))


if __name__ == "__main__":
    main()
