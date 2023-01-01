from unittest import TestCase
from main import (
  Add, Multiply, Square, Test as MonkeyTest, Monkey,
  parse_sections, parse_operation, parse_monkies,
  solve_puzzle
)

class Test(TestCase):
  def test_parse_sections(self):
    lines = ['aa', 'bb', '', 'cc', 'dd', 'ee']
    expected = [['aa', 'bb'], ['cc', 'dd', 'ee']]
    self.assertEqual(parse_sections(lines), expected)

  def test_parse_operation(self):
    self.assertEqual(parse_operation('  Operation: new = old + 6'), Add(6))
    self.assertEqual(parse_operation('  Operation: new = old * 19'), Multiply(19))
    self.assertEqual(parse_operation('  Operation: new = old * old'), Square())

  def test_parse_monkies(self):
    lines = [
      'Monkey 0:',
      '  Starting items: 79, 98',
      '  Operation: new = old * 19',
      '  Test: divisible by 23',
      '    If true: throw to monkey 1',
      '    If false: throw to monkey 2',
      '',
      'Monkey 1:',
      '  Starting items: 49',
      '  Operation: new = old + 15',
      '  Test: divisible by 3',
      '    If true: throw to monkey 0',
      '    If false: throw to monkey 2',
    ]
    expected = [
      Monkey(0, [79, 98], Multiply(19), MonkeyTest(23, {True: 1, False: 2})),
      Monkey(1, [49], Add(15), MonkeyTest(3, {True: 0, False: 2})),
    ]
    self.assertEqual(parse_monkies(lines), expected)

  def test_operations(self):
    self.assertEqual(Add(6).apply(3), 9)
    self.assertEqual(Multiply(4).apply(3), 12)
    self.assertEqual(Square().apply(5), 25)

  def test_take_turn(self):
    monkey_0 = Monkey(0, [4, 5], Multiply(3), MonkeyTest(2, {True: 1, False: 2}))
    monkey_1 = Monkey(1, [6], Add(1), MonkeyTest(23, {True: 0, False: 2}))
    monkey_2 = Monkey(2, [], Square(), MonkeyTest(6, {True: 1, False: 0}))
    monkey_0.take_turn([monkey_0, monkey_1, monkey_2])
    self.assertEqual(monkey_0.items, [])
    self.assertEqual(monkey_1.items, [6, 4])
    self.assertEqual(monkey_2.items, [5])

  def test_play_game(self):
    lines = [
      'Monkey 0:',
      '  Starting items: 79, 98',
      '  Operation: new = old * 19',
      '  Test: divisible by 23',
      '    If true: throw to monkey 2',
      '    If false: throw to monkey 3',
      '',
      'Monkey 1:',
      '  Starting items: 54, 65, 75, 74',
      '  Operation: new = old + 6',
      '  Test: divisible by 19',
      '    If true: throw to monkey 2',
      '    If false: throw to monkey 0',
      '',
      'Monkey 2:',
      '  Starting items: 79, 60, 97',
      '  Operation: new = old * old',
      '  Test: divisible by 13',
      '    If true: throw to monkey 1',
      '    If false: throw to monkey 3',
      '',
      'Monkey 3:',
      '  Starting items: 74',
      '  Operation: new = old + 3',
      '  Test: divisible by 17',
      '    If true: throw to monkey 0',
      '    If false: throw to monkey 1',
    ]
    self.assertEqual(solve_puzzle(lines), 10605)
