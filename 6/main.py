from sys import stdin
from functools import reduce

def find_start(marker_len, line):
  def reducer(window_at, char_at):
    return (
      window_at if len(set(window_at[1])) == marker_len else
      (char_at[0], [*window_at[1][-(marker_len - 1):], char_at[1]])
    )
  result = reduce(reducer, enumerate(line), (-1, []))
  return result[0] + 1 if len(set(result[1])) == marker_len else None

def main():
  lines = stdin.read().splitlines()
  print(find_start(4, lines[0]))
  print(find_start(14, lines[0]))

if __name__ == "__main__":
  main()
