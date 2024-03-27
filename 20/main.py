import sys
from math import floor

def parse_numbers(lines):
  return [int(line) for line in lines]

def mix_number(mixed, item):
  i = mixed.index(item)
  j = (i + item[1]) % (len(mixed) - 1)
  if i == 0 and j == 0:
    return mixed
  j = len(mixed) - 1 if j == 0 else j
  mixed.remove(item)
  mixed.insert(j, item)
  return mixed

def mix_numbers(numbers):
  enumerated = list(enumerate(numbers))
  mixed = enumerated.copy()
  for item in enumerated:
    mix_number(mixed, item)
  return [n for (_, n) in mixed]

def solve_puzzle(lines):
  numbers = parse_numbers(lines)
  mixed = mix_numbers(numbers)
  zero_i = mixed.index(0)
  return sum(mixed[(zero_i + offset) % len(mixed)] for offset in [1000, 2000, 3000])

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
