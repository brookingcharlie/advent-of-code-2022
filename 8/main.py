from sys import stdin
from functools import reduce
from itertools import count

def parse(lines):
  id_gen = count(1)
  return [[(next(id_gen), int(c)) for c in line] for line in lines]

def find_visible(traversal):
  def reducer(state, tree):
    (found, highest) = state
    (id, height) = tree
    return ((found | {id}) if height > highest else found, max(highest, height))
  return reduce(reducer, traversal, (set(), -1))[0]

def solve_puzzle(lines):
  traversals = (
    (rows := parse(lines)) +
    [list(reversed(row)) for row in rows] +
    (columns := [[row[i] for row in rows] for i in range(len(rows[0]))]) +
    [list(reversed(column)) for column in columns]
  )
  return len({id for traversal in traversals for id in find_visible(traversal)})

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
