import sys
from dataclasses import dataclass
from functools import cache
from math import ceil, prod
import re

@dataclass(frozen=True)
class Blueprint:
  blueprint_id: int
  costs: tuple[tuple[int]]

@dataclass(frozen=True)
class State:
  mins_left: [int]
  balance: tuple[int] = (0, 0, 0, 0)
  robots: tuple[int] = (1, 0, 0, 0)

  def __worth_buying(self, i, costs):
    return i == 3 or (
      self.mins_left > 2 and
      any(cost[i] * self.mins_left > self.robots[i] * self.mins_left + self.balance[i] for cost in costs)
    )

  def __mins_waiting_to_buy_robot(self, cost):
    if any(r == 0 and c != 0 for (r, c) in zip(self.robots, cost)):
      return None
    mins_waiting = max(max(0, ceil((c - b) / r)) for (b, r, c) in zip(self.balance, self.robots, cost) if c > 0) + 1
    return mins_waiting if mins_waiting < self.mins_left else None

  def __buy_robot_next_states(self, costs):
    return [
      State(
        self.mins_left - mins_waiting,
        tuple((b + r * mins_waiting - c) for (b, r, c) in zip(self.balance, self.robots, cost)),
        (*self.robots[:i], self.robots[i] + 1, *self.robots[i + 1:])
      )
      for (i, cost) in enumerate(costs)
      if self.__worth_buying(i, costs) and (mins_waiting := self.__mins_waiting_to_buy_robot(cost)) is not None
    ]

  def __do_nothing_next_state(self):
    return State(self.mins_left - 1, tuple((b + r) for (b, r) in zip(self.balance, self.robots)), self.robots)

  @cache
  def max_geodes(self, costs):
    if self.mins_left <= 1:
      return self.balance[3] + self.robots[3] * self.mins_left
    next_states = self.__buy_robot_next_states(costs) or [self.__do_nothing_next_state()]
    return max(s.max_geodes(costs) for s in next_states)

def parse_blueprints(lines):
  def parse_blueprint(line):
    blueprint_id = int(re.findall(r'Blueprint (\d+):', line)[0])
    ore_cost = int(re.findall(r'Each ore robot costs (\d+) ore.', line)[0])
    clay_cost = int(re.findall(r'Each clay robot costs (\d+) ore.', line)[0])
    obsidian_cost = [*map(int, re.findall(r'Each obsidian robot costs (\d+) ore and (\d+) clay.', line)[0])]
    geode_cost = [*map(int, re.findall(r'Each geode robot costs (\d+) ore and (\d+) obsidian.', line)[0])]
    return Blueprint(
      blueprint_id,
      (
        (ore_cost, 0, 0, 0),
        (clay_cost, 0, 0, 0),
        (obsidian_cost[0], obsidian_cost[1], 0, 0),
        (geode_cost[0], 0, geode_cost[1], 0),
      )
    )
  return [parse_blueprint(line) for line in lines]

def solve_puzzle(lines):
  blueprints = parse_blueprints(lines)
  return (
    sum([b.blueprint_id * State(24).max_geodes(b.costs) for b in blueprints]),
    prod([State(32).max_geodes(b.costs) for b in blueprints[:3]])
  )

def main():
  lines = sys.stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
