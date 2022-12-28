from sys import stdin
from dataclasses import dataclass
from functools import reduce
from itertools import count, product
from operator import mul

@dataclass
class Tree:
  id: int
  height: int

def parse(lines):
  id_gen = count(0)
  return [[Tree(next(id_gen), int(c)) for c in line] for line in lines]

def find_visible_1(traversal):
  def reducer(state, tree):
    (found, highest) = state
    return ((found | {tree.id}) if tree.height > highest else found, max(highest, tree.height))
  return reduce(reducer, traversal, (set(), -1))[0]

def solve_puzzle_1(lines):
  rows = parse(lines)
  traversals = (
    rows +
    [list(reversed(row)) for row in rows] +
    (columns := [[row[i] for row in rows] for i in range(len(rows[0]))]) +
    [list(reversed(column)) for column in columns]
  )
  return len({id for traversal in traversals for id in find_visible_1(traversal)})

def find_visible_2(starting_height, traversal):
  stop_at = next((tree_at[0] + 1 for tree_at in enumerate(traversal) if tree_at[1].height >= starting_height), None)
  return {tree.id for tree in traversal[:stop_at]}

def solve_puzzle_2(lines):
  rows = parse(lines)
  def reducer(highest_score, index):
    traversals = [
      rows[index[0]][index[1] + 1:],
      list(reversed(rows[index[0]][:index[1]])),
      [row[index[1]] for row in rows[index[0] + 1:]],
      list(reversed([row[index[1]] for row in rows[:index[0]]]))
    ]
    tree = rows[index[0]][index[1]]
    distances = [len(find_visible_2(tree.height, traversal)) for traversal in traversals]
    score = reduce(mul, distances, 1)
    return max(highest_score, score)
  indexes = product(range(len(rows)), range(len(rows[0])))
  return reduce(reducer, indexes, -1)

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle_1(lines))
  print(solve_puzzle_2(lines))

if __name__ == "__main__":
  main()
