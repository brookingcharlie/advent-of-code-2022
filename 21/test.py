from unittest import TestCase
from main import (
  Monkey, Number, Operator, Operation, Reference,
  parse_monkeys, solve_puzzle
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

  def test_parse_monkeys(self):
    monkeys = parse_monkeys(Test.lines)
    self.assertEqual(monkeys[0], Monkey('root', Operation(Operator.ADD, Reference('pppw'), Reference('sjmn'))))
    self.assertEqual(monkeys[4], Monkey('ptdq', Operation(Operator.SUBTRACT, Reference('humn'), Reference('dvpt'))))
    self.assertEqual(monkeys[11], Monkey('pppw', Operation(Operator.DIVIDE, Reference('cczh'), Reference('lfqf'))))
    self.assertEqual(monkeys[12], Monkey('lgvd', Operation(Operator.MULTIPLY, Reference('ljgn'), Reference('ptdq'))))
    self.assertEqual(monkeys[14], Monkey('hmdt', Number(32)))

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), 152)
