from sys import stdin
from enum import Enum, auto

class Shape(Enum):
  ROCK = auto()
  PAPER = auto()
  SCISSORS = auto()

their_shape = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
winner = {Shape.ROCK: Shape.PAPER, Shape.PAPER: Shape.SCISSORS, Shape.SCISSORS: Shape.ROCK}
loser = {v: k for k, v in winner.items()}

def parse_round_1(line):
  my_shape = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}
  round = line.split()
  return (their_shape[round[0]], my_shape[round[1]])

def parse_round_2(line):
  round = line.split()
  theirs = their_shape[round[0]]
  mine = (
    winner[theirs] if round[1] == 'Z' else
    theirs if round[1] == 'Y' else
    loser[theirs]
  )
  return (theirs, mine)

def score_outcome(round):
  return (
    6 if round in winner.items() else
    3 if round[0] == round[1] else
    0
  )

def score_round(round):
  shape_score = {Shape.ROCK: 1, Shape.PAPER: 2, Shape.SCISSORS: 3}
  return score_outcome(round) + shape_score[round[1]]

def total_score(lines, parse_round):
  rounds = [parse_round(line) for line in lines]
  scores = [score_round(round) for round in rounds]
  return sum(scores)

def main():
  lines = stdin.read().splitlines()
  print(total_score(lines, parse_round_1))
  print(total_score(lines, parse_round_2))

if __name__ == "__main__":
    main()
