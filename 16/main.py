import sys
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import product

@dataclass
class Valve:
  label: str
  rate: int
  leads_to: list[str]

def parse_valves(lines):
  def parse_valve(line):
    [label, rate_str, *leads_to] = re.findall(r'\b[A-Z0-9]+\b', line)
    return Valve(label, int(rate_str), leads_to)
  valves = [parse_valve(line) for line in lines]
  return {v.label: v for v in valves}

def infer_shortcuts(valve_map, start):
  def shortest(a, b, dist=0, seen=set()):
    if b.label in a.leads_to:
      return dist + 1
    return min([s for l in a.leads_to if l not in seen and (s := shortest(valve_map[l], b, dist + 1, {*seen, a.label}))], default=None)
  return {
    a.label: {b.label: s + 1 for b in valve_map.values() if a != b and b.rate > 0 and (s := shortest(a, b))}
    for a in valve_map.values() if a.label == start or a.rate > 0
  }

def find_solution(valve_map, time, num_actors=1):
  start = 'AA'
  shortcuts = infer_shortcuts(valve_map, start)
  @cache
  def generate_options(time, open_valves, position):
    result = []
    current_rate = sum(valve_map[valve].rate for valve in open_valves)
    possible_new_positions = [p for p in shortcuts[position] if p not in open_valves and time > shortcuts[position][p]]
    result.append((time * current_rate, open_valves))
    for new_position in possible_new_positions:
      new_open_valves = frozenset([*open_valves, new_position])
      new_time = time - shortcuts[position][new_position]
      for option in generate_options(new_time, new_open_valves, new_position):
        result.append((shortcuts[position][new_position] * current_rate + option[0], option[1]))
    return result
  options = generate_options(time, frozenset(), start)
  if num_actors == 1:
    return max(total for (total, _) in options)
  elif num_actors == 2:
    return max(t1 + t2 for ((t1, o1), (t2, o2)) in product(options, options) if o1.isdisjoint(o2))

def solve_puzzle(lines):
  valve_map = parse_valves(lines)
  return (find_solution(valve_map, 30), find_solution(valve_map, 26, 2))

def main():
  lines = sys.stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
