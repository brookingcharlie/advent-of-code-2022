import sys
import re

def parse_cubes(lines):
  return [tuple(int(n) for n in re.findall(r'\d+', line)) for line in lines]

def solve_puzzle(lines):
  cubes = set(parse_cubes(lines))
  def sides_exposed(cube):
    deltas = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    adjacent_points = [tuple(map(sum, zip(cube, delta))) for delta in deltas]
    return sum(1 for p in adjacent_points if p not in cubes)
  return sum(sides_exposed(cube) for cube in cubes)

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
