from unittest import TestCase
from main import Shape, parse_round, score_outcome, score_round, total_score

class Test(TestCase):
  def test_parse_round(self):
    self.assertEqual(parse_round('A Y'), (Shape.ROCK, Shape.PAPER))
    self.assertEqual(parse_round('B X'), (Shape.PAPER, Shape.ROCK))
    self.assertEqual(parse_round('C Z'), (Shape.SCISSORS, Shape.SCISSORS))

  def test_score_outcome(self):
    self.assertEqual(score_outcome((Shape.SCISSORS, Shape.ROCK)), 6)
    self.assertEqual(score_outcome((Shape.PAPER, Shape.PAPER)), 3)
    self.assertEqual(score_outcome((Shape.SCISSORS, Shape.PAPER)), 0)

  def test_score_round(self):
    self.assertEqual(score_round((Shape.ROCK, Shape.PAPER)), 8)
    self.assertEqual(score_round((Shape.PAPER, Shape.ROCK)), 1)
    self.assertEqual(score_round((Shape.SCISSORS, Shape.SCISSORS)), 6)

  def test_total_score(self):
    self.assertEqual(total_score(['A Y', 'B X', 'C Z']), 15)
