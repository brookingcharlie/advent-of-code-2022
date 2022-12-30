from unittest import TestCase
from main import (
  Noop, Addx, State, parse_instructions, apply_instruction, run_program, get_signal_strength,
  is_pixel_lit, solve_puzzle
)

class Test(TestCase):
  def test_parse_instructions(self):
    lines = ['noop', 'addx 3', 'addx -5']
    expected = [Noop(), Addx(3), Addx(-5)]
    self.assertEqual(parse_instructions(lines), expected)

  def test_apply_instruction(self):
    self.assertEqual(apply_instruction(State(1, 2), Noop()), [State(2, 2)])
    self.assertEqual(apply_instruction(State(7, -2), Addx(5)), [State(8, -2), State(9, 3)])
    self.assertEqual(apply_instruction(State(2, 3), Addx(-8)), [State(3, 3), State(4, -5)])

  def test_run_program(self):
    instructions = [Addx(-2), Noop(), Addx(10)]
    expected = [State(0, 1), State(1, 1), State(2, -1), State(3, -1), State(4, -1), State(5, 9)]
    self.assertEqual(run_program(instructions), expected)

  def test_get_signal_strength(self):
    states = [State(0, 1), State(1, 1), State(2, -1), State(3, -1), State(4, -1), State(5, 9)]
    self.assertEqual(get_signal_strength(states, 2), 2)
    self.assertEqual(get_signal_strength(states, 3), -3)
    self.assertEqual(get_signal_strength(states, 5), -5)

  def test_is_pixel_lit(self):
    states = [State(0, 0), State(1, 1), State(2, 16), State(3, 16), State(4, 5), State(5, 5)]
    self.assertEqual(is_pixel_lit(states, 0), True)
    self.assertEqual(is_pixel_lit(states, 1), True)
    self.assertEqual(is_pixel_lit(states, 2), False)
    self.assertEqual(is_pixel_lit(states, 3), False)
    self.assertEqual(is_pixel_lit(states, 4), True)

  def test_solve_puzzle(self):
    lines = [
      'addx 15',
      'addx -11',
      'addx 6',
      'addx -3',
      'addx 5',
      'addx -1',
      'addx -8',
      'addx 13',
      'addx 4',
      'noop',
      'addx -1',
      'addx 5',
      'addx -1',
      'addx 5',
      'addx -1',
      'addx 5',
      'addx -1',
      'addx 5',
      'addx -1',
      'addx -35',
      'addx 1',
      'addx 24',
      'addx -19',
      'addx 1',
      'addx 16',
      'addx -11',
      'noop',
      'noop',
      'addx 21',
      'addx -15',
      'noop',
      'noop',
      'addx -3',
      'addx 9',
      'addx 1',
      'addx -3',
      'addx 8',
      'addx 1',
      'addx 5',
      'noop',
      'noop',
      'noop',
      'noop',
      'noop',
      'addx -36',
      'noop',
      'addx 1',
      'addx 7',
      'noop',
      'noop',
      'noop',
      'addx 2',
      'addx 6',
      'noop',
      'noop',
      'noop',
      'noop',
      'noop',
      'addx 1',
      'noop',
      'noop',
      'addx 7',
      'addx 1',
      'noop',
      'addx -13',
      'addx 13',
      'addx 7',
      'noop',
      'addx 1',
      'addx -33',
      'noop',
      'noop',
      'noop',
      'addx 2',
      'noop',
      'noop',
      'noop',
      'addx 8',
      'noop',
      'addx -1',
      'addx 2',
      'addx 1',
      'noop',
      'addx 17',
      'addx -9',
      'addx 1',
      'addx 1',
      'addx -3',
      'addx 11',
      'noop',
      'noop',
      'addx 1',
      'noop',
      'addx 1',
      'noop',
      'noop',
      'addx -13',
      'addx -19',
      'addx 1',
      'addx 3',
      'addx 26',
      'addx -30',
      'addx 12',
      'addx -1',
      'addx 3',
      'addx 1',
      'noop',
      'noop',
      'noop',
      'addx -9',
      'addx 18',
      'addx 1',
      'addx 2',
      'noop',
      'noop',
      'addx 9',
      'noop',
      'noop',
      'noop',
      'addx -1',
      'addx 2',
      'addx -37',
      'addx 1',
      'addx 3',
      'noop',
      'addx 15',
      'addx -21',
      'addx 22',
      'addx -6',
      'addx 1',
      'noop',
      'addx 2',
      'addx 1',
      'noop',
      'addx -10',
      'noop',
      'noop',
      'addx 20',
      'addx 1',
      'addx 2',
      'addx 2',
      'addx -6',
      'addx -11',
      'noop',
      'noop',
      'noop'
    ]
    (actual_1, actual_2) = solve_puzzle(lines)
    expected_1 = 13140
    expected_2 = [
      '##..##..##..##..##..##..##..##..##..##..',
      '###...###...###...###...###...###...###.',
      '####....####....####....####....####....',
      '#####.....#####.....#####.....#####.....',
      '######......######......######......####',
      '#######.......#######.......#######.....'
    ]
    self.assertEqual(actual_1, expected_1)
    self.assertEqual(actual_2, expected_2)
