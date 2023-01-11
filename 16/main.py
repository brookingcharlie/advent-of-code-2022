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
  return [parse_valve(line) for line in lines]

def find_solution(all_valves, time, num_actors=1):
  valve_map = {v.label: v for v in all_valves}
  @cache
  def find_max(time_left, open_valves, positions):
    if time_left == 0:
      return 0
    combined_rate = sum(valve_map[valve].rate for valve in open_valves)
    if len(open_valves) == len(all_valves):
      return time_left * combined_rate
    possible_next_steps = product(*([('open', v), *[('move', l) for l in valve_map[v].leads_to]] for v in positions))
    options = []
    for next_step in possible_next_steps:
      to_open = frozenset([part[1] for part in next_step if part[0] == 'open'])
      new_open_valves = frozenset([*open_valves, *to_open]) if not to_open.issubset(open_valves) else open_valves
      new_positions = tuple(sorted(part[1] if part[0] == 'move' else positions[i] for (i, part) in enumerate(next_step)))
      if new_open_valves != open_valves or new_positions != positions:
        options.append(find_max(time_left - 1, new_open_valves, new_positions))
    return combined_rate + max(options, default=0)
  start = 'AA'
  open_valves = frozenset(valve.label for valve in all_valves if valve.rate == 0)
  return find_max(time, open_valves, tuple(start for _ in range(num_actors)))

def solve_puzzle(lines):
  all_valves = parse_valves(lines)
  return (find_solution(all_valves, 30), find_solution(all_valves, 26, 2))

def main():
  lines = sys.stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
