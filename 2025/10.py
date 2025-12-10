import dataclasses
import itertools

import pulp

puzzle = [line for line in open("inputs/10.txt").read().strip().split("\n")]


@dataclasses.dataclass
class Lights:
    buttons: list[tuple[int]]
    target_joltage: list[int]
    target_bulbs: list[bool]

    bulbs: list[bool]
    joltage: list[int]

    def __init__(self, buttons, target_bulbs, target_joltage) -> None:
        self.buttons = buttons
        self.target_bulbs = target_bulbs
        self.target_joltage = target_joltage

        self.bulbs = [False for _ in self.target_bulbs]
        self.joltage = [0 for _ in self.target_joltage]

    def press(self, *presses) -> None:
        for j in presses:
            indices = self.buttons[j]
            new_state = []
            for i, bulb in enumerate(self.bulbs):
                if i in indices:
                    new_state.append(not bulb)
                else:
                    new_state.append(bulb)
            self.bulbs = new_state

    def bulbs_ready(self) -> bool:
        return self.bulbs == self.target_bulbs

    def reset(self) -> None:
        self.bulbs = [False for _ in self.bulbs]


lights = []
for line in puzzle:
    bulbs = [b == "#" for b in line.split("] (")[0][1:]]
    buttons = []
    for button in line.split("] ")[1].split(" {")[0].split(" "):
        buttons.append(tuple(int(b) for b in button[1:-1].split(",")))
    joltage = [int(j) for j in line.split(" {")[1][:-1].split(",")]
    lights.append(
        Lights(
            buttons=buttons,
            target_bulbs=bulbs,
            target_joltage=joltage,
        )
    )


def find_fewest_clicks(light: Lights):
    button_count = len(light.buttons)

    for i in range(button_count):
        for clicks in itertools.combinations_with_replacement(range(button_count), i):
            light.reset()
            light.press(*clicks)
            if light.bulbs_ready():
                return len(clicks)
    return 0


def find_fewest_joltage_clicks(light: Lights):
    clicks = []
    for i in range(len(light.buttons)):
        click = pulp.LpVariable(f"button_{i}", lowBound=0, cat="Integer")
        clicks.append(click)
    problem = pulp.LpProblem("minimize", pulp.LpMinimize)
    problem += pulp.lpSum(clicks)

    for j in range(len(light.joltage)):
        buttons_affecting = []
        for button_index in range(len(light.buttons)):
            if j in light.buttons[button_index]:
                buttons_affecting.append(clicks[button_index])
        problem += pulp.lpSum(buttons_affecting) == light.target_joltage[j]
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    return int(problem.objective.value())


result_1 = 0
result_2 = 0
for light in lights:
    result_1 += find_fewest_clicks(light)
    result_2 += find_fewest_joltage_clicks(light)

print("1:", result_1)
print("2:", result_2)
