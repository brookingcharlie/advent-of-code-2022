import sys
from enum import Enum, auto
from dataclasses import dataclass, field, InitVar
from typing import ClassVar, Iterator
from itertools import cycle, islice, repeat

class Direction(Enum):
  RIGHT = auto()
  LEFT = auto()

@dataclass
class Cave:
  width: ClassVar[int] = 7
  start_x: ClassVar[int] = 2
  start_y_offset: ClassVar[int] = 3
  jets: InitVar[list[Direction]]
  jet_generator: Iterator[Direction] = None
  rocks: set[tuple[int, int]] = field(default_factory=set)
  height: int = 0

  def __post_init__(self, jets):
    self.jet_generator = cycle(jets)

  def add_rock(self, rock):
    pre_height = self.height
    start_y = pre_height + self.start_y_offset
    position = self.start_x, start_y
    min_x, max_x = 0, Cave.width - max(x for x, _ in rock) - 1
    for y in reversed(range(start_y + 1)):
      shift_x = -1 if next(self.jet_generator) == Direction.LEFT else 1
      x_move = (max(min_x, min(max_x, position[0] + shift_x)), y)
      if set((x_move[0] + x, x_move[1] + y) for (x, y) in rock).isdisjoint(self.rocks):
        position = x_move
      if y > 0:
        y_move = (position[0], y - 1)
        if set((y_move[0] + x, y_move[1] + y) for (x, y) in rock).isdisjoint(self.rocks):
          position = y_move
        else:
          break
    for (x, y) in rock:
      rock_point = (position[0] + x, position[1] + y)
      self.rocks.add(rock_point)
      self.height = max(self.height, rock_point[1] + 1)

  def draw(self):
    def line(y):
      return ('#' if (x, y) in self.rocks else '.' for x in range(Cave.width))
    lines = (f"|{''.join(line(y))}|" for y in reversed(range(self.height)))
    base = f"+{''.join(repeat('-', Cave.width))}+"
    return '\n'.join([*lines, base])

rock_shapes = [
  [(0, 0), (1, 0), (2, 0), (3, 0)],
  [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
  [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
  [(0, 0), (0, 1), (0, 2), (0, 3)],
  [(0, 0), (1, 0), (0, 1), (1, 1)]
]

def rock_generator(num_rocks):
  return islice(cycle(rock_shapes), num_rocks)

def parse_jets(line):
  lookup = {'<': Direction.LEFT, '>': Direction.RIGHT}
  return [lookup[char] for char in line]

def solve_puzzle(line, num_rocks):
  jets = parse_jets(line)
  cave = Cave(jets)
  for rock in rock_generator(num_rocks):
    cave.add_rock(rock)
  return cave.height

def main():
  line = sys.stdin.read().splitlines()[0]
  print(solve_puzzle(line, 2022))

if __name__ == "__main__":
  main()
