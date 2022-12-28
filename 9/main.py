from sys import stdin
from enum import Enum, auto
from dataclasses import dataclass
from functools import reduce

class Direction(Enum):
  RIGHT = auto()
  LEFT = auto()
  UP = auto()
  DOWN = auto()

@dataclass
class Move:
  direction: Direction
  distance: int

def parse(lines):
  direction_by_token = {
    'R': Direction.RIGHT,
    'L': Direction.LEFT,
    'U': Direction.UP,
    'D': Direction.DOWN
  }
  def parse_line(line):
    tokens = line.split()
    return Move(direction_by_token[tokens[0]], int(tokens[1]))
  return [parse_line(line) for line in lines]

def move_head(position, move):
  match move:
    case Move(Direction.RIGHT, distance):
      return [(position[0] + n, position[1]) for n in range(1, distance + 1)]
    case Move(Direction.LEFT, distance):
      return [(position[0] - n, position[1]) for n in range(1, distance + 1)]
    case Move(Direction.UP, distance):
      return [(position[0], position[1] + n) for n in range(1, distance + 1)]
    case Move(Direction.DOWN, distance):
      return [(position[0], position[1] - n) for n in range(1, distance + 1)]

def project(moves):
  def reducer(positions, move):
    return positions + move_head(positions[-1], move)
  return reduce(reducer, moves, [(0, 0)])

def step_tail(tail_position, head_position):
  (tx, ty), (hx, hy) =  tail_position, head_position
  (dx, dy) = (abs(hx - tx), abs(hy - ty))
  if dx <= 1 and dy <= 1:
    return None
  if dx == 0:
    return (tx, ty + (hy - ty) // dy)
  if dy == 0:
    return (tx + (hx - tx) // dx, ty)
  return (tx + (hx - tx) // dx, ty + (hy - ty) // dy)

def track(head_positions):
  def reducer(tail_positions, head_position):
    tail_position = step_tail(tail_positions[-1], head_position)
    return tail_positions + ([tail_position] if tail_position else [])
  return reduce(reducer, head_positions, [(0, 0)])

def solve_puzzle_1(lines):
  head_moves = parse(lines)
  head_positions = project(head_moves)
  tail_positions = track(head_positions)
  return len(set(tail_positions))

def solve_puzzle_2(lines):
  head_moves = parse(lines)
  head_positions = project(head_moves)
  tail_positions = reduce(lambda head, _: track(head), range(9), head_positions)
  return len(set(tail_positions))

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle_1(lines))
  print(solve_puzzle_2(lines))

if __name__ == "__main__":
  main()
