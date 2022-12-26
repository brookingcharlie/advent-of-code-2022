from unittest import TestCase
from main import parse_sections, parse_stacks, parse_moves, move_maker, solve_puzzle

class Test(TestCase):
  def test_parse_sections(self):
    lines = ['aa', 'bb', '', 'cc', 'dd', 'ee']
    expected = [['aa', 'bb'], ['cc', 'dd', 'ee']]
    self.assertEqual(parse_sections(lines), expected)

  def test_parse_stacks(self):
    lines = [
      '    [Z]    ',
      '    [Y]    ',
      '    [X] [A]',
      ' 1   2   3 ',
    ]
    stacks = parse_stacks(lines)
    self.assertEqual(len(stacks), 3)
    self.assertEqual(stacks[0], [])
    self.assertEqual(stacks[1], ['X', 'Y', 'Z'])
    self.assertEqual(stacks[2], ['A'])

  def test_parse_moves(self):
    lines = [
      'move 1 from 2 to 1',
      'move 3 from 1 to 3',
      'move 2 from 2 to 1',
      'move 1 from 1 to 2'
    ]
    moves = parse_moves(lines)
    self.assertEqual(len(moves), 4)
    self.assertEqual(moves[0], (1, 1, 0))
    self.assertEqual(moves[1], (3, 0, 2))
    self.assertEqual(moves[2], (2, 1, 0))
    self.assertEqual(moves[3], (1, 0, 1))

  def test_make_move(self):
    stacks = [['Z', 'N', 'D'], ['M', 'C'], ['P']]
    move = (3, 0, 2)
    expected_in_reverse = [[], ['M', 'C'], ['P', 'D', 'N', 'Z']]
    expected_in_bulk = [[], ['M', 'C'], ['P', 'Z', 'N', 'D']]
    self.assertEqual(move_maker(True)(stacks, move), expected_in_reverse)
    self.assertEqual(move_maker(False)(stacks, move), expected_in_bulk)

  def test_solve_puzzle(self):
    lines = [
      '    [D]    ',
      '[N] [C]    ',
      '[Z] [M] [P]',
      ' 1   2   3 ',
      '',
      'move 1 from 2 to 1',
      'move 3 from 1 to 3',
      'move 2 from 2 to 1',
      'move 1 from 1 to 2',
    ]
    self.assertEqual(solve_puzzle(lines, True), 'CMZ')
    self.assertEqual(solve_puzzle(lines, False), 'MCD')
