from sys import stdin
from functools import reduce

def find_start(line):
  def reducer(window_at, char_at):
    if len(set(window_at[1])) == 4:
      return window_at
    window = (
      [*window_at[1], char_at[1]] if len(window_at[1]) < 4 else
      [*window_at[1][1:], char_at[1]]
    )
    return (char_at[0], window, len(set(window)) == 4)
  result = reduce(reducer, enumerate(line), (-1, []))
  return result[0] + 1 if len(set(result[1])) == 4 else None

def main():
  lines = stdin.read().splitlines()
  print(find_start(lines[0]))

if __name__ == "__main__":
    main()
