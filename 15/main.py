from enum import Enum, auto
from dataclasses import dataclass, field
import sys
import re

class Item(Enum):
  SENSOR = auto()
  BEACON = auto()

@dataclass
class Sensor:
  position: tuple[int, int]
  closest_beacon: tuple[int, int]

  def distance(self):
    return sum(abs(self.closest_beacon[i] - self.position[i]) for i in [0, 1])

@dataclass
class Area:
  sensors: list[Sensor]
  __points: dict[tuple[int, int], Item] = field(default_factory=dict)
  __empty_ranges: dict[int, list[range]] = field(default_factory=dict)

  def __post_init__(self):
    for sensor in self.sensors:
      self.__points[sensor.position] = Item.SENSOR
      self.__points[sensor.closest_beacon] = Item.BEACON

  def __build_row_empty_ranges(self, y):
    if (ranges := self.__empty_ranges.get(y)) is not None:
      return ranges
    ranges = []
    for sensor in self.sensors:
      distance = sensor.distance()
      dy = abs(y - sensor.position[1])
      if dy <= distance:
        dx = distance - dy
        ranges.append(range(sensor.position[0] - dx, sensor.position[0] + dx + 1))
    merged_ranges = self.__merge_ranges(ranges)
    self.__empty_ranges[y] = merged_ranges
    return merged_ranges

  def __merge_ranges(self, ranges):
    if len(ranges) == 0:
      return ranges
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

  def __build_all_empty_ranges(self):
    min_y, max_y = sys.maxsize, -sys.maxsize
    for sensor in self.sensors:
      distance = sensor.distance()
      min_y = min(min_y, sensor.position[1] - distance)
      max_y = max(max_y, sensor.position[1] + distance)
    for y in range(min_y, max_y + 1):
      self.__build_row_empty_ranges(y)

  def num_empty(self, y):
    points_in_range = lambda r: sum(1 for (p_x, p_y) in self.__points if p_y == y and p_x in r)
    return sum(r.stop - r.start - points_in_range(r) for r in self.__build_row_empty_ranges(y))

  def tuning_frequency(self):
    (min_x, max_x), (min_y, max_y) = (sys.maxsize, -sys.maxsize), (sys.maxsize, -sys.maxsize)
    for sensor in self.sensors:
      min_x, max_x = min(min_x, sensor.position[0]), max(max_x, sensor.position[0])
      min_y, max_y = min(min_y, sensor.position[1]), max(max_y, sensor.position[1])
    for y in range(min_y, max_y + 1):
      ranges = self.__build_row_empty_ranges(y)
      if len(ranges) > 1:
        for x in range(min_x, max_x + 1):
          if not any(x in r for r in ranges) and (x, y) not in self.__points:
            return 4000000 * x + y

  def draw(self):
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
    self.__build_all_empty_ranges()
    (min_x, max_x), (min_y, max_y) = (sys.maxsize, -sys.maxsize), (sys.maxsize, -sys.maxsize)
    for x, y in self.__points:
      min_x, max_x = min(min_x, x), max(max_x, x)
      min_y, max_y = min(min_y, y), max(max_y, y)
    for y in self.__empty_ranges:
      min_x = min(min_x, min(r.start for r in self.__empty_ranges[y]))
      max_x = max(max_x, max(r.stop - 1 for r in self.__empty_ranges[y]))
      min_y, max_y = min(min_y, y), max(max_y, y)
    return [
      ''.join([get_char((x, y)) for x in range(min_x, max_x + 1)])
      for y in range(min_y, max_y + 1)
    ]

def parse_sensors(lines):
  def parse_sensor(line):
    regex = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
    coords = [int(match) for match in re.findall(regex, line)[0]]
    return Sensor(position=(*coords[0:2],), closest_beacon=(*coords[2:4],))
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
