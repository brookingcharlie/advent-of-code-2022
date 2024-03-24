from unittest import TestCase
from main import Blueprint, State, parse_blueprints, solve_puzzle

class Test(TestCase):
  lines = [
    (
      'Blueprint 1:' +
      ' Each ore robot costs 4 ore.' +
      ' Each clay robot costs 2 ore.' +
      ' Each obsidian robot costs 3 ore and 14 clay.' +
      ' Each geode robot costs 2 ore and 7 obsidian.'
    ),
    (
      'Blueprint 2:' +
      ' Each ore robot costs 2 ore.' +
      ' Each clay robot costs 3 ore.' +
      ' Each obsidian robot costs 3 ore and 8 clay.' +
      ' Each geode robot costs 3 ore and 12 obsidian.'
    ),
  ]

  def test_parse_blueprints(self):
    actual = parse_blueprints(Test.lines)
    expected = [
      Blueprint(1, ((4, 0, 0, 0), (2, 0, 0, 0), (3, 14, 0, 0), (2, 0, 7, 0))),
      Blueprint(2, ((2, 0, 0, 0), (3, 0, 0, 0), (3, 8, 0, 0), (3, 0, 12, 0))),
    ]
    self.assertEqual(actual, expected)

  def test_max_geodes_blueprint_1(self):
    self.assertEqual(State().max_geodes(parse_blueprints(Test.lines)[0].costs), 9)

  def test_max_geodes_blueprint_2(self):
    self.assertEqual(State().max_geodes(parse_blueprints(Test.lines)[1].costs), 12)

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), 33)
