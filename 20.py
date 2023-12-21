import dataclasses
import enum
import itertools
import math
import queue

import graphviz


puzzle = [line for line in open("inputs/20.txt").read().strip().split("\n")]


class Pulse(enum.StrEnum):
    LOW = "low"
    HIGH = "high"


@dataclasses.dataclass
class FlipFlop:
    name: str
    on: bool

    def receive(self, pulse: Pulse, _: str):
        if pulse == Pulse.LOW:
            self.on = not self.on
            return Pulse.HIGH if self.on else Pulse.LOW


@dataclasses.dataclass
class Conjunction:
    name: str
    inputs: dict

    def receive(self, pulse: Pulse, source: str):
        self.inputs[source] = pulse
        if all([p == Pulse.HIGH for p in self.inputs.values()]):
            return Pulse.LOW
        return Pulse.HIGH


@dataclasses.dataclass
class Relay:
    name: str

    def receive(self, pulse: Pulse, _: str):
        pass


def create_circuit(puzzle):
    circuit = {}
    for line in puzzle:
        source, dest = line.split(" -> ")
        circuit[source.strip("%&")] = dest.split(", ")
    return circuit


def create_module_name_mapping(puzzle, circuit):
    module_name_mapping = {}
    for line in puzzle:
        source, _ = line.split(" -> ")
        if source.startswith("%"):
            name = source[1:]
            module_name_mapping[name] = FlipFlop(name, False)
        elif source.startswith("&"):
            name = source[1:]
            inputs = [k for k, v in circuit.items() if name in v]
            module_name_mapping[name] = Conjunction(
                name, {n: Pulse.LOW for n in inputs}
            )
        else:
            module_name_mapping[source] = Relay(source)
    return module_name_mapping


def handle_button_clicks(circuit, module_name_mapping, times, critical_modules):
    pulses = {
        Pulse.LOW: 0,
        Pulse.HIGH: 0,
    }
    cycles = {t: 0 for t in critical_modules}
    tasks = queue.Queue()

    for i in itertools.count():
        if i == times:
            # pulses sent after {times} button presses
            yield pulses
        tasks.put(("broadcaster", Pulse.LOW))
        pulses[Pulse.LOW] += 1

        while not tasks.empty():
            source, pulse = tasks.get()
            targets = circuit[source]

            for target in targets:
                # source is connected to target(s)
                pulses[pulse] += 1
                if target not in module_name_mapping:
                    # target is not sending to any modules
                    continue
                module = module_name_mapping[target]
                if new_pulse := module.receive(pulse, source):
                    # target emits a pulse upon receiving from {source}
                    if module.name in critical_modules and new_pulse == Pulse.LOW:
                        # one of the critical mdoules emitted low pulse
                        # it means all its neighbours have high state
                        cycles[module.name] = i + 1
                        values = [v for v in cycles.values()]
                        if all(values):
                            # all critical modules reached
                            yield math.lcm(*values)
                    # put the new pulse in the queue
                    tasks.put((module.name, new_pulse))


circuit = create_circuit(puzzle)
module_name_mapping = create_module_name_mapping(puzzle, circuit)
critical_modules = ["lg", "gr", "bn", "st"]  # derived from the graph plotted below

results = handle_button_clicks(circuit, module_name_mapping, 1000, critical_modules)
print("1:", math.prod(next(results).values()))
print("2:", next(results))


def plot(puzzle, strip_broadcaster=False):
    graph = graphviz.Digraph()
    for line in puzzle:
        node_name, nodes = line.split(" -> ")
        nodes = nodes.split(", ")
        node_name = node_name.strip("&%")
        if strip_broadcaster and node_name == "broadcaster":
            continue
        for node in nodes:
            graph.edge(node_name, node)
    print(graph.render(directory="visual").replace("\\", "/"))


# plot(puzzle)
