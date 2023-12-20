import dataclasses
import enum
import itertools
import math
import queue

# import graphviz


puzzle = [line for line in open("inputs/20.txt").read().strip().split("\n")]

target_mapping = {"lg": "rr", "gr": "js", "bn": "bs", "st": "zb"}


class Pulse(str, enum.Enum):
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


node = None


@dataclasses.dataclass
class Conjunction:
    name: str
    inputs: dict

    def receive(self, pulse: Pulse, source: str):
        self.inputs[source] = pulse
        if all([p == Pulse.HIGH for p in self.inputs.values()]):
            if self.name in target_mapping:
                global node
                node = self.name
            return Pulse.LOW
        return Pulse.HIGH

    @property
    def watches(self):
        return len(self.inputs)


@dataclasses.dataclass
class Relay:
    name: str

    def receive(self, pulse: Pulse, _: str):
        pass


def create_circuit(puzzle):
    circuit = {}
    for line in puzzle:
        source, dest = line.split(" -> ")
        if source[0] in "%&":
            source = source[1:]
        circuit[source] = dest.split(", ")
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


candidates = ["js", "bs", "rr", "zb"]
early_candidates = ["lg", "gr", "bn", "st"]
starters = ["nd", "fx", "mc", "lf"]

found = {t: 0 for t in target_mapping}


def handle_button_click(circuit, module_name_mapping, times):
    pulses = {
        Pulse.LOW: 0,
        Pulse.HIGH: 0,
    }
    tasks = queue.Queue()
    for i in itertools.count(start=1):
        global node
        if node:
            print(node, i)
            found[node] = i
            node = None
        if all(found.values()):
            print([v for v in found.values()])
            result = math.prod([v - 1 for v in found.values()])
            print(result)
            assert result in range(224981741117232, 226106087649552)
            return
        if i % 100000 == 0:
            print(i)
        tasks.put(("broadcaster", Pulse.LOW))
        pulses[Pulse.LOW] += 1
        while not tasks.empty():
            source, pulse = tasks.get()
            targets = circuit[source]
            if source in target_mapping and target == target_mapping[source]:
                input(f"{source=} {target=} {i=} {pulse=}")
            for target in targets:
                pulses[pulse] += 1
                if module := module_name_mapping.get(target, None):
                    if new_pulse := module.receive(pulse, source):
                        tasks.put((module.name, new_pulse))

    return pulses


circuit = create_circuit(puzzle)
module_name_mapping = create_module_name_mapping(puzzle, circuit)
dummies = set()
for targets in circuit.values():
    for t in targets:
        if t not in circuit:
            dummies.add(t)


pulses = handle_button_click(circuit, module_name_mapping, 1000)

result_1 = pulses[Pulse.LOW] * pulses[Pulse.HIGH]
print("1:", result_1)

LOWW = 224981741117232
HIGH = 226106087649552

# def plot(puzzle, strip_broadcast=False):
#     dot = graphviz.Digraph()
#     for line in puzzle:
#         node_name, _, nodes = line.partition(" -> ")
#         nodes = nodes.split(", ")
#         node_name = node_name.strip("&%")
#         if strip_broadcast and node_name == "broadcaster":
#             continue
#         for node in nodes:
#             dot.edge(node_name, node)
#         # print(node_name, nodes)
#     print(dot.render(directory="visual").replace("\\", "/"))
#
# plot(puzzle)
