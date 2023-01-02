from unittest import TestCase
from main import Node, Problem, parse_problem, solve_puzzle

class Test(TestCase):
  def test_parse_problem(self):
    lines = [
      'Sa',
      'bE'
    ]
    problem = parse_problem(lines, 'c')
    def get_node_details(coord):
      node = next(n for n in problem.nodes if n.coord == coord)
      return (node.height, [a.coord for a in node.adjacent_nodes])
    self.assertEqual(get_node_details((0, 0)), (0, [(0, 1), (1, 0)]))
    self.assertEqual(get_node_details((0, 1)), (0, [(0, 0)]))
    self.assertEqual(get_node_details((1, 0)), (1, [(1, 1), (0, 0)]))
    self.assertEqual(get_node_details((1, 1)), (2, [(1, 0), (0, 1)]))
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
    self.assertEqual(solve_puzzle(lines), (31, 29))
