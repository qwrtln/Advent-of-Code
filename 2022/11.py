import math
import operator

from enum import Enum
from queue import Queue
from typing import Optional


from common import read_file


class Operation(str, Enum):
    ADD = "ADD"
    MULTIPLY = "MULTIPLY"
    SQUARE = "SQUARE"


CALM_FACTOR = 1

MONKEY_MAPPING = {}

LEAST_COMMON_MULTIPLE = 0


class Monkey:
    index: int
    items: Queue
    modulo: int
    operation: Operation
    fail_index: int
    pass_index: int
    _inspections: int
    lcm: int

    factor: Optional[int]

    def __init__(
        self,
        *,
        index: int,
        items: Queue[int],
        operation: Operation,
        factor: Optional[int],
        modulo: int,
        fail_index: int,
        pass_index: int,
    ) -> "Monkey":
        self.index = index
        self.items = items
        self.operation = operation
        self.factor = factor
        self.modulo = modulo
        self.fail_index = fail_index
        self.pass_index = pass_index
        self._inspections = 0

    def calculate_worry_level(self, item: int) -> int:
        new_worry_level = 0
        if self.operation == Operation.ADD:
            new_worry_level = item + self.factor
        if self.operation == Operation.MULTIPLY:
            new_worry_level = item * self.factor
        if self.operation == Operation.SQUARE:
            new_worry_level = pow(item, 2)
        return new_worry_level

    def do_round(self) -> None:
        while not self.items.empty():
            self._inspections += 1
            item = self.items.get()
            new_worry_level = self.calculate_worry_level(item) // CALM_FACTOR
            negation = ""
            if new_worry_level % self.modulo == 0:
                new_monkey = MONKEY_MAPPING[self.pass_index]
            else:
                new_monkey = MONKEY_MAPPING[self.fail_index]
                negation = "not "
            new_monkey.catch_item(new_worry_level % LEAST_COMMON_MULTIPLE)

    def catch_item(self, item: int) -> None:
        self.items.put(item)

    def __repr__(self) -> str:
        return f"Monkey {self.index} inspected {self._inspections} items"


if __name__ == "__main__":
    puzzle = read_file("11").split("Monkey")[1:]

    monkeys = []

    for mo in puzzle:
        index, modulo, failed_index, passed_index = 0, 0, 0, 0
        lines = mo.strip().split("\n")

        index = int(lines[0][0])

        _, items = lines[1].split(": ")
        actual_items = [int(i) for i in items.split(", ")]
        q = Queue()
        for i in actual_items:
            q.put(i)

        _, operation_str = lines[2].split(" = ")
        operation, factor = None, None
        if "+" in operation_str:
            _, additive = operation_str.split(" + ")
            operation = Operation.ADD
            factor = int(additive)
        elif "*" in operation_str:
            _, multiplicand = operation_str.split(" * ")
            if multiplicand == "old":
                operation = Operation.SQUARE
            else:
                operation = Operation.MULTIPLY
                factor = int(multiplicand)

        modulo = int(lines[3].split(" by ")[1])

        passed_index = int(lines[4].split("monkey ")[1])
        failed_index = int(lines[5].split("monkey ")[1])

        monkey = Monkey(
            index=index,
            items=q,
            operation=operation,
            factor=factor,
            modulo=modulo,
            fail_index=failed_index,
            pass_index=passed_index,
        )

        MONKEY_MAPPING[monkey.index] = monkey
        monkeys.append(monkey)

    LEAST_COMMON_MULTIPLE = math.lcm(*[m.modulo for m in monkeys])

    rounds = 100000
    for round in range(rounds):
        for m in monkeys:
            m.do_round()
    monkeys.sort(key=operator.attrgetter("_inspections"), reverse=True)
    print(monkeys[0]._inspections * monkeys[1]._inspections)
