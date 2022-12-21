from sys import stdin
from functools import reduce

def get_totals(lines):
  def reducer(totals, line):
    if line == '':
      return [*totals, 0]
    elif len(totals) == 0:
      return [int(line)]
    else:
      return [*totals[:-1], totals[-1] + int(line)]
  return reduce(reducer, lines, [])

def main():
  lines = stdin.read().splitlines()
  totals = get_totals(lines)
  print(max(totals))
  print(sum(sorted(totals)[-3:]))

if __name__ == "__main__":
    main()
