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

  def __post_init__(self):
    self.__tiles_90 = list(zip(*reversed(self.tiles)))
    self.__tiles_180 = list(zip(*reversed(self.__tiles_90)))
    self.__tiles_270 = list(zip(*reversed(self.__tiles_180)))

  def get_tile(self, point):
    return self.tiles[point[0] - 1][point[1] - 1]

  def find_start_point(self):
    return next((1, j + 1) for (j, t) in enumerate(self.tiles[0]) if t == Tile.OPEN)

  @staticmethod
  def __move_right(tiles, start_i, start_j, distance):
    min_j = next(j for (j, t) in enumerate(tiles[start_i]) if t is not None)
    max_j = next((j for (j, t) in enumerate(tiles[start_i]) if j > start_j and t is None), len(tiles[start_i])) - 1
    wall_j = next((j for (j, t) in enumerate(tiles[start_i]) if j > start_j and t == Tile.WALL), sys.maxsize)
    end_j = min(start_j + distance, wall_j - 1)
    if end_j > max_j:
      return Board.__move_right(tiles, start_i, min_j, (distance % len(tiles[start_i])) - (max_j - start_j) - 1)
    return end_j

  def apply_action(self, start, action):
    ((start_row, start_col), start_facing) = start
    (start_i, start_j) = (start_row - 1, start_col - 1)
    match (start_facing, action):
      case (Facing.RIGHT, Move(distance)):
        end_j = Board.__move_right(self.tiles, start_i, start_j, distance)
        return ((start_row, end_j + 1), Facing.RIGHT)
      case (Facing.LEFT, Move(distance)):
        (start_i_180, start_j_180) = (len(self.tiles) - start_i - 1, len(self.tiles[start_i]) - start_j - 1)
        end_j_180 = Board.__move_right(self.__tiles_180, start_i_180, start_j_180, distance)
        end_j = len(self.tiles[start_i]) - end_j_180 - 1
        return ((start_row, end_j + 1), Facing.LEFT)
      case (Facing.DOWN, Move(distance)):
        (start_i_270, start_j_270) = (len(self.tiles[start_i]) - start_j - 1, start_i)
        end_j_270 = Board.__move_right(self.__tiles_270, start_i_270, start_j_270, distance)
        end_i = end_j_270
        return ((end_i + 1, start_col), Facing.DOWN)
      case (Facing.UP, Move(distance)):
        (start_i_90, start_j_90) = (start_j, len(self.tiles) - start_i - 1)
        end_j_90 = Board.__move_right(self.__tiles_90, start_i_90, start_j_90, distance)
        end_i = len(self.tiles) - end_j_90 - 1
        return ((end_i + 1, start_col), Facing.UP)
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
