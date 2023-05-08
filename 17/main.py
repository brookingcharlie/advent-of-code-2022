import sys
from enum import Enum, auto
from dataclasses import dataclass, field, InitVar
from typing import ClassVar, Iterator
from itertools import cycle, islice, repeat

@dataclass
class Cave:
  __width: ClassVar[int] = 7
  __start_x: ClassVar[int] = 2
  __start_y_offset: ClassVar[int] = 3
  __band_size: ClassVar[int] = 50

  jets: InitVar[list[int]]
  height: int = 0

  __jet_generator: Iterator[int] = None
  __rocks: set[tuple[int, int]] = field(default_factory=set)
  __patterns_seen: dict[tuple[frozenset[tuple[int, int]], int, int], tuple[int, int]] = field(default_factory=dict)
  __repeated_band: tuple[int, int] = None

  def __post_init__(self, jets):
    self.__jet_generator = cycle(enumerate(jets))

  def add_rocks(self, rock_shapes, num_rocks):
    rock_generator = enumerate(islice(cycle(rock_shapes), num_rocks))
    num_repeated_bands, repeated_band_rocks, repeated_band_height = None, None, None
    for rock in rock_generator:
      if num_repeated_bands and rock[0] + num_repeated_bands * repeated_band_rocks == num_rocks:
        self.height += num_repeated_bands * repeated_band_height
        break
      self.__add_rock(rock, len(rock_shapes))
      if num_repeated_bands is None and self.__repeated_band:
        repeated_band_rocks, repeated_band_height = self.__repeated_band
        num_repeated_bands = (num_rocks - rock[0]) // repeated_band_rocks

  def __add_rock(self, rock, num_rock_shapes):
    position = self.__find_position(rock, num_rock_shapes)
    self.__commit_rock(position, rock)

  def __find_position(self, rock, num_rock_shapes):
    min_x, max_x = 0, Cave.__width - max(x for (x, _) in rock[1]) - 1
    start_y = self.height + self.__start_y_offset
    position = (self.__start_x, start_y)
    for (y, jet) in zip(reversed(range(start_y + 1)), self.__jet_generator):
      if y == start_y:
        self.__check_for_repeat(y, rock, num_rock_shapes, jet)
      x_move = (max(min_x, min(max_x, position[0] + jet[1])), y)
      if self.__unobstructed(x_move, rock):
        position = x_move
      y_move = (position[0], y - 1)
      if y_move[1] >= 0 and self.__unobstructed(y_move, rock):
        position = y_move
      else:
        break
    return position

  def __check_for_repeat(self, y, rock, num_rock_shapes, jet):
    if not self.__repeated_band:
      band = frozenset((x, self.height - y) for (x, y) in self.__rocks if self.height - y < self.__band_size),
      scenario = (band, rock[0] % num_rock_shapes, jet[0])
      if scenario in self.__patterns_seen:
        (rocks_seen, height_seen) = self.__patterns_seen[scenario]
        self.__repeated_band = (rock[0] - rocks_seen, self.height - height_seen)
      else:
        self.__patterns_seen[scenario] = (rock[0], self.height)

  def __unobstructed(self, position, rock):
    return set((position[0] + x, position[1] + y) for (x, y) in rock[1]).isdisjoint(self.__rocks)

  def __commit_rock(self, position, rock):
    for (x, y) in rock[1]:
      rock_point = (position[0] + x, position[1] + y)
      self.__rocks.add(rock_point)
      self.height = max(self.height, rock_point[1] + 1)

  def draw(self):
    def line(y):
      return ('#' if (x, y) in self.__rocks else '.' for x in range(Cave.__width))
    lines = (f"|{''.join(line(y))}|" for y in reversed(range(self.height)))
    base = f"+{''.join(repeat('-', Cave.__width))}+"
    return '\n'.join([*lines, base])

rock_shapes = [
  [(0, 0), (1, 0), (2, 0), (3, 0)],
  [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
  [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
  [(0, 0), (0, 1), (0, 2), (0, 3)],
  [(0, 0), (1, 0), (0, 1), (1, 1)]
]

def parse_jets(line):
  lookup = {'<': -1, '>': 1}
  return [lookup[char] for char in line]

def solve_puzzle(line, num_rocks):
  jets = parse_jets(line)
  cave = Cave(jets)
  cave.add_rocks(rock_shapes, num_rocks)
  return cave.height

def main():
  line = sys.stdin.read().splitlines()[0]
  print(solve_puzzle(line, 2022))
  print(solve_puzzle(line, 1000000000000))

if __name__ == "__main__":
  main()
