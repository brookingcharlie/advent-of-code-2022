from unittest import TestCase
from main import Cave, parse_jets, rock_shapes, solve_puzzle

class Test(TestCase):
  line = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

  def test_parse_jets(self):
    self.assertEqual(parse_jets('><<>'), [1, -1, -1, 1])

  def test_cave(self):
    cave = Cave(parse_jets(Test.line))
    cave.add_rocks(rock_shapes, 10)
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
    self.assertEqual(solve_puzzle(Test.line, 1000000000000), 1514285714288)
