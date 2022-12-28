from unittest import TestCase
from main import File, Dir, parse, solve_puzzle_1, solve_puzzle_2

class Test(TestCase):
  def test_object_model(self):
    dir = Dir('/', [Dir('a', [File('b', 10)]), File('c', 20), File('d', 30)])
    self.assertEqual(dir.total_size(), 60)

  def test_parse(self):
    lines = [
      *['$ cd /', '$ ls', 'dir a', 'dir b', '10 c'],
      *['$ cd a', '$ ls', '20 d', '30 e'],
      *['$ cd ..'],
      *['$ cd b', '$ ls', '40 f']
    ]
    a = Dir('a', [File('d', 20), File('e', 30)])
    b = Dir('b', [File('f', 40)])
    c = File('c', 10)
    self.assertEqual(parse(lines), Dir('/', [a, b, c]))

  def test_solve_puzzle(self):
    lines = [
      '$ cd /',
      '$ ls',
      'dir a',
      '14848514 b.txt',
      '8504156 c.dat',
      'dir d',
      '$ cd a',
      '$ ls',
      'dir e',
      '29116 f',
      '2557 g',
      '62596 h.lst',
      '$ cd e',
      '$ ls',
      '584 i',
      '$ cd ..',
      '$ cd ..',
      '$ cd d',
      '$ ls',
      '4060174 j',
      '8033020 d.log',
      '5626152 d.ext',
      '7214296 k',
    ]
    self.assertEqual(solve_puzzle_1(lines), 95437)
    self.assertEqual(solve_puzzle_2(lines), 24933642)
