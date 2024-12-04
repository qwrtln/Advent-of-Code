def read_file(puzzle: str) -> str:
    with open(f"inputs/{puzzle}.txt") as f:
        return "".join(f.readlines())
