from sys import stdin

def parse_pair(line):
  return tuple(
    range(int((a := half.split('-'))[0]), int(a[1]) + 1)
    for half in line.split(',')
  )

def has_containment(pair):
  (s1, s2) = tuple(set(half) for half in pair)
  return set(s1).issubset(s2) or set(s2).issubset(s1)

def has_overlap(pair):
  return bool(set(pair[0]) & set(pair[1]))

def total(lines, predicate):
  pairs = [parse_pair(line) for line in lines]
  return len([pair for pair in pairs if predicate(pair)])

def main():
  lines = stdin.read().splitlines()
  print(total(lines, has_containment))
  print(total(lines, has_overlap))

if __name__ == "__main__":
    main()
