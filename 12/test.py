from unittest import TestCase
from main import Node, Edge, Graph, Problem, parse_problem, solve_puzzle

class Test(TestCase):
  def test_parse_problem(self):
    lines = [
      'Sa',
      'bE'
    ]
    nodes = [
      n00 := Node((0, 0), 0),
      n01 := Node((0, 1), 0),
      n10 := Node((1, 0), 1),
      n11 := Node((1, 1), 2),
    ]
    edges = [
      Edge(n00, n01),
      Edge(n00, n10),
      Edge(n01, n00),
      Edge(n10, n11),
      Edge(n10, n00),
      Edge(n11, n10),
      Edge(n11, n01),
    ]
    actual = parse_problem(lines, 'c')
    expected = Problem(Graph(nodes, edges), n00, n11)
    self.assertEqual(actual, expected)

  def test_solve_puzzle(self):
    lines = [
      'Sabqponm',
      'abcryxxl',
      'accszExk',
      'acctuvwj',
      'abdefghi',
    ]
    actual = solve_puzzle(lines)
    expected = 31
    self.assertEqual(actual, expected)
