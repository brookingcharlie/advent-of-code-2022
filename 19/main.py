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

@cache
def compute_max_geodes(mins_left, robots, balance, robot_costs):
  if mins_left == 0:
    return balance[3]
  if mins_left == 1:
    return balance[3] + robots[3]
  inert_state = State(robots, tuple((b + r) for (b, r) in zip(balance, robots)))
  spend_states = [
    State(
      (*robots[:i], robots[i] + 1, *robots[i + 1:]),
      tuple((b + r - c) for (b, r, c) in zip(balance, robots, cost))
    )
    for (i, cost) in enumerate(robot_costs)
    if (
      all(b >= c for (b, c) in zip(balance, cost)) and
      (i == 3 or mins_left > 2) and
      (i == 3 or any(robot_cost[i] * mins_left > robots[i] * mins_left + balance[i] for robot_cost in robot_costs))
    )
  ]
  next_states = [inert_state, *spend_states]
  return max(compute_max_geodes(mins_left - 1, s.robots, s.balance, robot_costs) for s in next_states)

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
  compute_max_geodes.cache_clear()
  state = State()
  return compute_max_geodes(24, state.robots, state.balance, blueprint.robot_costs)

def solve_puzzle(lines):
  blueprints = parse_blueprints(lines)
  return sum([b.blueprint_id * max_geodes(b) for b in blueprints])

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
