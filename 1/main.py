from sys import stdin
from functools import reduce

lines = stdin.read().splitlines()
def reducer(totals, line):
  if line == '':
    return [*totals, 0]
  elif len(totals) == 0:
    return [int(line)]
  else:
    return [*totals[:-1], totals[-1] + int(line)]
totals = reduce(reducer, lines, [])
print(max(totals))
