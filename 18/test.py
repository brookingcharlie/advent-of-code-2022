from unittest import TestCase
from main import parse_cubes, solve_puzzle

class Test(TestCase):
  lines = [
    '2,2,2',
    '1,2,2',
    '3,2,2',
    '2,1,2',
    '2,3,2',
    '2,2,1',
    '2,2,3',
    '2,2,4',
    '2,2,6',
    '1,2,5',
    '3,2,5',
    '2,1,5',
    '2,3,5',
  ]

  def test_parse_cubes(self):
    cubes = parse_cubes(Test.lines)
    self.assertEqual(cubes[0], (2, 2, 2))
    self.assertEqual(cubes[-1], (2, 3, 5))

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), 64)
