from unittest import TestCase
from main import get_totals

class Test(TestCase):
  def test_empty(self):
    self.assertEqual(get_totals([]), [])

  def test_single_elf_single_item(self):
    self.assertEqual(get_totals(['5']), [5])

  def test_single_elf_multiple_items(self):
    self.assertEqual(get_totals(['3', '6']), [9])

  def test_multiple_elves(self):
    self.assertEqual(get_totals(['1', '2', '', '3', '4', '5']), [3, 12])
