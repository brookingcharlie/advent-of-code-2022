from unittest import TestCase
from main import Node, Problem, parse_problem, solve_puzzle

class Test(TestCase):
  def test_parse_problem(self):
    lines = [
      'Sa',
      'bE'
    ]
    problem = parse_problem(lines, 'c')
    self.assertEqual(problem.nodes[0].coord, (0, 0))
    self.assertEqual(problem.nodes[2].coord, (1, 0))
    self.assertEqual(problem.nodes[0].height, 0)
    self.assertEqual(problem.nodes[2].height, 1)
    self.assertEqual([node.coord for node in problem.nodes[0].edges], [(0, 1), (1, 0)])
    self.assertEqual([node.coord for node in problem.nodes[2].edges], [(1, 1), (0, 0)])
    self.assertEqual(problem.start.coord, (0, 0))
    self.assertEqual(problem.end.coord, (1, 1))

  def test_solve_puzzle(self):
    lines = [
      'Sabqponm',
      'abcryxxl',
      'accszExk',
      'acctuvwj',
      'abdefghi',
    ]
    actual = solve_puzzle(lines)
    expected = (31, 29)
    self.assertEqual(actual, expected)
