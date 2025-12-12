import copy
import dataclasses
import string

puzzle = [line for line in open("inputs/12.txt").read().strip().split("\n")]


@dataclasses.dataclass
class Region:
    width: int
    height: int
    present_count: list[int]

    grid: list[list[int]] = dataclasses.field(init=False)

    def __post_init__(self):
        self.grid = []
        for _ in range(self.height):
            self.grid.append([0 for _ in range(self.width)])

    @property
    def valid(self) -> bool:
        for line in self.grid:
            for point in line:
                if point > 1:
                    return False
        return True

    def insert(self, x, y, present) -> bool:
        backup = copy.deepcopy(self.grid)
        for i in range(3):
            for j in range(3):
                self.grid[y + j][i + x] += present.lines[j][i]
                if self.grid[y + j][i + x] > 1:
                    self.grid = backup
                    return False
        return True

    @property
    def area(self) -> int:
        return self.width * self.height

    def has_enough_space(self, presents) -> bool:
        present_area = 0
        for i, c in enumerate(self.present_count):
            present_area += c * presents[i].area
            if present_area > self.area:
                return False
        return True

    def __repr__(self) -> str:
        repr = ""
        for l in self.grid:
            for number in l:
                repr += "#" if number == 1 else "."
            repr += "\n"
        return repr[:-1]


@dataclasses.dataclass
class Present:
    lines: list[list[int]]

    def flip_vertically(self) -> None:
        new_lines = []
        for l in self.lines:
            new_lines.append(l[::-1])
        self.lines = new_lines

    def flip_horizontally(self) -> None:
        self.lines = self.lines[::-1]

    def rotate(self, angle: int) -> None:
        match angle:
            case 1:  # 90 degrees
                new_lines = [[0, 0, 0] for _ in range(3)]
                index = 2
                for l in self.lines:
                    for i, p in enumerate(l):
                        new_lines[i][index] = p
                    index -= 1
                self.lines = new_lines
            case 2:  # 180 degrees
                self.flip_vertically()
                self.flip_horizontally()
            case 3:  # 270 degrees
                new_lines = [[0, 0, 0] for _ in range(3)]
                index = 0
                for l in self.lines:
                    for i, p in enumerate(l):
                        new_lines[2 - i][index] = p
                    index += 1
                self.lines = new_lines

    @property
    def area(self) -> int:
        return sum(sum(l) for l in self.lines)

    def __repr__(self) -> str:
        repr = ""
        for l in self.lines:
            for number in l:
                repr += "#" if number == 1 else "."
            repr += "\n"
        return repr[:-1]


def parse_input(puzzle):
    presents = {}
    regions = []
    parsing_presents = True
    present_lines = []
    present_index = None

    for line in puzzle:
        if "x" in line:
            parsing_presents = False
        if parsing_presents:
            if line == "":
                presents[present_index] = Present(present_lines)
                present_lines = []
            elif line and line[0] in string.digits:
                present_index = int(line[0])
            else:
                present_lines.append([1 if c == "#" else 0 for c in line])
        else:
            grid_size, present_count = line.split(": ")
            coords = [int(c) for c in grid_size.split("x")]
            presents_index = [int(p) for p in present_count.split()]
            regions.append(Region(coords[0], coords[1], presents_index))
    return presents, regions


presents, regions = parse_input(puzzle)

print(sum(r.has_enough_space(presents) for r in regions))
