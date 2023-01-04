from unittest import TestCase
from main import Cave, parse_rocks, solve_puzzle

class Test(TestCase):
  example_lines = [
    '498,4 -> 498,6 -> 496,6',
    '503,4 -> 502,4 -> 502,9 -> 494,9',
  ]

  def test_parse_rocks(self):
    cave = Cave(parse_rocks(Test.example_lines))
    expected = [
      '......+...',
      '..........',
      '..........',
      '..........',
      '....#...##',
      '....#...#.',
      '..###...#.',
      '........#.',
      '........#.',
      '#########.',
    ]
    self.assertEqual(cave.draw(), expected)

  def test_add_sand(self):
    cave = Cave(parse_rocks(Test.example_lines))
    for i in range(8):
      cave.add_sand()
    expected = [
      '......+...',
      '..........',
      '..........',
      '..........',
      '....#...##',
      '....#...#.',
      '..###.o.#.',
      '.....ooo#.',
      '....oooo#.',
      '#########.',
    ]
    self.assertEqual(cave.draw(), expected)

  def test_full_cave(self):
    cave = Cave(parse_rocks(Test.example_lines))
    for i in range(24):
      self.assertEqual(cave.add_sand(), True)
    expected = [
      '......+...',
      '..........',
      '......o...',
      '.....ooo..',
      '....#ooo##',
      '...o#ooo#.',
      '..###ooo#.',
      '....oooo#.',
      '.o.ooooo#.',
      '#########.',
    ]
    self.assertEqual(cave.draw(), expected)
    self.assertEqual(cave.add_sand(), False)

  def test_direction_change(self):
    lines = [
      '498,1 -> 498,3 -> 501,3',
      '503,3 -> 503,6 -> 500,6',
    ]
    cave = Cave(parse_rocks(lines))
    for i in range(4):
      cave.add_sand()
    expected = [
      '..+...',
      '#.....',
      '#oo...',
      '####.#',
      '.....#',
      '...oo#',
      '..####',
    ]
    self.assertEqual(cave.draw(), expected)

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.example_lines), 24)
