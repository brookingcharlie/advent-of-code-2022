from unittest import TestCase
from main import (
  Number, Operator, Operation,
  parse_lines, find_variables, solve_puzzle
)

class Test(TestCase):
  lines = [
    'root: pppw + sjmn',
    'dbpl: 5',
    'cczh: sllz + lgvd',
    'zczc: 2',
    'ptdq: humn - dvpt',
    'dvpt: 3',
    'lfqf: 4',
    'humn: 5',
    'ljgn: 2',
    'sjmn: drzm * dbpl',
    'sllz: 4',
    'pppw: cczh / lfqf',
    'lgvd: ljgn * ptdq',
    'drzm: hmdt - zczc',
    'hmdt: 32',
  ]

  def test_parse_lines(self):
    monkeys = parse_lines(Test.lines)
    self.assertEqual(monkeys['root'], Operation(Operator.ADD, 'pppw', 'sjmn'))
    self.assertEqual(monkeys['ptdq'], Operation(Operator.SUBTRACT, 'humn', 'dvpt'))
    self.assertEqual(monkeys['pppw'], Operation(Operator.DIVIDE, 'cczh', 'lfqf'))
    self.assertEqual(monkeys['lgvd'], Operation(Operator.MULTIPLY, 'ljgn', 'ptdq'))
    self.assertEqual(monkeys['hmdt'], Number(32))

  def test_find_variables(self):
    monkeys = parse_lines(Test.lines)
    self.assertEqual(find_variables(monkeys, 'root', 'humn'), ['root', 'pppw', 'cczh', 'lgvd', 'ptdq', 'humn'])

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), (152, 301))
