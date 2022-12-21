from sys import stdin
from enum import Enum, auto

class Shape(Enum):
  ROCK = auto()
  PAPER = auto()
  SCISSORS = auto()

winner = {Shape.ROCK: Shape.PAPER, Shape.PAPER: Shape.SCISSORS, Shape.SCISSORS: Shape.ROCK}

def strategy_1(their_shape, my_token):
  my_shape_by_token = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}
  return my_shape_by_token[my_token]

def strategy_2(their_shape, my_token):
  loser = {v: k for k, v in winner.items()}
  return (
    winner[their_shape] if my_token == 'Z' else
    their_shape if my_token == 'Y' else
    loser[their_shape]
  )

def parse_round(line, strategy):
  their_shape_by_token = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
  round = line.split()
  their_shape = their_shape_by_token[round[0]]
  return (their_shape, strategy(their_shape, round[1]))

def score_outcome(round):
  return (
    6 if round in winner.items() else
    3 if round[0] == round[1] else
    0
  )

def score_round(round):
  score_by_shape = {Shape.ROCK: 1, Shape.PAPER: 2, Shape.SCISSORS: 3}
  return score_outcome(round) + score_by_shape[round[1]]

def total_score(lines, strategy):
  rounds = [parse_round(line, strategy) for line in lines]
  scores = [score_round(round) for round in rounds]
  return sum(scores)

def main():
  lines = stdin.read().splitlines()
  print(total_score(lines, strategy_1))
  print(total_score(lines, strategy_2))

if __name__ == "__main__":
    main()
