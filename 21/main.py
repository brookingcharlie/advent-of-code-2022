import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import re

@dataclass
class Expression(ABC):
  @abstractmethod
  def evaluate(self, scope):
    pass

@dataclass
class Number(Expression):
  value: int

  def evaluate(self, scope):
    return self.value

class Operator(Enum):
  ADD = auto()
  SUBTRACT = auto()
  MULTIPLY = auto()
  DIVIDE = auto()

@dataclass
class Reference(Expression):
  name: str

  def evaluate(self, scope):
    return scope[self.name].evaluate(scope)

@dataclass
class Operation(Expression):
  operator: Operator
  left: Reference
  right: Reference

  def evaluate(self, scope):
    match self.operator:
      case Operator.ADD:
        return self.left.evaluate(scope) + self.right.evaluate(scope)
      case Operator.SUBTRACT:
        return self.left.evaluate(scope) - self.right.evaluate(scope)
      case Operator.MULTIPLY:
        return self.left.evaluate(scope) * self.right.evaluate(scope)
      case Operator.DIVIDE:
        return self.left.evaluate(scope) // self.right.evaluate(scope)

@dataclass
class Monkey():
  name: str
  expression: Expression

def parse_operator(s):
  match s:
    case '+':
      return Operator.ADD
    case '-':
      return Operator.SUBTRACT
    case '*':
      return Operator.MULTIPLY
    case '/':
      return Operator.DIVIDE

def parse_expression(s):
  if match := re.findall(r'(\d+)', s):
    return Number(int(match[0]))
  elif match := re.findall(r'(\w+) (\+|\-|\*|\/) (\w+)', s):
    return Operation(parse_operator(match[0][1]), Reference(match[0][0]), Reference(match[0][2]))

def parse_monkey(line):
  [(name, expr)] = re.findall(r'(\w+): (.+)', line)
  return Monkey(name, parse_expression(expr))

def parse_monkeys(lines):
  return [parse_monkey(line) for line in lines]

def solve_puzzle(lines):
  monkeys = parse_monkeys(lines)
  scope = {monkey.name: monkey.expression for monkey in monkeys}
  return scope['root'].evaluate(scope)

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
