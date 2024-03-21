from unittest import TestCase
from main import Blueprint, State, parse_blueprints, max_geodes, solve_puzzle

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

  def test_state_0(self):
    self.assertEqual(State(), State((1, 0, 0, 0), (0, 0, 0, 0)))

  def test_next_states_1(self):
    state = State()
    actual = state.next_states(parse_blueprints(Test.lines)[0])
    expected = set([
      State((1, 0, 0, 0), (1, 0, 0, 0)),
    ])
    self.assertEqual(actual, expected)

  def test_next_states_2(self):
    state = State((1, 0, 0, 0), (1, 0, 0, 0))
    actual = state.next_states(parse_blueprints(Test.lines)[0])
    expected = set([
      State((1, 0, 0, 0), (2, 0, 0, 0)),
    ])
    self.assertEqual(actual, expected)

  def test_next_states_3(self):
    state = State((1, 0, 0, 0), (2, 0, 0, 0))
    actual = state.next_states(parse_blueprints(Test.lines)[0])
    expected = set([
      State((1, 0, 0, 0), (3, 0, 0, 0)),
      State((1, 1, 0, 0), (1, 0, 0, 0)),
    ])
    self.assertEqual(actual, expected)

  def test_next_states_18(self):
    state = State((1, 4, 2, 0), (3, 13, 8, 0))
    actual = state.next_states(parse_blueprints(Test.lines)[0])
    expected = set([
      State((1, 4, 2, 0), (4, 17, 10, 0)),
      State((1, 5, 2, 0), (2, 17, 10, 0)),
      State((1, 4, 2, 1), (2, 17, 3, 0)),
    ])
    self.assertEqual(actual, expected)

  def test_next_states_19(self):
    state = State((1, 4, 2, 1), (2, 17, 3, 0))
    actual = state.next_states(parse_blueprints(Test.lines)[0])
    expected = set([
      State((1, 4, 2, 1), (3, 21, 5, 1)),
      State((1, 5, 2, 1), (1, 21, 5, 1)),
    ])
    self.assertEqual(actual, expected)

  def test_next_states_20(self):
    state = State((1, 4, 2, 1), (3, 21, 5, 1))
    actual = state.next_states(parse_blueprints(Test.lines)[0])
    expected = set([
      State((1, 4, 2, 1), (4, 25, 7, 2)),
      State((1, 5, 2, 1), (2, 25, 7, 2)),
      State((1, 4, 3, 1), (1, 11, 7, 2)),
    ])
    self.assertEqual(actual, expected)

  def test_max_geodes_blueprint_1(self):
    self.assertEqual(max_geodes(parse_blueprints(Test.lines)[0]), 9)

  def test_max_geodes_blueprint_2(self):
    self.assertEqual(max_geodes(parse_blueprints(Test.lines)[1]), 12)

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), 33)
