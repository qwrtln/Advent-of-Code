# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     536.7 ms ±  28.0 ms    [User: 528.7 ms, System: 6.8 ms]
#   Range (min … max):   505.0 ms … 588.0 ms    10 runs
#
# Benchmark: pypy (3.10.14)
#   Time (mean ± σ):     353.9 ms ±  26.5 ms    [User: 324.1 ms, System: 28.9 ms]
#   Range (min … max):   332.9 ms … 421.0 ms    10 runs
#
import bisect
import copy
import operator
from dataclasses import dataclass

puzzle = open("inputs/09.txt").read().strip().split("\n")[0]


@dataclass
class File:
    id: int
    index: int
    size: int


@dataclass
class Space:
    index: int
    size: int


def parse_disk(puzzle):
    files, spaces = [], []
    is_file = True
    file_id, index = 0, 0
    for digit in puzzle:
        size = int(digit)
        if is_file:
            files.append(File(id=file_id, index=index, size=size))
            file_id += 1
        else:
            spaces.append(Space(index=index, size=size))
        index += size
        is_file = not is_file

    return files, spaces


def move_blocks(files, spaces):
    new_files = []
    last_file = files.pop()
    for space in spaces:
        index = space.index
        while space.size >= last_file.size:
            if last_file.index < space.index:
                files.append(last_file)
                return new_files
            new_files.append(File(last_file.id, index, last_file.size))
            space.size -= last_file.size
            index += last_file.size
            last_file = files.pop()
        if space.size < last_file.size:
            if last_file.index < space.index:
                files.append(last_file)
                return new_files
            new_files.append(File(last_file.id, index, space.size))
            last_file.size -= space.size


def _find_space(size, spaces):
    for s in spaces:
        if s.size >= size:
            return s


def _swap_file_w_space(file, space, spaces):
    old_file_index = file.index
    file.index = space.index
    space.index = old_file_index
    spaces.remove(space)
    bisect.insort(spaces, space, key=operator.attrgetter("index"))


def _put_file_in_bigger_space(file, space, spaces):
    spaces.remove(space)
    remaining_space = Space(space.index + file.size, space.size - file.size)
    pushed_back_space = Space(file.index, file.size)
    file.index = space.index
    spaces.append(pushed_back_space)
    bisect.insort(spaces, remaining_space, key=operator.attrgetter("index"))


def defragment(files, spaces):
    for file in sorted(files, key=operator.attrgetter("id"), reverse=True):
        space = _find_space(file.size, spaces)
        if space and space.index < file.index:
            if file.size == space.size:
                _swap_file_w_space(file, space, spaces)
            else:
                _put_file_in_bigger_space(file, space, spaces)


def calculate_checksum(files):
    result = 0
    for f in files:
        for s in range(0, f.size):
            result += f.id * (f.index + s)
    return result


files, spaces = parse_disk(puzzle)

files_backup = copy.deepcopy(files)
spaces_backup = copy.deepcopy(spaces)

moved_files = move_blocks(files, spaces) or []
print("1:", calculate_checksum([*files, *moved_files]))

defragment(files_backup, spaces_backup)
print("2:", calculate_checksum(files_backup))
