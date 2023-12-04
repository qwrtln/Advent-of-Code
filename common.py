import pathlib


def get_puzzle(name: str, sample: bool = False):
    suffix = "-sample" if sample else ""
    filename = f"{name.split('/')[-1].split('.')[0]}{suffix}"
    path = f"inputs/{filename}.txt"
    return pathlib.Path(path).read_text().splitlines(False)
