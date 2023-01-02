from sys import stdin
from itertools import zip_longest
from functools import reduce
from operator import mul

def parse_list(chars):
  if chars[0] != '[':
    return None
  result = []
  while chars != []:
    if chars[0] == '[':
      chars.pop(0)
    if chars[0] == ',':
      chars.pop(0)
    if (number := parse_number(chars)) is not None:
      result.append(number)
    if (nested_list := parse_list(chars)) is not None:
      result.append(nested_list)
    if chars[0] == ']':
      chars.pop(0)
      return result

def parse_number(chars):
  if not chars[0].isdigit():
    return None
  result = 0
  while chars != []:
    if chars[0].isdigit():
      result = result * 10 + int(chars.pop(0))
    else:
      return result

def parse_pairs(lines):
  return [
    tuple(parse_list(list(line)) for line in lines[i:i + 2])
    for i in range(0, len(lines), 3)
  ]

def in_order(pair):
  for values in zip_longest(*pair):
    match values:
      case None, _:
        return True
      case _, None:
        return False
      case int(a), int(b):
        if a < b:
          return True
        if a > b:
          return False
      case list(a), list(b):
        if (answer := in_order((a, b))) is not None:
          return answer
      case int(a), list(b):
        if (answer := in_order(([a], b))) is not None:
          return answer
      case list(a), int(b):
        if (answer := in_order((a, [b]))) is not None:
          return answer

def solve_part_1(pairs):
  pairs_in_order = [in_order(pair) for pair in pairs]
  return sum(i + 1 for i in range(len(pairs_in_order)) if pairs_in_order[i])

def quicksort(a, lo, hi):
  if lo < 0 or lo >= hi:
    return
  p = partition(a, lo, hi)
  quicksort(a, lo, p - 1)
  quicksort(a, p + 1, hi)

def partition(a, lo, hi):
  pivot = a[hi]
  i = lo - 1
  for j in range(lo, hi):
    if in_order((a[j], pivot)) != False:
      i += 1
      a[i], a[j] = a[j], a[i]
  i += 1
  a[i], a[hi] = a[hi], a[i]
  return i

def solve_part_2(pairs):
  dividers = [[[2]], [[6]]]
  packets = [packet for pair in pairs for packet in pair] + dividers
  quicksort(packets, 0, len(packets) - 1)
  return reduce(mul, [packets.index(divider) + 1 for divider in dividers], 1)

def solve_puzzle(lines):
  pairs = parse_pairs(lines)
  return (solve_part_1(pairs), solve_part_2(pairs))

def main():
  lines = stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
