from sys import stdin
from functools import reduce

def start_finder(n):
  def find_start(line):
    def reducer(window_at, char_at):
      if len(set(window_at[1])) == n:
        return window_at
      window = (
        [*window_at[1], char_at[1]] if len(window_at[1]) < n else
        [*window_at[1][1:], char_at[1]]
      )
      return (char_at[0], window)
    result = reduce(reducer, enumerate(line), (-1, []))
    return result[0] + 1 if len(set(result[1])) == n else None
  return find_start

def main():
  lines = stdin.read().splitlines()
  print(start_finder(4)(lines[0]))
  print(start_finder(14)(lines[0]))

if __name__ == "__main__":
    main()
