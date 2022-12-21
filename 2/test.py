from unittest import TestCase
from main import Shape, parse_round_1, parse_round_2, score_outcome, score_round, total_score

class Test(TestCase):
  def test_parse_round_1(self):
    self.assertEqual(parse_round_1('A Y'), (Shape.ROCK, Shape.PAPER))
    self.assertEqual(parse_round_1('B X'), (Shape.PAPER, Shape.ROCK))
    self.assertEqual(parse_round_1('C Z'), (Shape.SCISSORS, Shape.SCISSORS))

  def test_parse_round_2(self):
    self.assertEqual(parse_round_2('A Y'), (Shape.ROCK, Shape.ROCK))
    self.assertEqual(parse_round_2('B X'), (Shape.PAPER, Shape.ROCK))
    self.assertEqual(parse_round_2('C Z'), (Shape.SCISSORS, Shape.ROCK))
    self.assertEqual(parse_round_2('C X'), (Shape.SCISSORS, Shape.PAPER))

  def test_score_outcome(self):
    self.assertEqual(score_outcome((Shape.SCISSORS, Shape.ROCK)), 6)
    self.assertEqual(score_outcome((Shape.PAPER, Shape.PAPER)), 3)
    self.assertEqual(score_outcome((Shape.SCISSORS, Shape.PAPER)), 0)

  def test_score_round(self):
    self.assertEqual(score_round((Shape.ROCK, Shape.PAPER)), 8)
    self.assertEqual(score_round((Shape.PAPER, Shape.ROCK)), 1)
    self.assertEqual(score_round((Shape.SCISSORS, Shape.SCISSORS)), 6)

  def test_total_score_1(self):
    self.assertEqual(total_score(['A Y', 'B X', 'C Z'], parse_round_1), 15)

  def test_total_score_2(self):
    self.assertEqual(total_score(['A Y', 'B X', 'C Z'], parse_round_2), 12)
