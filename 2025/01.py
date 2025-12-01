puzzle = [line for line in open("inputs/01.txt").read().strip().split("\n")]

DIAL_STEPS = 100
position = 50
step_zero = 0
crossed_zero = 0
for line in puzzle:
    steps = int(line[1:])
    if line.startswith("L"):
        steps *= -1
        crossed_zero += abs((position + steps) // DIAL_STEPS)
    else:
        crossed_zero += (position + steps - 1) // DIAL_STEPS + abs(
            (position - 1) // DIAL_STEPS
        )
    position += steps
    position %= DIAL_STEPS
    step_zero += position == 0


print(f"1: {step_zero}")
print(f"2: {crossed_zero}")
