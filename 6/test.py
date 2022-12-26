from unittest import TestCase
from main import start_finder

class Test(TestCase):
  def test_start_finder(self):
    self.assertEqual(start_finder(4)(''), None)
    self.assertEqual(start_finder(4)('abc'), None)
    self.assertEqual(start_finder(4)('abcd'), 4)
    self.assertEqual(start_finder(4)('abcde'), 4)
    self.assertEqual(start_finder(4)('bvwbjplbgvbhsrlpgdmjqwftvncz'), 5)
    self.assertEqual(start_finder(4)('nppdvjthqldpwncqszvftbrmjlhg'), 6)
    self.assertEqual(start_finder(4)('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 10)
    self.assertEqual(start_finder(4)('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 11)
    self.assertEqual(start_finder(14)('mjqjpqmgbljsphdztnvjfqwrcgsmlb'), 19)
    self.assertEqual(start_finder(14)('bvwbjplbgvbhsrlpgdmjqwftvncz'), 23)
    self.assertEqual(start_finder(14)('nppdvjthqldpwncqszvftbrmjlhg'), 23)
    self.assertEqual(start_finder(14)('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 29)
    self.assertEqual(start_finder(14)('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 26)
