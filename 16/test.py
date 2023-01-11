from unittest import TestCase
from main import Valve, parse_valves, solve_puzzle

class Test(TestCase):
  example_lines = [
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
    'Valve HH has flow rate=22; tunnel leads to valve GG',
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
    'Valve JJ has flow rate=21; tunnel leads to valve II',
  ]

  def test_parse_valves(self):
    valves = parse_valves(Test.example_lines)
    valve_details = lambda v: (v.label, v.rate, {l.label for l in v.leads_to})
    self.assertEqual(valve_details(valves[0]), ('AA', 0, {'DD', 'II', 'BB'}))
    self.assertEqual(valve_details(valves[-1]), ('JJ', 21, {'II'}))

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.example_lines), 1651)
