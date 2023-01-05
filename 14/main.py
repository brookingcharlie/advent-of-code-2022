from sys import stdin
from dataclasses import dataclass, field
from typing import ClassVar
from itertools import product

@dataclass
class Cave:
  sand_entry: ClassVar[tuple[int, int]] = (500, 0)
  rocks: set[tuple[int, int]]
  sand: set[tuple[int, int]] = field(default_factory=set)

  @property
  def bounds(self):
    return (
      (min(x for (x, y) in self.rocks), max(x for (x, y) in self.rocks)),
      (self.sand_entry[1], max(y for (x, y) in self.rocks))
    )

  def add_sand(self):
    obstacles = self.rocks | self.sand
    def try_move(start, offset):
      possible_x = start[0] + offset
      possible_y = min((y - 1 for (x, y) in obstacles if x == possible_x and y > start[1]), default = None)
      return (possible_x, possible_y) if possible_y is None or possible_y > start[1] else None
    current = self.sand_entry
    while True:
      moves = (try_move(current, offset) for offset in [0, -1, 1])
      move = next((move for move in moves if move is not None), None)
      if move is None:
        self.sand.add(current)
        return True
      if move[1] is None:
        return False
      current = move

  def draw(self):
    def get_char(coords):
      match coords:
        case self.sand_entry:
          return '+'
        case coords if coords in self.rocks:
          return '#'
        case coords if coords in self.sand:
          return 'o'
        case _:
          return '.'
    result = [
      ''.join([get_char((x, y)) for x in range(self.bounds[0][0], self.bounds[0][1] + 1)])
      for y in range(self.bounds[1][0], self.bounds[1][1] + 1)
    ]
    return result

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
  cave = Cave(parse_rocks(lines))
  while (cave.add_sand()):
    pass
  return len(cave.sand)

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
