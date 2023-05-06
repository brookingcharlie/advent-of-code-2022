from unittest import TestCase
from main import Direction, Cave, rock_generator, parse_jets, solve_puzzle

class Test(TestCase):
  line = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

  def test_parse_jets(self):
    actual = parse_jets('><<>')
    expected = [Direction.RIGHT, Direction.LEFT, Direction.LEFT, Direction.RIGHT]
    self.assertEqual(actual, expected)

  def test_cave(self):
    cave = Cave(parse_jets(Test.line))
    for rock in rock_generator(10):
      cave.add_rock(rock)
    drawing = (
      '|....#..|\n'
      '|....#..|\n'
      '|....##.|\n'
      '|##..##.|\n'
      '|######.|\n'
      '|.###...|\n'
      '|..#....|\n'
      '|.####..|\n'
      '|....##.|\n'
      '|....##.|\n'
      '|....#..|\n'
      '|..#.#..|\n'
      '|..#.#..|\n'
      '|#####..|\n'
      '|..###..|\n'
      '|...#...|\n'
      '|..####.|\n'
      '+-------+'
    )
    self.assertEqual(cave.draw(), drawing)
    self.assertEqual(cave.height, 17)

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.line, 2022), 3068)
