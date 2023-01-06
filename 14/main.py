from sys import stdin
from dataclasses import dataclass, field
from typing import ClassVar
from itertools import product

@dataclass
class Cave:
  sand_entry: ClassVar[tuple[int, int]] = (500, 0)
  rocks: set[tuple[int, int]]
  sand: set[tuple[int, int]] = field(default_factory=set)
  has_floor: bool = False

  @property
  def bounds(self):
    obstacles = self.rocks | self.sand
    return (
      (min(x for (x, y) in obstacles), max(x for (x, y) in obstacles)),
      (self.sand_entry[1], max(y for (x, y) in obstacles))
    )

  def add_sand(self):
    if self.sand_entry in self.sand:
      return False
    obstacles = self.rocks | self.sand
    floor_y = max(y for (_, y) in self.rocks) + 2 if self.has_floor else None
    def try_move(start, offset):
      if (start[0] + offset, start[1] + 1) in obstacles or self.has_floor and start[1] + 1 == floor_y:
        return None
      end_x = start[0] + offset
      end_y = min((y for (x, y) in obstacles if x == end_x and y > start[1] + 1), default = floor_y)
      return (end_x, end_y - 1 if end_y is not None else None)
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
    floor_y = max(y for (_, y) in self.rocks) + 2
    def get_char(coords):
      match coords:
        case coords if coords in self.rocks or self.has_floor and coords[1] == floor_y:
          return '#'
        case coords if coords in self.sand:
          return 'o'
        case self.sand_entry:
          return '+'
        case _:
          return '.'
    ((min_x, max_x), (min_y, max_y)) = self.bounds
    result = [
      ''.join([get_char((x, y)) for x in range(min_x, max_x + 1)])
      for y in range(min_y, max_y + 1 + (1 if self.has_floor else 0))
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
  cave_1 = Cave(parse_rocks(lines))
  while (cave_1.add_sand()):
    pass
  cave_2 = Cave(parse_rocks(lines), has_floor = True)
  while (cave_2.add_sand()):
    pass
  return (len(cave_1.sand), len(cave_2.sand))

def main():
  lines = stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
