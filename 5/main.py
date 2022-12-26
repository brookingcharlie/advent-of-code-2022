from sys import stdin
from functools import reduce
import re

def parse_sections(lines):
  def reducer(sections, line):
    return (
      [*sections, []] if line == '' else
      [[line]] if sections == [] else
      [*sections[:-1], [*sections[-1], line]]
    )
  return reduce(reducer, lines, [])

def parse_stacks(lines):
  num_stacks = (len(lines[0]) + 1) // 4
  def reducer(stacks, line):
    items = [*line[1:num_stacks * 4:4]]
    return [[*stack, item] if item != ' ' else stack for (stack, item) in zip(stacks, items)]
  return reduce(reducer, reversed(lines[:-1]), [[]] * num_stacks)

def parse_moves(lines):
  matches = [re.findall(r"move (\d+) from (\d) to (\d)", line)[0] for line in lines]
  return [(int(match[0]), int(match[1]) - 1, int(match[2]) - 1) for match in matches]

def move_maker(in_reverse):
  def make_move(stacks, move):
    (num_items, from_stack, to_stack) = move
    removed_items = stacks[from_stack][-1 * num_items:]
    added_items = list(reversed(removed_items)) if in_reverse else removed_items
    return [
      stacks[i][:-1 * num_items] if i == from_stack else
      stacks[i] + added_items if i == to_stack else
      stacks[i]
      for i in range(len(stacks))
    ]
  return make_move

def solve_puzzle(lines, in_reverse):
  sections = parse_sections(lines)
  starting_stacks = parse_stacks(sections[0])
  moves = parse_moves(sections[1])
  ending_stacks = reduce(move_maker(in_reverse), moves, starting_stacks)
  return ''.join([stack[-1] for stack in ending_stacks])

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines, True))
  print(solve_puzzle(lines, False))

if __name__ == "__main__":
    main()
