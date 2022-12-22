from unittest import TestCase
from main import parse_pair, has_containment, has_overlap, total

class Test(TestCase):
  def test_parse_pair(self):
    self.assertEqual(parse_pair('2-4,6-8'), (range(2, 5), range(6, 9)))
    self.assertEqual(parse_pair('6-6,4-6'), (range(6, 7), range(4, 7)))

  def test_has_containment(self):
    self.assertEqual(has_containment((range(2, 9), range(3, 8))), True)
    self.assertEqual(has_containment((range(3, 8), range(2, 9))), True)
    self.assertEqual(has_containment((range(1, 3), range(2, 4))), False)
    self.assertEqual(has_containment((range(2, 4), range(4, 8))), False)

  def test_has_overlap(self):
    self.assertEqual(has_overlap((range(2, 9), range(3, 8))), True)
    self.assertEqual(has_overlap((range(3, 8), range(3, 9))), True)
    self.assertEqual(has_overlap((range(1, 3), range(2, 4))), True)
    self.assertEqual(has_overlap((range(2, 4), range(4, 8))), False)

  def test_totals(self):
    lines = [
      '2-4,6-8',
      '2-3,4-5',
      '5-7,7-9',
      '2-8,3-7',
      '6-6,4-6',
      '2-6,4-8'
    ]
    self.assertEqual(total(lines, has_containment), 2)
    self.assertEqual(total(lines, has_overlap), 4)
