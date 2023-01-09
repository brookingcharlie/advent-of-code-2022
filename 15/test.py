from unittest import TestCase
from main import Sensor, Area, parse_sensors, solve_puzzle

class Test(TestCase):
  example_lines = [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
  ]

  def test_parse_sensors(self):
    sensors = parse_sensors(Test.example_lines)
    self.assertEqual(sensors[0], Sensor(pos=(2, 18), beacon=(-2, 15)))
    self.assertEqual(sensors[13], Sensor(pos=(20, 1), beacon=(15, 3)))

  def test_area(self):
    actual = Area(parse_sensors(Test.example_lines)).draw()
    expected = [
      '..........#..........................',
      '.........###.........................',
      '........#####........................',
      '.......#######.......................',
      '......#########.............#........',
      '.....###########...........###.......',
      '....#############.........#####......',
      '...###############.......#######.....',
      '..#################.....#########....',
      '.###################.#.###########...',
      '##########S########################..',
      '.###########################S#######.',
      '..###################S#############..',
      '...###################SB##########...',
      '....#############################....',
      '.....###########################.....',
      '......#########################......',
      '.......#########S#######S#####.......',
      '........#######################......',
      '.......#########################.....',
      '......####B######################....',
      '.....###S#############.###########...',
      '......#############################..',
      '.......#############################.',
      '.......#############S#######S########',
      '......B#############################.',
      '.....############SB################..',
      '....##################S##########B...',
      '...#######S######################....',
      '....############################.....',
      '.....#############S######S######.....',
      '......#########################......',
      '.......#######..#############B.......',
      '........#####....###..#######........',
      '.........###......#....#####.........',
      '..........#.............###..........',
      '.........................#...........',
    ]
    self.assertEqual(actual, expected)

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.example_lines, 10), (26, 56000011))
