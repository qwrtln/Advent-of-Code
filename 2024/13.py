# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):      43.8 ms ±   2.1 ms    [User: 32.7 ms, System: 11.0 ms]
#   Range (min … max):    40.7 ms …  51.6 ms    68 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):      79.5 ms ±   5.6 ms    [User: 55.7 ms, System: 24.2 ms]
#   Range (min … max):    75.3 ms … 107.9 ms    36 runs
#
from dataclasses import dataclass


@dataclass
class Machine:
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    prize_x: int
    prize_y: int


def parse_buttons(button, line):
    x, y = line.strip(f"Button {button}: ").split(", ")
    return int(x[2:]), int(y[2:])


def parse_prize(line):
    x, y = line.strip("Prize: ").split(", ")
    return int(x[2:]), int(y[2:])


def parse_machine(m):
    return Machine(
        *parse_buttons("A", m[0]), *parse_buttons("B", m[1]), *parse_prize(m[2])
    )


def get_all_machines(puzzle):
    machines = []
    m = []
    for line in open(puzzle).read().strip().split("\n"):
        if line == "":
            machines.append(parse_machine(m))
            m = []
        else:
            m.append(line)
    machines.append(parse_machine(m))
    return machines


def presses_price(presses):
    a, b = presses
    return 3 * a + b


def solve_machine(m, modifier=0):
    # https://en.wikipedia.org/wiki/Cramer%27s_rule
    prize_x = m.prize_x + modifier
    prize_y = m.prize_y + modifier
    det = m.a_x * m.b_y - m.b_x * m.a_y
    det_a = prize_x * m.b_y - m.b_x * prize_y
    det_b = m.a_x * prize_y - prize_x * m.a_y
    if det_a % det == 0 and det_b % det == 0:
        return det_a // det, det_b // det


result_1 = 0
result_2 = 0
increase = 10**13
for m in get_all_machines("inputs/13.txt"):
    if solution := solve_machine(m):
        result_1 += presses_price(solution)
    if solution := solve_machine(m, increase):
        result_2 += presses_price(solution)

print("1:", result_1)
print("2:", result_2)
