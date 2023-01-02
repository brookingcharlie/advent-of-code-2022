from sys import stdin
from itertools import zip_longest

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

def solve_puzzle(lines):
  pairs_in_order = [in_order(pair) for pair in parse_pairs(lines)]
  return sum(i + 1 for i in range(len(pairs_in_order)) if pairs_in_order[i])

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
