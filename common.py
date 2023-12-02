def read_file(puzzle: str) -> str:
    with open(f"inputs/{puzzle}.txt") as f:
        return "".join(f.readlines())


def get_puzzle(filename: str, sample: bool = False):
    suffix = "-sample" if sample else ""
    return read_file(f"{filename.split('/')[-1].split('.')[0]}{suffix}").strip()
