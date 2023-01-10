from enum import Enum, auto
from dataclasses import dataclass, field
import sys
import re

class Item(Enum):
  SENSOR = auto()
  BEACON = auto()

@dataclass
class Sensor:
  pos: tuple[int, int]
  beacon: tuple[int, int]
  distance: int = None

  def __post_init__(self):
    self.distance = sum(abs(self.beacon[i] - self.pos[i]) for i in [0, 1])

@dataclass
class Area:
  sensors: list[Sensor]
  __points: dict[tuple[int, int], Item] = field(default_factory=dict)
  __empty_ranges: dict[int, list[range]] = field(default_factory=dict)

  def __post_init__(self):
    for sensor in self.sensors:
      self.__points[sensor.pos] = Item.SENSOR
      self.__points[sensor.beacon] = Item.BEACON

  def __build_row_empty_ranges(self, y):
    if (ranges := self.__empty_ranges.get(y)) is not None:
      return ranges
    ranges = []
    for sensor in self.sensors:
      dy = abs(y - sensor.pos[1])
      if dy <= sensor.distance:
        dx = sensor.distance - dy
        ranges.append(range(sensor.pos[0] - dx, sensor.pos[0] + dx + 1))
    merged_ranges = merge_ranges(ranges)
    self.__empty_ranges[y] = merged_ranges
    return merged_ranges

  def num_empty(self, y):
    points_in_range = lambda r: sum(1 for (p_x, p_y) in self.__points if p_y == y and p_x in r)
    return sum(r.stop - r.start - points_in_range(r) for r in self.__build_row_empty_ranges(y))

  def tuning_frequency(self):
    (min_x, max_x) = min_max(self.sensors, lambda sensor: sensor.pos[0])
    (min_y, max_y) = min_max(self.sensors, lambda sensor: sensor.pos[1])
    for y in range(min_y, max_y + 1):
      ranges = self.__build_row_empty_ranges(y)
      if len(ranges) > 1:
        x = ranges[0].stop
        return 4000000 * x + y

  def draw(self):
    def build_all_empty_ranges():
      sensor_y_key = lambda sensor: (sensor.pos[1] - sensor.distance, sensor.pos[1] + sensor.distance)
      (min_y, max_y) = min_max(self.sensors, sensor_y_key)
      for y in range(min_y, max_y + 1):
        self.__build_row_empty_ranges(y)

    def get_char(point):
      match self.__points.get(point):
        case Item.SENSOR:
          return 'S'
        case Item.BEACON:
          return 'B'
        case None if any(point[0] in r for r in self.__empty_ranges[point[1]]):
          return '#'
        case None:
          return '.'

    build_all_empty_ranges()
    range_x_key = lambda y: min_max(self.__empty_ranges[y], lambda r: (r.start, r.stop - 1))
    (min_x, max_x) = min_max(self.__empty_ranges, range_x_key)
    (min_y, max_y) = min_max(self.__empty_ranges, lambda y: y)
    return [
      ''.join([get_char((x, y)) for x in range(min_x, max_x + 1)])
      for y in range(min_y, max_y + 1)
    ]

def merge_ranges(ranges):
  merged_ranges = []
  start, stop = None, None
  for r in sorted(ranges, key=lambda r: r.start):
    if start is None:
      start, stop = r.start, r.stop
    elif stop < r.start:
      merged_ranges.append(range(start, stop))
      start, stop = r.start, r.stop
    elif stop < r.stop:
      stop = r.stop
  if start is not None:
    merged_ranges.append(range(start, stop))
  return merged_ranges

def min_max(iterable, key):
  min_item, max_item = sys.maxsize, -sys.maxsize
  for item in iterable:
    match key(item):
      case (key_min, key_max):
        min_item, max_item = min(min_item, key_min), max(max_item, key_max)
      case key_val:
        min_item, max_item = min(min_item, key_val), max(max_item, key_val)
  return (min_item, max_item)

def parse_sensors(lines):
  def parse_sensor(line):
    regex = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
    coords = [int(match) for match in re.findall(regex, line)[0]]
    return Sensor(pos=(*coords[0:2],), beacon=(*coords[2:4],))
  return [parse_sensor(line) for line in lines]

def solve_puzzle(lines, y):
  area = Area(parse_sensors(lines))
  return (area.num_empty(y), area.tuning_frequency())

def main():
  lines = sys.stdin.read().splitlines()
  for solution in solve_puzzle(lines, 2000000):
    print(solution)

if __name__ == "__main__":
  main()
