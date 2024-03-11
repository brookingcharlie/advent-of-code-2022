import sys
import re

def parse_cubes(lines):
  return set(tuple(int(n) for n in re.findall(r'\d+', line)) for line in lines)

def adjacent_points(point):
  deltas = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
  return set(tuple(map(sum, zip(point, delta))) for delta in deltas)

def create_bounding_box(cubes):
  return tuple((min(d) - 1, max(d) + 1) for d in [[c[i] for c in cubes] for i in range(3)])

def outside_bounding_box(bounding_box, point):
  return any(p < b[0] or p > b[1] for (p, b) in zip(point, bounding_box))

def solve_puzzle_1(cubes):
  return sum(len(adjacent_points(cube) - cubes) for cube in cubes)

def solve_puzzle_2(cubes):
  bounding_box = create_bounding_box(cubes)
  start_point = tuple(b[0] for b in bounding_box)
  remaining_points = set([start_point])
  visited_points = set()
  surface_area = 0
  while len(remaining_points) > 0:
    point = remaining_points.pop()
    reachable_points = set(
      p for p in adjacent_points(point)
      if not outside_bounding_box(bounding_box, p) and p not in visited_points
    )
    reachable_cubes = reachable_points.intersection(cubes)
    remaining_points.update(reachable_points.difference(reachable_cubes))
    visited_points.add(point)
    surface_area += len(reachable_cubes)
  return surface_area

def solve_puzzle(lines):
  cubes = parse_cubes(lines)
  return (solve_puzzle_1(cubes), solve_puzzle_2(cubes))

def main():
  lines = sys.stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
