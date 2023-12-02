from common import get_puzzle

RED = 12
GREEN = 13
BLUE = 14

if __name__ == "__main__":
    puzzle = get_puzzle(__file__, sample=True)

    for line in puzzle.split("\n"):
        print(line)
