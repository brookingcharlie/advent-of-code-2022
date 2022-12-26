from unittest import TestCase
from main import find_start

class Test(TestCase):
  def test_find_start(self):
    self.assertEqual(find_start(''), None)
    self.assertEqual(find_start('abc'), None)
    self.assertEqual(find_start('abcd'), 4)
    self.assertEqual(find_start('abcde'), 4)
    self.assertEqual(find_start('bvwbjplbgvbhsrlpgdmjqwftvncz'), 5)
    self.assertEqual(find_start('nppdvjthqldpwncqszvftbrmjlhg'), 6)
    self.assertEqual(find_start('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 10)
    self.assertEqual(find_start('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 11)
