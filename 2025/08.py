import bisect
import dataclasses
import itertools
import math
import operator

puzzle = [line for line in open("inputs/08.txt").read().strip().split("\n")]


@dataclasses.dataclass(frozen=True)
class Box:
    x: int
    y: int
    z: int

    def distance(self, box: "Box") -> float:
        return (
            (box.x - self.x) ** 2 + (box.y - self.y) ** 2 + (box.z - self.z) ** 2
        ) ** 0.5


@dataclasses.dataclass
class Circuit:
    boxes: set[Box]
    connections: set[frozenset[Box]]

    def __init__(self, box_1) -> None:
        self.boxes = {box_1}
        self.connections = set()

    def __len__(self) -> int:
        return len(self.boxes)

    def __in__(self, other: Box) -> bool:
        return other in self.boxes

    def connect(self, box_in, box_out) -> None:
        assert box_in in self.boxes, f"{box_in} not in circuit!"
        self.boxes.add(box_out)
        self.connections.add(frozenset({box_in, box_out}))


boxes = [Box(*[int(n) for n in line.split(",")]) for line in puzzle]


distances_sorted = []
for n1, n2 in itertools.combinations(boxes, 2):
    distance = n1.distance(n2)
    bisect.insort(distances_sorted, (distance, (n1, n2)), key=operator.itemgetter(0))

circuits = []
box_circuit_mapping = {}
for b in boxes:
    circuit = Circuit(b)
    circuits.append(circuit)
    box_circuit_mapping[b] = circuit


def calculate(distances_sorted, circuits, box_circuit_mapping, limit=None):
    for i, (_, (b1, b2)) in enumerate(distances_sorted, start=1):
        circuit_1 = box_circuit_mapping[b1]
        circuit_2 = box_circuit_mapping[b2]
        if circuit_1 is not circuit_2:
            circuit_1.boxes |= circuit_2.boxes
            circuit_1.connections |= circuit_2.connections
            circuit_1.connect(b1, b2)
            box_circuit_mapping[b1] = circuit_1
            box_circuit_mapping[b2] = circuit_1
            for b in circuit_2.boxes:
                box_circuit_mapping[b] = circuit_1
            circuits.remove(circuit_2)

        if i == limit:
            circuits.sort(key=lambda x: len(x), reverse=True)
            yield math.prod(len(c) for c in circuits[:3])
        if len(circuits) == 1:
            yield b1.x * b2.x


result = calculate(distances_sorted, circuits, box_circuit_mapping, 1000)
print("1:", next(result))
print("2:", next(result))
