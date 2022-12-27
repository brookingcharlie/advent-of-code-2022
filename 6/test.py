from unittest import TestCase
from main import find_start

class Test(TestCase):
  def test_find_start(self):
    self.assertEqual(find_start(4, ''), None)
    self.assertEqual(find_start(4, 'abc'), None)
    self.assertEqual(find_start(4, 'abcd'), 4)
    self.assertEqual(find_start(4, 'abcde'), 4)
    self.assertEqual(find_start(4, 'bvwbjplbgvbhsrlpgdmjqwftvncz'), 5)
    self.assertEqual(find_start(4, 'nppdvjthqldpwncqszvftbrmjlhg'), 6)
    self.assertEqual(find_start(4, 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 10)
    self.assertEqual(find_start(4, 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 11)
    self.assertEqual(find_start(14, 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'), 19)
    self.assertEqual(find_start(14, 'bvwbjplbgvbhsrlpgdmjqwftvncz'), 23)
    self.assertEqual(find_start(14, 'nppdvjthqldpwncqszvftbrmjlhg'), 23)
    self.assertEqual(find_start(14, 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 29)
    self.assertEqual(find_start(14, 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 26)
