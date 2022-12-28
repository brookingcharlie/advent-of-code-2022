from unittest import TestCase
from main import Move, Direction, parse, move_head, step_tail, solve_puzzle

class Test(TestCase):
  def test_parse(self):
    lines = ['D 2', 'U 1', 'R 7', 'L 6']
    expected = [
      Move(Direction.DOWN, 2),
      Move(Direction.UP, 1),
      Move(Direction.RIGHT, 7),
      Move(Direction.LEFT, 6),
    ]
    self.assertEqual(parse(lines), expected)

  def test_move_head(self):
    self.assertEqual(move_head((9, 0), Move(Direction.LEFT, 2)), [(8, 0), (7, 0)])
    self.assertEqual(move_head((-9, 2), Move(Direction.RIGHT, 3)), [(-8, 2), (-7, 2), (-6, 2)])
    self.assertEqual(move_head((-3, -2), Move(Direction.UP, 1)), [(-3, -1)])
    self.assertEqual(move_head((-3, -4), Move(Direction.DOWN, 2)), [(-3, -5), (-3, -6)])

  def test_step_tail(self):
    self.assertEqual(step_tail((0, 0), (2, 0)), (1, 0))
    self.assertEqual(step_tail((3, 0), (4, 1)), None)
    self.assertEqual(step_tail((3, 0), (4, 2)), (4, 1))
    self.assertEqual(step_tail((4, 1), (4, 3)), (4, 2))
    self.assertEqual(step_tail((4, 3), (3, 4)), None)
    self.assertEqual(step_tail((2, 4), (1, 3)), None)
    self.assertEqual(step_tail((2, 4), (2, 3)), None)
    self.assertEqual(step_tail((2, 4), (3, 3)), None)
    self.assertEqual(step_tail((2, 4), (4, 3)), (3, 3))
    self.assertEqual(step_tail((3, 4), (1, 4)), (2, 4))

  def test_solve_puzzle(self):
    lines = [
      'R 4',
      'U 4',
      'L 3',
      'D 1',
      'R 4',
      'D 1',
      'L 5',
      'R 2',
    ]
    self.assertEqual(solve_puzzle(lines), 13)
