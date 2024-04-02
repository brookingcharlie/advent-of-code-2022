from unittest import TestCase

from main import Tile, Move, Turn, Rotate, Facing, parse_input, draw_board, calculate_password, solve_puzzle

class Test(TestCase):
  lines = [
    '        ...#',
    '        .#..',
    '        #...',
    '        ....',
    '...#.......#',
    '........#...',
    '..#....#....',
    '..........#.',
    '        ...#....',
    '        .....#..',
    '        .#......',
    '        ......#.',
    '',
    '10R5L5R10L4R5L5',
  ]

  def test_parse_input(self):
    (board, path) = parse_input(Test.lines)
    self.assertEqual(board.get_tile((1, 7)), None)
    self.assertEqual(board.get_tile((1, 16)), None)
    self.assertEqual(board.get_tile((1, 9)), Tile.OPEN)
    self.assertEqual(board.get_tile((2, 10)), Tile.WALL)
    self.assertEqual(board.get_tile((5, 4)), Tile.WALL)
    self.assertEqual(board.get_tile((12, 16)), Tile.OPEN)
    self.assertEqual(path[0], Move(10))
    self.assertEqual(path[1], Turn(Rotate.RIGHT))
    self.assertEqual(path[8], Move(4))
    self.assertEqual(path[-2], Turn(Rotate.LEFT))
    self.assertEqual(path[-1], Move(5))

  def test_draw_board(self):
    (board, _) = parse_input(Test.lines)
    self.assertEqual(
      draw_board(board),
      [
        '        ...#    ',
        '        .#..    ',
        '        #...    ',
        '        ....    ',
        '...#.......#    ',
        '........#...    ',
        '..#....#....    ',
        '..........#.    ',
        '        ...#....',
        '        .....#..',
        '        .#......',
        '        ......#.',
      ]
    )

  def test_start_point(self):
    (board, _) = parse_input(Test.lines)
    self.assertEqual(board.find_start_point(), (1, 9))

  def test_example_path(self):
    (board, _) = parse_input(Test.lines)
    self.assertEqual(board.apply_action(((1, 9), Facing.RIGHT), Move(10)), ((1, 11), Facing.RIGHT))
    self.assertEqual(board.apply_action(((1, 11), Facing.RIGHT), Turn(Rotate.RIGHT)), ((1, 11), Facing.DOWN))
    self.assertEqual(board.apply_action(((1, 11), Facing.DOWN), Move(5)), ((6, 11), Facing.DOWN))
    self.assertEqual(board.apply_action(((6, 11), Facing.DOWN), Turn(Rotate.LEFT)), ((6, 11), Facing.RIGHT))
    self.assertEqual(board.apply_action(((6, 11), Facing.RIGHT), Move(5)), ((6, 4), Facing.RIGHT))
    self.assertEqual(board.apply_action(((6, 4), Facing.RIGHT), Turn(Rotate.RIGHT)), ((6, 4), Facing.DOWN))
    self.assertEqual(board.apply_action(((6, 4), Facing.DOWN), Move(10)), ((8, 4), Facing.DOWN))
    self.assertEqual(board.apply_action(((8, 4), Facing.DOWN), Turn(Rotate.LEFT)), ((8, 4), Facing.RIGHT))
    self.assertEqual(board.apply_action(((8, 4), Facing.RIGHT), Move(4)), ((8, 8), Facing.RIGHT))
    self.assertEqual(board.apply_action(((8, 8), Facing.RIGHT), Turn(Rotate.RIGHT)), ((8, 8), Facing.DOWN))
    self.assertEqual(board.apply_action(((8, 8), Facing.DOWN), Move(5)), ((6, 8), Facing.DOWN))
    self.assertEqual(board.apply_action(((6, 8), Facing.DOWN), Turn(Rotate.LEFT)), ((6, 8), Facing.RIGHT))
    self.assertEqual(board.apply_action(((6, 8), Facing.RIGHT), Move(5)), ((6, 8), Facing.RIGHT))

  def test_moves(self):
    (board, _) = parse_input(Test.lines)
    self.assertEqual(board.apply_action(((6, 4), Facing.LEFT), Move(5)), ((6, 11), Facing.LEFT))
    self.assertEqual(board.apply_action(((8, 4), Facing.UP), Move(10)), ((6, 4), Facing.UP))
    self.assertEqual(board.apply_action(((6, 8), Facing.UP), Move(5)), ((8, 8), Facing.UP))
    self.assertEqual(board.apply_action(((7, 2), Facing.LEFT), Move(12)), ((7, 9), Facing.LEFT))

  def test_turns(self):
    (board, _) = parse_input(Test.lines)
    self.assertEqual(board.apply_action(((1, 7), Facing.RIGHT), Turn(Rotate.RIGHT)), ((1, 7), Facing.DOWN))
    self.assertEqual(board.apply_action(((1, 9), Facing.DOWN), Turn(Rotate.RIGHT)), ((1, 9), Facing.LEFT))
    self.assertEqual(board.apply_action(((2, 10), Facing.LEFT), Turn(Rotate.RIGHT)), ((2, 10), Facing.UP))
    self.assertEqual(board.apply_action(((5, 4), Facing.UP), Turn(Rotate.RIGHT)), ((5, 4), Facing.RIGHT))
    self.assertEqual(board.apply_action(((12, 16), Facing.RIGHT), Turn(Rotate.LEFT)), ((12, 16), Facing.UP))
    self.assertEqual(board.apply_action(((1, 7), Facing.UP), Turn(Rotate.LEFT)), ((1, 7), Facing.LEFT))
    self.assertEqual(board.apply_action(((1, 9), Facing.LEFT), Turn(Rotate.LEFT)), ((1, 9), Facing.DOWN))
    self.assertEqual(board.apply_action(((2, 10), Facing.DOWN), Turn(Rotate.LEFT)), ((2, 10), Facing.RIGHT))

  def test_calculate_password(self):
    self.assertEqual(calculate_password(((6, 8), Facing.RIGHT)), 6032)
    self.assertEqual(calculate_password(((5, 7), Facing.UP)), 5031)

  def test_solve_puzzle(self):
    self.assertEqual(solve_puzzle(Test.lines), 6032)
