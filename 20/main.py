import sys
from math import floor

def parse_numbers(lines, decryption_key):
  return [int(line) * decryption_key for line in lines]

def mix_number(mixed, item):
  i = mixed.index(item)
  j = (i + item[1]) % (len(mixed) - 1)
  if i == 0 and j == 0:
    return mixed
  j = len(mixed) - 1 if j == 0 else j
  mixed.remove(item)
  mixed.insert(j, item)
  return mixed

def mix_numbers(numbers, iterations):
  enumerated = list(enumerate(numbers))
  mixed = enumerated.copy()
  for _ in range(iterations):
    for item in enumerated:
      mix_number(mixed, item)
  return [n for (_, n) in mixed]

def solve_puzzle_part(lines, decryption_key, iterations):
  numbers = parse_numbers(lines, decryption_key)
  mixed = mix_numbers(numbers, iterations)
  zero_i = mixed.index(0)
  return sum(mixed[(zero_i + offset) % len(mixed)] for offset in [1000, 2000, 3000])

def solve_puzzle(lines):
  return (solve_puzzle_part(lines, 1, 1), solve_puzzle_part(lines, 811589153, 10))

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
