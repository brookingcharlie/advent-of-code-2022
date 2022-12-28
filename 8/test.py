from unittest import TestCase
from main import Tree, parse, find_visible_1, find_visible_2, solve_puzzle_1, solve_puzzle_2

class Test(TestCase):
  def test_parse(self):
    lines = ['24', '68']
    expected = [[Tree(0, 2), Tree(1, 4)], [Tree(2, 6), Tree(3, 8)]]
    self.assertEqual(parse(lines), expected)

  def test_find_visible_1(self):
    traversal = [Tree(0, 3), Tree(1, 0), Tree(2, 3), Tree(3, 7), Tree(4, 3)]
    self.assertEqual(find_visible_1(traversal), {0, 3})

  def test_find_visible_2(self):
    self.assertEqual(find_visible_2(5, [Tree(18, 4), Tree(19, 9)]), {18, 19})
    self.assertEqual(find_visible_2(5, [Tree(16, 3), Tree(15, 3)]), {15, 16})
    self.assertEqual(find_visible_2(5, [Tree(12, 3), Tree(7, 5), Tree(2, 3)]), {12, 7})
    self.assertEqual(find_visible_2(5, [Tree(22, 3)]), {22})

  def test_solve_puzzle(self):
    lines = [
      '30373',
      '25512',
      '65332',
      '33549',
      '35390',
    ]
    self.assertEqual(solve_puzzle_1(lines), 21)
    self.assertEqual(solve_puzzle_2(lines), 8)
