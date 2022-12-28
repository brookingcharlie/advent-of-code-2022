from unittest import TestCase
from main import parse, find_visible, solve_puzzle

class Test(TestCase):
  def test_parse(self):
    lines = ['24', '68']
    expected = [[(1, 2), (2, 4)], [(3, 6), (4, 8)]]
    self.assertEqual(parse(lines), expected)

  def test_find_visible(self):
    traversal = [(1, 3), (2, 0), (3, 3), (4, 7), (5, 3)]
    self.assertEqual(find_visible(traversal), {1, 4})

  def test_solve_puzzle(self):
    lines = [
      '30373',
      '25512',
      '65332',
      '33549',
      '35390',
    ]
    self.assertEqual(solve_puzzle(lines), 21)
