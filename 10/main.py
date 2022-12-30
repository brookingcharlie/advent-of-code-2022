from sys import stdin
from dataclasses import dataclass
from functools import reduce

@dataclass
class Noop:
  pass

@dataclass
class Addx:
  operand: int

@dataclass
class State:
  cycle: int
  register: int

def parse_instructions(lines):
  def parse_instruction(line):
    if line == 'noop':
      return Noop()
    if (tokens := line.split())[0] == 'addx':
      return Addx(int(tokens[1]))
  return [parse_instruction(line) for line in lines]

def apply_instruction(state, instruction):
  match instruction:
    case Noop():
      return [State(state.cycle + 1, state.register)]
    case Addx(n):
      return [State(state.cycle + 1, state.register), State(state.cycle + 2, state.register + n)]

def run_program(instructions):
  def reducer(states, instruction):
    return states + apply_instruction(states[-1], instruction)
  return reduce(reducer, instructions, [State(0, 1)])

def get_signal_strength(states, cycle):
  return cycle * states[cycle - 1].register

def solve_puzzle(lines):
  instructions = parse_instructions(lines)
  states = run_program(instructions)
  return sum(get_signal_strength(states, cycle) for cycle in [20, 60, 100, 140, 180, 220])

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
