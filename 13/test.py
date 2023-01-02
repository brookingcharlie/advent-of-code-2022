from unittest import TestCase
from main import parse_pairs, in_order, solve_puzzle

class Test(TestCase):
  def test_parse_pairs(self):
    lines = [
      '[]',
      '[0]',
      '',
      '[1,2]',
      '[1,[2,[3,4],5]]',
    ]
    expected = [([], [0]), ([1, 2], [1, [2, [3, 4], 5]])]
    self.assertEqual(parse_pairs(lines), expected)

  def test_in_order(self):
    self.assertEqual(in_order(([1, 1, 3, 1, 1], [1, 1, 5, 1, 1])), True)
    self.assertEqual(in_order(([[1], [2, 3, 4]], [[1], 4])), True)
    self.assertEqual(in_order(([9], [[8, 7, 6]])), False)
    self.assertEqual(in_order(([[4, 4], 4, 4], [[4, 4], 4, 4, 4])), True)
    self.assertEqual(in_order(([7, 7, 7, 7], [7, 7, 7])), False)
    self.assertEqual(in_order(([], [3])), True)
    self.assertEqual(in_order(([[[]]], [[]])), False)
    self.assertEqual(in_order(([3, [4, [5, 6, 7]], 8, 9], [3, [4, [5, 6, 0]], 8, 9])), False)

  def test_solve_puzzle(self):
    lines = [
      '[1,1,3,1,1]',
      '[1,1,5,1,1]',
      '',
      '[[1],[2,3,4]]',
      '[[1],4]',
      '',
      '[9]',
      '[[8,7,6]]',
      '',
      '[[4,4],4,4]',
      '[[4,4],4,4,4]',
      '',
      '[7,7,7,7]',
      '[7,7,7]',
      '',
      '[]',
      '[3]',
      '',
      '[[[]]]',
      '[[]]',
      '',
      '[1,[2,[3,[4,[5,6,7]]]],8,9]',
      '[1,[2,[3,[4,[5,6,0]]]],8,9]',
    ]
    self.assertEqual(solve_puzzle(lines), (13, 140))
