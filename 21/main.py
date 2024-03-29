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

def parse_line(line):
  [(name, expression)] = re.findall(r'(\w+): (.+)', line)
  return (name, parse_expression(expression))

def parse_lines(lines):
  monkeys = [parse_line(line) for line in lines]
  return {name: expression for (name, expression) in monkeys}

def find_variables(scope, root, leaf):
  variables = [leaf]
  current = leaf
  while current != root:
    parent = next(
      name for (name, expression) in scope.items()
      if type(expression) == Operation and current in [expression.left.name, expression.right.name]
    )
    variables.append(parent)
    current = parent
  variables.reverse()
  return variables

def solve_part_1(scope):
  return scope['root'].evaluate(scope)

def solve_part_2(scope):
  variables = find_variables(scope, 'root', 'humn')
  root: Operation = scope['root']
  answer = (root.left if root.right.name in variables else root.right).evaluate(scope)
  for variable in variables[1:-1]:
    operation = scope[variable]
    match operation.operator:
      case Operator.ADD:
        solve = lambda answer, constant, constant_on_left: answer - constant
      case Operator.SUBTRACT:
        solve = lambda answer, constant, constant_on_left: constant - answer if constant_on_left else answer + constant
      case Operator.MULTIPLY:
        solve = lambda answer, constant, constant_on_left: answer // constant
      case Operator.DIVIDE:
        solve = lambda answer, constant, constant_on_left: constant // answer if constant_on_left else answer * constant
    (constant, constant_on_left) = (operation.left, True) if operation.right.name in variables else (operation.right, False)
    answer = solve(answer, constant.evaluate(scope), constant_on_left)
  return answer

def solve_puzzle(lines):
  scope = parse_lines(lines)
  return (solve_part_1(scope), solve_part_2(scope))

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
