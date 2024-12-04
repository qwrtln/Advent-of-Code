import textwrap


from common import read_file


CYCLES_TO_MEASURE = [20, 60, 100, 140, 180, 220]


def check_cycle(cycle: int, signal: int) -> int:
    if cycle in CYCLES_TO_MEASURE:
        return cycle * signal
    return 0


def draw_pixel(cycle: int, signal: int) -> chr:
    if cycle % 40 in range(signal, signal + 3):
        return "#"
    return "."


if __name__ == "__main__":
    puzzle = read_file("10").split("\n")[:-1]
    signal = 1
    cycle = 0
    pixels = ""
    signal_strength = 0
    for line in puzzle:
        if line == "noop":
            cycle += 1
            signal_strength += check_cycle(cycle, signal)
            pixels += draw_pixel(cycle, signal)
            continue
        cycle += 1
        signal_strength += check_cycle(cycle, signal)
        pixels += draw_pixel(cycle, signal)
        cycle += 1
        signal_strength += check_cycle(cycle, signal)
        pixels += draw_pixel(cycle, signal)
        _, value = line.split(" ")
        signal += int(value)
    print(signal_strength)
    print("\n".join(textwrap.wrap(pixels, 40)))
