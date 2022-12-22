from unittest import TestCase
from main import parse_rucksack, find_shared_item, determine_priority, total_priority, find_groups, find_badge, total_badge_priority

class Test(TestCase):
  def test_parse_rucksack(self):
    actual = parse_rucksack('vJrwphcJFM')
    expected = (['v', 'J', 'r', 'w', 'p'], ['h', 'c', 'J', 'F', 'M'])
    self.assertEqual(actual, expected)

  def test_find_shared_item(self):
    self.assertEqual(find_shared_item((['v', 'J', 'r'], ['h', 'c', 'J'])), 'J')

  def test_determine_priority(self):
    self.assertEqual(determine_priority('p'), 16)
    self.assertEqual(determine_priority('L'), 38)
    self.assertEqual(determine_priority('P'), 42)
    self.assertEqual(determine_priority('t'), 20)

  def test_find_groups(self):
    r1 = (['a', 'b', 'c'], ['d', 'b', 'e'])
    r2 = (['D', 'K', 'z'], ['K', 'c', 'p'])
    r3 = (['y', 'c', 'W'], ['y', 'w', 'L'])
    r4 = (['J', 'E', 'B'], ['U', 'J', 'x'])
    r5 = (['x', 'D', 'E'], ['L', 'E', 'x'])
    r6 = (['E', 'O', 'w'], ['p', 'w', 'A'])
    actual = find_groups([r1, r2, r3, r4, r5, r6])
    expected = [[r1, r2, r3], [r4, r5, r6]]
    self.assertEqual(actual, expected)

  def test_find_badge(self):
    group = [
      (['a', 'b', 'c'], ['d', 'b', 'e']),
      (['D', 'K', 'z'], ['K', 'c', 'p']),
      (['y', 'c', 'W'], ['y', 'w', 'L'])
    ]
    self.assertEqual(find_badge(group), 'c')

  def test_totals(self):
    lines = [
      'vJrwpWtwJgWrhcsFMMfFFhFp',
      'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
      'PmmdzqPrVvPwwTWBwg',
      'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
      'ttgJtRGJQctTZtZT',
      'CrZsJsPPZsGzwwsLwLmpwMDw'
    ]
    self.assertEqual(total_priority(lines), 157)
    self.assertEqual(total_badge_priority(lines), 70)
