import sys
from dataclasses import dataclass
from functools import cache
import re

@dataclass(frozen=True)
class Blueprint:
  blueprint_id: int
  robot_costs: tuple[tuple[int]]

@dataclass(frozen=True)
class State:
  robots: tuple[int] = (1, 0, 0, 0)
  balance: tuple[int] = (0, 0, 0, 0)

  def next_states(self, blueprint):
    return compute_next_states(self.robots, self.balance, blueprint.robot_costs)

@cache
def compute_next_states(robots, balance, robot_costs):
  inert_state = State(robots, tuple((b + r) for (b, r) in zip(balance, robots)))
  spend_states = [
    State(
      (*robots[:i], robots[i] + 1, *robots[i + 1:]),
      tuple((b + r - c) for (b, r, c) in zip(balance, robots, cost))
    )
    for (i, cost) in enumerate(robot_costs)
    if all(b >= c for (b, c) in zip(balance, cost))
  ]
  return set([inert_state, *spend_states])

def parse_blueprints(lines):
  def parse_blueprint(line):
    blueprint_id = int(re.findall(r'Blueprint (\d+):', line)[0])
    ore_robot_cost = int(re.findall(r'Each ore robot costs (\d+) ore.', line)[0])
    clay_robot_cost = int(re.findall(r'Each clay robot costs (\d+) ore.', line)[0])
    obsidian_robot_cost = [*map(int, re.findall(r'Each obsidian robot costs (\d+) ore and (\d+) clay.', line)[0])]
    geode_robot_cost = [*map(int, re.findall(r'Each geode robot costs (\d+) ore and (\d+) obsidian.', line)[0])]
    return Blueprint(
      blueprint_id,
      (
        (ore_robot_cost, 0, 0, 0),
        (clay_robot_cost, 0, 0, 0),
        (obsidian_robot_cost[0], obsidian_robot_cost[1], 0, 0),
        (geode_robot_cost[0], 0, geode_robot_cost[1], 0),
      )
    )
  return [parse_blueprint(line) for line in lines]

def max_geodes(blueprint):
  compute_next_states.cache_clear()
  states = set([State()])
  for i in range(24):
    states = set(x for xs in [s.next_states(blueprint) for s in states] for x in xs)
  return max(s.balance[3] for s in states)

def solve_puzzle(lines):
  blueprints = parse_blueprints(lines)
  return sum([b.blueprint_id * max_geodes(b) for b in blueprints])

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
