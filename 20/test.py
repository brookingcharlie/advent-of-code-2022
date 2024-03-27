from unittest import TestCase
from main import parse_numbers, mix_number, mix_numbers, solve_puzzle

class Test(TestCase):
  lines = ['1', '2', '-3', '3', '-2', '0', '4']

  def test_parse_numbers_1(self):
    self.assertEqual(
      parse_numbers(Test.lines, 1),
      [1, 2, -3, 3, -2, 0, 4]
    )

  def test_parse_numbers_811589153(self):
    self.assertEqual(
      parse_numbers(Test.lines, 811589153),
      [811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612]
    )

  def test_mix_number_0(self):
    self.assertEqual(
      mix_number([(0, 1), (1, 2), (2, -3), (3, 0), (4, 3), (5, 4), (6, -2)], (3, 0)),
      list([(0, 1), (1, 2), (2, -3), (3, 0), (4, 3), (5, 4), (6, -2)])
    )

  def test_mix_number_1(self):
    self.assertEqual(
      mix_number([(0, 1), (1, 2), (2, -3), (3, 3), (4, -2), (5, 0), (6, 4)], (0, 1)),
      [(1, 2), (0, 1), (2, -3), (3, 3), (4, -2), (5, 0), (6, 4)]
    )

  def test_mix_number_4(self):
    self.assertEqual(
      mix_number([(0, 1), (1, 2), (2, -3), (3, 0), (4, 3), (5, 4), (6, -2)], (5, 4)),
      [(0, 1), (1, 2), (2, -3), (5, 4), (3, 0), (4, 3), (6, -2)]
    )

  def test_mix_number_minus_3(self):
    self.assertEqual(
      mix_number([(0, 1), (1, -3), (2, 2), (3, 3), (4, -2), (5, 0), (6, 4)], (1, -3)),
      [(0, 1), (2, 2), (3, 3), (4, -2), (1, -3), (5, 0), (6, 4)]
    )

  def test_mix_number_minus_2(self):
    self.assertEqual(
      mix_number([(0, 1), (1, 2), (2, -2), (3, -3), (4, 0), (5, 3), (6, 4)], (2, -2)),
      [(0, 1), (1, 2), (3, -3), (4, 0), (5, 3), (6, 4), (2, -2)]
    )

  def test_mix_number_0_first(self):
    self.assertEqual(
      mix_number([(0, 0), (1, 2), (2, -3), (3, 1), (4, 3), (5, 4), (6, -2)], (0, 0)),
      [(0, 0), (1, 2), (2, -3), (3, 1), (4, 3), (5, 4), (6, -2)]
    )

  def test_mix_numbers_1(self):
    self.assertEqual(
      mix_numbers([1, 2, -3, 3, -2, 0, 4], 1),
      [1, 2, -3, 4, 0, 3, -2]
    )

  def test_mix_numbers_10(self):
    self.assertEqual(
      mix_numbers([811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612], 10),
      [0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153]
    )

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), (3, 1623178306))
