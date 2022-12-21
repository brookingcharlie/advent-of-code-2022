from sys import stdin
from enum import Enum, auto

class Shape(Enum):
  ROCK = auto()
  PAPER = auto()
  SCISSORS = auto()

def parse_round(line):
  theirs = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
  mine = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}
  round = line.split()
  return (theirs[round[0]], mine[round[1]])

def score_outcome(round):
  winners = [(Shape.ROCK, Shape.PAPER), (Shape.PAPER, Shape.SCISSORS), (Shape.SCISSORS, Shape.ROCK)]
  return 6 if round in winners else 3 if round[0] == round[1] else 0

def score_round(round):
  shape_score = {Shape.ROCK: 1, Shape.PAPER: 2, Shape.SCISSORS: 3}
  return score_outcome(round) + shape_score[round[1]]

def total_score(lines):
  rounds = [parse_round(line) for line in lines]
  scores = [score_round(round) for round in rounds]
  return sum(scores)

def main():
  lines = stdin.read().splitlines()
  print(total_score(lines))

if __name__ == "__main__":
    main()
