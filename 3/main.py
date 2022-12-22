from sys import stdin

def parse_rucksack(line):
  half_way = len(line) // 2
  return ([*line[:half_way]], [*line[half_way:]])

def find_shared_item(rucksack):
  return set(rucksack[0]).intersection(set(rucksack[1])).pop()

def determine_priority(item):
  return (
    ord(item) - ord('a') + 1 if item.islower() else
    ord(item) - ord('A') + 27
  )

def total_priority(lines):
  rucksacks = [parse_rucksack(line) for line in lines]
  priorities = [determine_priority(find_shared_item(rucksack)) for rucksack in rucksacks]
  return sum(priorities)

def find_groups(rucksacks):
  group_size = 3
  return [
    rucksacks[(i * group_size):((i + 1) * group_size)]
    for i in range(len(rucksacks) // group_size)
  ]

def find_badge(group):
  rucksack_sets = [set(rucksack[0] + rucksack[1]) for rucksack in group]
  return set.intersection(*rucksack_sets).pop()

def total_badge_priority(lines):
  rucksacks = [parse_rucksack(line) for line in lines]
  badges = [find_badge(group) for group in find_groups(rucksacks)]
  priorities = [determine_priority(badge) for badge in badges]
  return sum(priorities)

def main():
  lines = stdin.read().splitlines()
  print(total_priority(lines))
  print(total_badge_priority(lines))

if __name__ == "__main__":
    main()
