from sys import stdin
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
import re

@dataclass
class Node(ABC):
  name: str
  @abstractmethod
  def total_size(self):
    pass

@dataclass
class File(Node):
  size: int
  def total_size(self):
    return self.size

@dataclass
class Dir(Node):
  children: list[Node]
  def total_size(self):
    return sum(child.total_size() for child in self.children)

def parse(lines):
  def reducer(stack, line):
    cd_match = re.findall(r'\$ cd (.*)', line)
    dir_match = re.findall(r'dir (.*)', line)
    file_match = re.findall(r'(\d+) (.*)', line)
    if cd_match == ['/']:
      return stack[0:1] or [Dir('/', [])]
    if cd_match == ['..']:
      return stack[:-1]
    if cd_match != []:
      return [*stack, next(c for c in stack[-1].children if c.name == cd_match[0])]
    if dir_match != []:
      stack[-1].children += [Dir(dir_match[0], [])]
    elif file_match != []:
      stack[-1].children += [File(file_match[0][1], int(file_match[0][0]))]
    return stack
  return reduce(reducer, lines, [])[0]

def find_dirs(dir, predicate):
  child_dirs = [child for child in dir.children if isinstance(child, Dir)]
  return (
    ([dir] if predicate(dir) else []) +
    [found for child in child_dirs for found in find_dirs(child, predicate)]
  )

def solve_puzzle_1(lines):
  root = parse(lines)
  predicate = lambda dir: dir.total_size() <= (MAX_SIZE := 100000)
  return sum(dir.total_size() for dir in find_dirs(root, predicate))

def solve_puzzle_2(lines):
  root = parse(lines)
  unused_space = (TOTAL_SPACE := 70000000) - root.total_size()
  deficit = (REQUIRED_SPACE := 30000000) - unused_space
  predicate = lambda dir: dir.total_size() >= deficit
  return min(dir.total_size() for dir in find_dirs(root, predicate))

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle_1(lines))
  print(solve_puzzle_2(lines))

if __name__ == "__main__":
  main()
