import sys
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

class Tile(Enum):
  OPEN = auto()
  WALL = auto()

class Rotate(Enum):
  LEFT = auto()
  RIGHT = auto()

class Facing(Enum):
  LEFT = auto()
  RIGHT = auto()
  UP = auto()
  DOWN  = auto()

class Action(ABC):
  pass

@dataclass
class Move(Action):
  distance: int

@dataclass
class Turn(Action):
  direction: Rotate

@dataclass
class Board():
  tiles: list[list[Tile]]
  __x_flipped_tiles: list[list[Tile]] = None
  __y_flipped_tiles: list[list[Tile]] = None

  def __post_init__(self):
    self.__x_flipped_tiles = [
      [self.tiles[i][len(self.tiles[i]) - j - 1]
      for j in range(len(self.tiles[i]))]
      for i in range(len(self.tiles))
    ]
    self.__y_flipped_tiles = [
      [self.tiles[len(self.tiles) - i - 1][j]
      for j in range(len(self.tiles[i]))]
      for i in range(len(self.tiles))
    ]

  def get_tile(self, point):
    return self.tiles[point[0] - 1][point[1] - 1]

  def find_start_point(self):
    return next((1, j + 1) for (j, t) in enumerate(self.tiles[0]) if t == Tile.OPEN)

  @staticmethod
  def __move_right(tiles, start_i, start_j, distance):
    min_j = next(j for j in range(len(tiles[start_i])) if tiles[start_i][j] is not None)
    max_j = next(
      (j - 1 for j in range(start_j, len(tiles[start_i])) if tiles[start_i][j] is None),
      len(tiles[start_i]) - 1
    )
    wall_j = next(
      (j for j in range(start_j + 1, len(tiles[start_i])) if tiles[start_i][j] == Tile.WALL),
      sys.maxsize
    )
    end_j = min(start_j + distance, wall_j - 1)
    if end_j > max_j:
      moved = max_j - start_j + 1
      return Board.__move_right(tiles, start_i, min_j, distance - moved)
    return end_j

  @staticmethod
  def __move_down(tiles, start_i, start_j, distance):
    min_i = next(i for i in range(len(tiles)) if tiles[i][start_j] is not None)
    max_i = next(
      (i - 1 for i in range(start_i, len(tiles)) if tiles[i][start_j] is None),
      len(tiles) - 1
    )
    wall_i = next(
      (i for i in range(start_i + 1, len(tiles)) if tiles[i][start_j] == Tile.WALL),
      sys.maxsize
    )
    end_i = min(start_i + distance, wall_i - 1)
    if end_i > max_i:
      moved = max_i - start_i + 1
      return Board.__move_down(tiles, min_i, start_j, distance - moved)
    return end_i

  def apply_action(self, start, action):
    ((start_row, start_col), start_facing) = start
    (start_i, start_j) = (start_row - 1, start_col - 1)
    match (start_facing, action):
      case (Facing.RIGHT, Move(distance)):
        end_j = Board.__move_right(self.tiles, start_i, start_j, distance)
        return ((start_i + 1, end_j + 1), Facing.RIGHT)
      case (Facing.LEFT, Move(distance)):
        flipped_start_j = len(self.tiles[start_i]) - start_j - 1
        flipped_end_j = Board.__move_right(self.__x_flipped_tiles, start_i, flipped_start_j, distance)
        unflipped_end_j = len(self.tiles[start_i]) - flipped_end_j - 1
        return ((start_i + 1, unflipped_end_j + 1), Facing.LEFT)
      case (Facing.DOWN, Move(distance)):
        end_i = Board.__move_down(self.tiles, start_i, start_j, distance)
        return ((end_i + 1, start_j + 1), Facing.DOWN)
      case (Facing.UP, Move(distance)):
        flipped_start_i = len(self.tiles) - start_i - 1
        flipped_end_i = Board.__move_down(self.__y_flipped_tiles, flipped_start_i, start_j, distance)
        unflipped_end_i = len(self.tiles) - flipped_end_i - 1
        return ((unflipped_end_i + 1, start_j + 1), Facing.UP)
      case (Facing.UP, Turn(Rotate.RIGHT)): return ((start_row, start_col), Facing.RIGHT)
      case (Facing.RIGHT, Turn(Rotate.RIGHT)): return ((start_row, start_col), Facing.DOWN)
      case (Facing.DOWN, Turn(Rotate.RIGHT)): return ((start_row, start_col), Facing.LEFT)
      case (Facing.LEFT, Turn(Rotate.RIGHT)): return ((start_row, start_col), Facing.UP)
      case (Facing.UP, Turn(Rotate.LEFT)): return ((start_row, start_col), Facing.LEFT)
      case (Facing.LEFT, Turn(Rotate.LEFT)): return ((start_row, start_col), Facing.DOWN)
      case (Facing.DOWN, Turn(Rotate.LEFT)): return ((start_row, start_col), Facing.RIGHT)
      case (Facing.RIGHT, Turn(Rotate.LEFT)): return ((start_row, start_col), Facing.UP)

def parse_board(lines):
  def char_to_tile(c):
    match c:
      case ' ': return None
      case '.': return Tile.OPEN
      case '#': return Tile.WALL
  unpadded_tiles = [[char_to_tile(c) for c in line] for line in lines]
  width = max(len(row) for row in unpadded_tiles)
  tiles = [row + [None] * (width - len(row)) for row in unpadded_tiles]
  return Board(tiles)

def draw_board(board):
  def tile_to_char(t):
    match t:
      case None: return ' '
      case Tile.OPEN: return '.'
      case Tile.WALL: return '#'
  return [''.join([tile_to_char(t) for t in row]) for row in board.tiles]

def parse_path(line):
  def char_to_direction(c):
    match c:
      case 'L': return Rotate.LEFT
      case 'R': return Rotate.RIGHT
  return [
    Move(int(s)) if s.isdigit() else Turn(char_to_direction(s))
    for s in re.findall(r'\d+|L|R', line)
  ]

def parse_input(lines):
  return (parse_board(lines[:-2]), parse_path(lines[-1]))

def calculate_password(state):
  match state[1]:
    case Facing.RIGHT: facing_number = 0
    case Facing.DOWN: facing_number = 1
    case Facing.LEFT: facing_number = 2
    case Facing.UP: facing_number = 3
  return 1000 * state[0][0] + 4 * state[0][1] + facing_number

def solve_puzzle(lines):
  (board, path) = parse_input(lines)
  state = (board.find_start_point(), Facing.RIGHT)
  for action in path:
    state = board.apply_action(state, action)
  return calculate_password(state)

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
