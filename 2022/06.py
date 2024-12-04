from itertools import count


from common import read_file


MARKER_LENGTH = 14

if __name__ == "__main__":
    puzzle = read_file("06")

    for i in count():
        chars = puzzle[i : i + MARKER_LENGTH]
        if len(chars) == len(set(chars)):
            print(i + MARKER_LENGTH)
            break
