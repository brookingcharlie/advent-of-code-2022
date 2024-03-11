from unittest import TestCase
from main import parse_cubes, create_bounding_box, outside_bounding_box, solve_puzzle

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
    self.assertIn((2, 2, 2), cubes)
    self.assertIn((2, 3, 5), cubes)

  def test_create_bounding_box(self):
    actual = create_bounding_box(parse_cubes(Test.lines))
    expected = ((0, 4), (0, 4), (0, 7))
    self.assertEqual(actual, expected)

  def test_outside_bounding_box(self):
    bounding_box = ((0, 2), (0, 4), (0, 3))
    self.assertEqual(outside_bounding_box(bounding_box, (0, 3, 2)), False)
    self.assertEqual(outside_bounding_box(bounding_box, (2, 0, 0)), False)
    self.assertEqual(outside_bounding_box(bounding_box, (3, 1, 2)), True)
    self.assertEqual(outside_bounding_box(bounding_box, (0, 5, 4)), True)

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), (64, 58))
