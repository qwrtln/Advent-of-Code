from typing import Any, Dict, List, Optional, Tuple


from common import read_file


class File:
    name: str
    size: int

    def __init__(self, name: str, size: str) -> None:
        self.name = name
        self.size = int(size)


class Directory:
    name: str
    parent: Optional["Directory"]
    contents: List[Any]
    _dirs: Dict[str, Any]

    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        self.name = name
        self.parent = parent
        self.contents = []
        self._dirs = {}

    def add_contents(self, content: Any) -> None:
        self.contents.append(content)
        if isinstance(content, Directory):
            self._dirs[content.name] = content

    @property
    def size(self) -> int:
        total_size = 0
        for item in self.contents:
            if isinstance(item, File):
                total_size += item.size
            else:
                total_size += item.size
        return total_size

    def change_dir(self, name: str) -> "Directory":
        if name == "..":
            return self.parent
        return self._dirs[name]


def find_dirs(dir: Directory) -> List[Directory]:
    dirs = []
    for item in dir.contents:
        if isinstance(item, Directory):
            dirs.append(item)
            dirs += find_dirs(item)
    return dirs


if __name__ == "__main__":
    puzzle = read_file("07").split("\n")[:-1]
    filesystem = Directory("/")
    current_dir = filesystem
    for line in puzzle[2:]:
        if line.startswith("$"):
            commands = line.split(" ")
            if commands[1] == "cd":
                current_dir = current_dir.change_dir(commands[2])
        elif line.startswith("dir"):
            dir_name = line.split(" ")[1]
            current_dir.add_contents(Directory(dir_name, parent=current_dir))
        else:
            size, name = line.split(" ")
            current_dir.add_contents(File(name, size))

    total_disk_space = 70000000
    space_required = 30000000
    space_available = total_disk_space - filesystem.size
    must_delete_at_least = space_required - space_available
    current_max = total_disk_space

    for d in find_dirs(filesystem):
        if d.size > must_delete_at_least and d.size < current_max:
            current_max = d.size
    print(current_max)
