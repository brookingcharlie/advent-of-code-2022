from sys import stdin
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from operator import mul
import re

@dataclass
class Operation(ABC):
  @abstractmethod
  def apply(self, worry_level) -> int:
    pass

@dataclass
class Add(Operation):
  operand: int
  def apply(self, worry_level):
    return worry_level + self.operand

@dataclass
class Multiply(Operation):
  operand: int
  def apply(self, worry_level):
    return worry_level * self.operand

@dataclass
class Square(Operation):
  def apply(self, worry_level):
    return worry_level * worry_level

@dataclass
class Test:
  divisor: int
  throw_to: dict[bool, int]
  def apply(self, worry_level):
    return self.throw_to[worry_level % self.divisor == 0]

@dataclass
class Monkey:
  id: int
  items: list[int]
  operation: Operation
  test: Test
  num_inspections: int = 0
  def take_turn(self, monkies, relieve):
    for _ in range(len(self.items)):
      worry_level = relieve(self.operation.apply(self.items.pop(0)))
      monkies[self.test.apply(worry_level)].receive_item(worry_level) 
      self.num_inspections += 1
  def receive_item(self, item):
    self.items.append(item)

def parse_sections(lines):
  def reducer(sections, line):
    return (
      [*sections, []] if line == '' else
      [[line]] if sections == [] else
      [*sections[:-1], [*sections[-1], line]]
    )
  return reduce(reducer, lines, [])

def parse_operation(line):
  match re.findall(r'new = old (\+|\*) (\d+|old)', line)[0]:
    case ('+', operand):
      return Add(int(operand))
    case ('*', 'old'):
      return Square()
    case ('*', operand):
      return Multiply(int(operand))

def parse_monkey(lines):
  id = int(re.findall(r'Monkey (\d+)', lines[0])[0])
  items = [int(token) for token in re.findall(r'\d+', lines[1])]
  operation = parse_operation(lines[2])
  test_params = [int(re.findall(r'\d+', line)[0]) for line in lines[3:]]
  test = Test(test_params[0], {True: test_params[1], False: test_params[2]})
  return Monkey(id, items, operation, test)

def parse_monkies(lines):
  return [parse_monkey(section) for section in parse_sections(lines)]

def play_game(monkies, num_rounds, relieve):
  for _ in range(num_rounds):
    for monkey in monkies:
      monkey.take_turn(monkies, relieve)

def solve_puzzle(lines, num_rounds, relieve = None):
  monkies = parse_monkies(lines)
  if relieve is None:
    n = reduce(mul, [monkey.test.divisor for monkey in monkies], 1)
    relieve = lambda worry_level: worry_level % n
  play_game(monkies, num_rounds, relieve)
  highest = sorted(monkey.num_inspections for monkey in monkies)[-2:]
  return highest[0] * highest[1]

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines, 20, lambda worry_level: worry_level // 3))
  print(solve_puzzle(lines, 10000))

if __name__ == "__main__":
  main()
