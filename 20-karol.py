from __future__ import annotations

import collections
import dataclasses
import math
import pathlib
import typing


def state(s):
    return "high" if s else "low"


NODES: dict[str, Node] = dict()
PULSE_COUNT = collections.Counter()
NODE_LIST: list[Node] = list()


@dataclasses.dataclass
class Node:
    name: str
    clk: int = 0
    outputs: list[Node] = dataclasses.field(default_factory=list, repr=False)
    inputs: list[Node] = dataclasses.field(default_factory=list, repr=False)
    state: bool = dataclasses.field(default=False)
    input_changes: list[Change] = dataclasses.field(default_factory=list, repr=False)

    @property
    def changed(self):
        return bool(self.input_changes)

    @property
    def pclk(self):
        if self.input_changes:
            return self.input_changes[0].clk
            # min_clk = math.inf
            # for _, _, clk in self.input_changes:
            #     min_clk = min(min_clk, clk)
            # return min_clk
        return self.clk

    def tick(self, g_clock: int):
        if g_clock == self.pclk and self.changed:
            for value in self.action():
                if value:
                    self.send_pulse()
        self.clk += 1

    def action(self):
        raise NotImplementedError()

    def send_pulse(self):
        for output_node in self.outputs:
            PULSE_COUNT[self.state] += 1
            print(f"{self.name} -{state(self.state)}-> {output_node.name}")
            output_node.input_changes.append(Change(self, self.state, self.clk + 1))

    @classmethod
    def factorio(cls, label: str) -> Node:
        klass: typing.Type[Node]

        # check first sign
        match label[0], label:
            case "%", _:
                klass = FlipFlop
                label = label[1:]
            case "&", _:
                klass = Conjunction
                label = label[1:]
            case _, "broadcaster":
                klass = Broadcaster
            case _:
                klass = Output

        node = klass(label)

        return node

    def add_output(self, other_node: Node):
        print(f"Adding output {self.name} -> {other_node.name}")
        self.outputs.append(other_node)
        other_node.inputs.append(self)


@dataclasses.dataclass
class Change:
    source: Node
    state: bool
    clk: int


@dataclasses.dataclass
class Broadcaster(Node):
    def action(self):
        change = self.input_changes.pop(0)
        assert len(self.inputs) == 1

        self.state = change.state
        yield True


@dataclasses.dataclass
class Output(Node):
    def action(self):
        yield False


@dataclasses.dataclass
class Button(Node):
    triggered: bool = False

    def press(self, clk):
        self.triggered = False
        self.input_changes.append(Change(self, False, clk))

    def action(self):
        self.input_changes.clear()
        self.state = False
        if not self.triggered:
            self.triggered = True
            yield True
        else:
            yield False


@dataclasses.dataclass
class FlipFlop(Node):
    prev_state: bool = False

    def action(self):
        # take item from incoming queue
        remaining_changes = []
        processing_changes = []

        for change in self.input_changes:
            if change.clk > self.clk:
                remaining_changes.append(change)
            else:
                processing_changes.append(change)

        self.input_changes = remaining_changes

        # self.clk = clk
        # print(f"{node.name} -{state(new_state)}-> {self.name}")
        flops = [change for change in processing_changes if change.state is False]
        assert len(flops) <= 1, processing_changes

        if not flops:
            yield False
        else:
            # print(f"change state from {state(self.state)} to {state(not new_state)}")
            self.state = not self.state
            yield True


@dataclasses.dataclass
class Conjunction(Node):
    input_states: dict[str, bool] = dataclasses.field(default_factory=dict)

    def action(self):
        if not self.input_states:
            for inp in self.inputs:
                self.input_states[inp.name] = False

        remaining_changes = []

        for change in self.input_changes:
            # node, new_state, clk = change
            if change.clk > self.clk:
                remaining_changes.append(change)
                continue

            # self.clk = clk
            self.input_states[change.source.name] = change.state
            self.state = not all(self.input_states.values())
            yield state

        self.input_changes = remaining_changes


def solve(path):
    data = pathlib.Path(path).read_text().splitlines()
    for line in data:
        node_name, _, _ = line.partition(" -> ")
        node = Node.factorio(node_name)
        NODES[node.name] = node
        NODE_LIST.append(node)

    # output = Output("output")
    # NODES["output"] = output

    for line in data:
        node_name, _, connected_nodes = line.partition(" -> ")
        connected_nodes = connected_nodes.split(", ")
        node_name = node_name.strip("%&")
        current_node = NODES[node_name]
        for connected_node in connected_nodes:
            output_node = NODES.get(connected_node)
            if output_node is None:
                print("-" * 40)
                print(f"Adding dummy node {connected_node}")
                print("-" * 40)
                output_node = Output(connected_node)
                NODES[connected_node] = output_node

            current_node.add_output(output_node)

    # add button and initialize it
    btn = Button("button")
    btn.add_output(NODES["broadcaster"])
    NODES["btn"] = btn
    NODE_LIST.insert(0, btn)

    global_clock = 0
    for i in range(1000):
        # print("==================")
        btn.press(global_clock)
        print("-" * 40)
        print(f"Pressed {i+1} time!")
        print("-" * 40)

        while True:
            # print("-" * 40)
            # print(f"{global_clock=}\n")

            # end condition
            queue = [n.changed and n.pclk == global_clock for n in NODE_LIST]
            if not any(queue):
                break

            # find node(s) with highest clk
            for n in NODE_LIST:
                n.tick(global_clock)

            global_clock += 1
            # input(">")
    print(PULSE_COUNT)
    return math.prod(PULSE_COUNT.values())


def main():
    # print(f'{solve("example.txt")=}')
    # print(f'{solve("wrn.txt")=}')
    print(f'{solve("inputs/20-karol.txt")=}')
    # print(f'{solve("input.txt")=}')
    # solve("input.txt")=601323840 -- too low
    # solve("input.txt")=601307779 -- too low
    # solve("input.txt")=602039529 -- too low
    # solve("input.txt")=631422154 ???
    # solve("input.txt")=728025736 ???


if __name__ == "__main__":
    main()
