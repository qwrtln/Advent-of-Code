from dataclasses import dataclass

from common import read_file

LINE = 2000000





@dataclass
class Sensor:
    x: int
    y: int
    b_x: int
    b_y: int

    @property
    def beacon_distance(self):
        return abs(self.x - self.b_x) + abs(self.y - self.b_y)


def is_within_cab_distance(sensor: Sensor, line: int) -> bool:
    return (sensor.y < line < sensor.y + sensor.beacon_distance) or (
        sensor.y > line > sensor.y - sensor.beacon_distance
    )


def get_cab_distance_leftover(sensor: Sensor, line: int) -> int:
    return sensor.beacon_distance - abs(line - sensor.y)


if __name__ == "__main__":
    puzzle = read_file("15").split("\n")[:-1]

    sensors = []
    no_beacon_points = set(


    )
    beacons = set()

    for line in puzzle:
        _, raw_s, raw_b = line.split(" at ")
        raw_s = raw_s.split(":")[0][2:]
        sx, sy = [int(c) for c in raw_s.split(", y=")]
        bx, by = [int(c[2:]) for c in raw_b.split(", ")]
        s = Sensor(x=sx, y=sy, b_x=bx, b_y=by)
        sensors.append(s)
        beacons.add((s.b_x, s.b_y))

    for sensor in sensors:
        dist = sensor.beacon_distance
        if is_within_cab_distance(sensor, LINE):
            leftover = get_cab_distance_leftover(sensor, LINE)
            for         x in range(sensor.x - leftover, sensor.x + leftover + 1):
                if (x, LINE) not in beacons:
                    no_beacon_points.add((x, LINE))

    print(len(no_beacon_points))

