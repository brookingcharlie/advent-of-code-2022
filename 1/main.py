from sys import stdin
from functools import reduce
from unittest import TestCase

def get_totals(lines):
  def reducer(totals, line):
    if line == '':
      return [*totals, 0]
    elif len(totals) == 0:
      return [int(line)]
    else:
      return [*totals[:-1], totals[-1] + int(line)]
  return reduce(reducer, lines, [])

def main():
  lines = stdin.read().splitlines()
  print(max(get_totals(lines)))

class Test(TestCase):
  def test_empty(self):
    self.assertEqual(get_totals([]), [])

  def test_single_elf_single_item(self):
    self.assertEqual(get_totals(['5']), [5])

  def test_single_elf_multiple_items(self):
    self.assertEqual(get_totals(['3', '6']), [9])

  def test_multiple_elves(self):
    self.assertEqual(get_totals(['1', '2', '', '3', '4', '5']), [3, 12])

if __name__ == "__main__":
    main()
