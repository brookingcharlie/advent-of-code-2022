import sys
import re
from dataclasses import dataclass, field
from functools import cache

@dataclass(unsafe_hash=True)
class Valve:
  label: str
  rate: int
  leads_to_labels: frozenset[str]
  leads_to: frozenset['Valve'] = field(default_factory=frozenset)

def parse_valves(lines):
  def parse_valve(line):
    [label, rate_str, *leads_to_labels] = re.findall(r'\b[A-Z0-9]+\b', line)
    return Valve(label, int(rate_str), frozenset(leads_to_labels))
  valves = [parse_valve(line) for line in lines]
  for valve in valves:
    valve.leads_to = frozenset(next(v for v in valves if v.label == l) for l in valve.leads_to_labels)
  return valves

def find_solution(all_valves, time):
  @cache
  def find_max(time_left, open_valves, valve):
    if time_left == 0:
      return 0
    combined_rate = sum(v.rate for v in open_valves)
    if len(open_valves) == len(all_valves):
      return time_left * combined_rate
    options = []
    if valve not in open_valves:
      options.append(find_max(time_left - 1, frozenset([*open_valves, valve]), valve))
    for new_valve in valve.leads_to:
      options.append(find_max(time_left - 1, open_valves, new_valve))
    return combined_rate + max(options, default=0)
  start = next(v for v in all_valves if v.label == 'AA')
  open_valves = frozenset(v for v in all_valves if v.rate == 0)
  return find_max(time, open_valves, start)

def solve_puzzle(lines):
  all_valves = parse_valves(lines)
  return find_solution(all_valves, 30)

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
