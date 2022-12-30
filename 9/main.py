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

def parse_moves(lines):
  direction_by_token = {
    'R': Direction.RIGHT,
    'L': Direction.LEFT,
    'U': Direction.UP,
    'D': Direction.DOWN
  }
  def parse_move(line):
    tokens = line.split()
    return Move(direction_by_token[tokens[0]], int(tokens[1]))
  return [parse_move(line) for line in lines]

def move_head(position, move):
  match move:
    case Move(Direction.RIGHT, distance):
      return [(position[0] + n, position[1]) for n in range(1, 1 + distance)]
    case Move(Direction.LEFT, distance):
      return [(position[0] - n, position[1]) for n in range(1, 1 + distance)]
    case Move(Direction.UP, distance):
      return [(position[0], position[1] + n) for n in range(1, 1 + distance)]
    case Move(Direction.DOWN, distance):
      return [(position[0], position[1] - n) for n in range(1, 1 + distance)]

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
    new_tail_position = step_tail(tail_positions[-1], head_position)
    return tail_positions + ([new_tail_position] if new_tail_position else [])
  return reduce(reducer, head_positions[1:], head_positions[:1])

def solve_puzzle(lines, num_knots):
  head_positions = project(parse_moves(lines))
  tail_positions = reduce(lambda positions, _: track(positions), range(num_knots - 1), head_positions)
  return len(set(tail_positions))

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines, 2))
  print(solve_puzzle(lines, 10))

if __name__ == "__main__":
  main()
