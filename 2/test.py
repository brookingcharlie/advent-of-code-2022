from unittest import TestCase
from main import Shape, strategy_1, strategy_2, parse_round, score_outcome, score_round, total_score

class Test(TestCase):
  def test_parse_round_1(self):
    self.assertEqual(parse_round('A Y', strategy_1), (Shape.ROCK, Shape.PAPER))
    self.assertEqual(parse_round('B X', strategy_1), (Shape.PAPER, Shape.ROCK))
    self.assertEqual(parse_round('C Z', strategy_1), (Shape.SCISSORS, Shape.SCISSORS))

  def test_parse_round_2(self):
    self.assertEqual(parse_round('A Y', strategy_2), (Shape.ROCK, Shape.ROCK))
    self.assertEqual(parse_round('B X', strategy_2), (Shape.PAPER, Shape.ROCK))
    self.assertEqual(parse_round('C Z', strategy_2), (Shape.SCISSORS, Shape.ROCK))
    self.assertEqual(parse_round('C X', strategy_2), (Shape.SCISSORS, Shape.PAPER))

  def test_score_outcome(self):
    self.assertEqual(score_outcome((Shape.SCISSORS, Shape.ROCK)), 6)
    self.assertEqual(score_outcome((Shape.PAPER, Shape.PAPER)), 3)
    self.assertEqual(score_outcome((Shape.SCISSORS, Shape.PAPER)), 0)

  def test_score_round(self):
    self.assertEqual(score_round((Shape.ROCK, Shape.PAPER)), 8)
    self.assertEqual(score_round((Shape.PAPER, Shape.ROCK)), 1)
    self.assertEqual(score_round((Shape.SCISSORS, Shape.SCISSORS)), 6)

  def test_total_score_1(self):
    self.assertEqual(total_score(['A Y', 'B X', 'C Z'], strategy_1), 15)

  def test_total_score_2(self):
    self.assertEqual(total_score(['A Y', 'B X', 'C Z'], strategy_2), 12)
