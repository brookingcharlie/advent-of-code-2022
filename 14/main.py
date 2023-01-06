from sys import stdin
from enum import Enum, auto
from dataclasses import dataclass, field, InitVar
from typing import ClassVar
from itertools import product, count

class Material(Enum):
  ROCK = auto()
  SAND = auto()

@dataclass
class Cave:
  sand_entry: ClassVar[tuple[int, int]] = (500, 0)
  rocks: InitVar[set[tuple[int, int]]]
  has_floor: InitVar[bool] = False
  __columns: dict[int, dict[int, Material]] = field(default_factory=dict)
  __floor_y: int = None

  def __post_init__(self, rocks, has_floor):
    for point in rocks:
      self.__add_point(point, Material.ROCK)
    self.__floor_y = max(y for (_, y) in rocks) + 2 if has_floor else None

  def __get_column(self, x):
    if (column := self.__columns.get(x)) is None:
      self.__columns[x] = (column := dict())
    return column

  def __add_point(self, point, material):
    self.__get_column(point[0])[point[1]] = material

  def __get_point(self, point):
    if self.__floor_y is not None and point[1] == self.__floor_y:
      return Material.ROCK
    if (column := self.__columns.get(point[0])) is None:
      return None
    return column.get(point[1])

  def __get_landing_point(self, x, start_y):
    if self.__get_point((x, start_y + 1)) is not None:
      return None
    y = min((y for y in self.__get_column(x).keys() if y > start_y + 1), default = self.__floor_y)
    return (x, y - 1) if y is not None else (x, None)

  def add_sand(self):
    if self.__get_point(self.sand_entry) is not None:
      return False
    current = self.sand_entry
    while True:
      moves = (self.__get_landing_point(current[0] + offset, current[1]) for offset in [0, -1, 1])
      move = next((move for move in moves if move is not None), None)
      if move is None:
        self.__add_point(current, Material.SAND)
        return True
      if move[1] is None:
        return False
      current = move

  def draw(self):
    def get_char(point):
      match self.__get_point(point):
        case Material.ROCK:
          return '#'
        case Material.SAND:
          return 'o'
        case _ if point == self.sand_entry:
          return '+'
        case _:
          return '.'
    min_x = min(self.__columns.keys())
    max_x = max(self.__columns.keys())),
    min_y = self.sand_entry[1]
    max_y = self.__floor_y or max(max(column.keys()) for column in self.__columns.values())
    return [
      ''.join([get_char((x, y)) for x in range(min_x, max_x + 1)])
      for y in range(min_y, max_y + 1)
    ]

def parse_rocks(lines):
  def parse_rock(line):
    path = [tuple(int(n) for n in point.split(',')) for point in line.split(' -> ')]
    return {
      (x, y)
      for ((a_x, a_y), (b_x, b_y)) in zip(path, path[1:])
      for (x, y) in product(
        range(min(a_x, b_x), max(a_x, b_x) + 1),
        range(min(a_y, b_y), max(a_y, b_y) + 1)
      )
    }
  return {(x, y) for line in lines for (x, y) in parse_rock(line)}

def solve_puzzle(lines):
  caves = [Cave(parse_rocks(lines)), Cave(parse_rocks(lines), has_floor = True)]
  return tuple(next(i for i in count() if not cave.add_sand()) for cave in caves)

def main():
  lines = stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
