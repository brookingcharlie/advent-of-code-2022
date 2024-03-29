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

  @abstractmethod
  def solve(self, scope, variables, answer):
    pass

@dataclass
class Number(Expression):
  value: int

  def evaluate(self, scope):
    return self.value

  def solve(self, scope, variables, answer):
    return answer

class Operator(Enum):
  ADD = auto()
  SUBTRACT = auto()
  MULTIPLY = auto()
  DIVIDE = auto()

@dataclass
class Operation(Expression):
  operator: Operator
  left: str
  right: str

  def evaluate(self, scope):
    match self.operator:
      case Operator.ADD:
        return scope[self.left].evaluate(scope) + scope[self.right].evaluate(scope)
      case Operator.SUBTRACT:
        return scope[self.left].evaluate(scope) - scope[self.right].evaluate(scope)
      case Operator.MULTIPLY:
        return scope[self.left].evaluate(scope) * scope[self.right].evaluate(scope)
      case Operator.DIVIDE:
        return scope[self.left].evaluate(scope) // scope[self.right].evaluate(scope)

  def solve(self, scope, variables, answer):
    match self.operator:
      case Operator.ADD:
        variable_answer = (
          answer - scope[self.right].evaluate(scope) if self.left in variables else
          answer - scope[self.left].evaluate(scope)
        )
      case Operator.SUBTRACT:
        variable_answer = (
          answer + scope[self.right].evaluate(scope) if self.left in variables else
          scope[self.left].evaluate(scope) - answer
        )
      case Operator.MULTIPLY:
        variable_answer = (
          answer // scope[self.right].evaluate(scope) if self.left in variables else
          answer // scope[self.left].evaluate(scope)
        )
      case Operator.DIVIDE:
        variable_answer = (
          answer * scope[self.right].evaluate(scope) if self.left in variables else
          scope[self.left].evaluate(scope) // answer
        )
    variable_operation = scope[self.left if self.left in variables else self.right]
    return variable_operation.solve(scope, variables, variable_answer)

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
    return Operation(parse_operator(match[0][1]), match[0][0], match[0][2])

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
      if type(expression) == Operation and current in [expression.left, expression.right]
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
  answer = scope[root.left if root.left not in variables else root.right].evaluate(scope)
  return scope[variables[1]].solve(scope, variables, answer)

def solve_puzzle(lines):
  scope = parse_lines(lines)
  return (solve_part_1(scope), solve_part_2(scope))

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
