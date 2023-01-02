from sys import stdin
from dataclasses import dataclass
from itertools import product

@dataclass
class Node:
  coord: tuple[int, int]
  height: int
  edges: list['Node'] = None

@dataclass
class Problem:
  nodes: list[Node]
  start: Node
  end: Node

def parse_nodes(lines, highest_letter):
  nodes, start, end = [], None, None
  create_node = lambda coord, letter: Node(coord, ord(letter) - ord('a'))
  for coord in product(range(len(lines)), range(len(lines[0]))):
    match lines[coord[0]][coord[1]]:
      case 'S':
        nodes.append(start := create_node(coord, 'a'))
      case 'E':
        nodes.append(end := create_node(coord, highest_letter))
      case letter:
        nodes.append(create_node(coord, letter))
  return (nodes, start, end)

def infer_edges(nodes, dimensions):
  def infer_edge(node, offset):
    (i, j) = (node.coord[0] + offset[0], node.coord[1] + offset[1])
    if i not in range(dimensions[0]) or j not in range(dimensions[1]):
      return None 
    to_node = nodes[i * dimensions[1] + j]
    return to_node if to_node.height <= node.height + 1 else None
  for node in nodes:
    potential_edges = [infer_edge(node, offset) for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    node.edges = [edge for edge in potential_edges if edge is not None]

def parse_problem(lines, highest_letter = 'z'):
  (nodes, start, end) = parse_nodes(lines, highest_letter)
  infer_edges(nodes, (len(lines), len(lines[0])))
  return Problem(nodes, start, end)

def search(problem, start):
  queue = [start]
  explored = {start.coord}
  parent = dict()
  while queue != []:
    v = queue.pop(0)
    if v == problem.end:
      path = [v.coord]
      while (p := parent.get(path[0], None)) is not None:
        path.insert(0, p)
      return len(path) - 1
    for w in v.edges:
      if w.coord not in explored:
        explored.add(w.coord)
        parent[w.coord] = v.coord
        queue.append(w)
  return None

def solve_puzzle(lines):
  problem = parse_problem(lines)
  from_current = search(problem, problem.start)
  all_from_a = [search(problem, node) for node in problem.nodes if node.height == 0]
  min_from_a = min(result for result in all_from_a if result is not None)
  return (from_current, min_from_a)

def main():
  lines = stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
