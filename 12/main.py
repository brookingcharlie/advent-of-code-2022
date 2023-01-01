from sys import stdin
from dataclasses import dataclass
from functools import reduce
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
  def letter_to_height(letter):
    return ord(letter) - ord('a')
  def node_reducer(state, coord):
    (nodes, start, end), (i, j) = state, coord
    match lines[i][j]:
      case 'S':
        return ([*nodes, node := Node(coord, letter_to_height('a'))], node, end)
      case 'E':
        return ([*nodes, node := Node(coord, letter_to_height(highest_letter))], start, node)
      case letter:
        return ([*nodes, Node(coord, letter_to_height(letter))], start, end)
  coords = product(range(len(lines)), range(len(lines[0])))
  return reduce(node_reducer, coords, ([], None, None))

def parse_edges(node_grid):
  def create_edge(a_coord, step):
    b_coord = (a_coord[0] + step[0], a_coord[1] + step[1])
    if b_coord[0] not in range(len(node_grid)) or b_coord[1] not in range(len(node_grid[0])):
      return None 
    a, b = node_grid[a_coord[0]][a_coord[1]], node_grid[b_coord[0]][b_coord[1]]
    return b if b.height <= a.height + 1 else None
  for coord in product(range(len(node_grid)), range(len(node_grid[0]))):
    potential_edges = [create_edge(coord, step) for step in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    node_grid[coord[0]][coord[1]].edges = [edge for edge in potential_edges if edge is not None]

def parse_problem(lines, highest_letter = 'z'):
  (nodes, start, end) = parse_nodes(lines, highest_letter)
  node_grid = [[nodes[i * len(lines[0]) + j] for j in range(len(lines[0]))] for i in range(len(lines))]
  parse_edges(node_grid)
  return Problem(nodes, start, end)

def search(problem, start):
  q = []
  explored = set()
  parent = dict()
  def get_path(v):
    return [v] if (p := parent.get(v, None)) is None else [*get_path(p), v]
  explored.add(start.coord)
  q.append(start)
  while q != []:
    v = q.pop(0)
    if v == problem.end:
      return len(get_path(v.coord)) - 1
    for w in v.edges:
      if w.coord not in explored:
        explored.add(w.coord)
        parent[w.coord] = v.coord
        q.append(w)
  return None

def solve_puzzle(lines):
  problem = parse_problem(lines)
  from_current = search(problem, problem.start)
  results_from_a = [search(problem, node) for node in problem.nodes if node.height == 0]
  from_any_a = min(result for result in results_from_a if result is not None)
  return (from_current, from_any_a)

def main():
  lines = stdin.read().splitlines()
  for solution in solve_puzzle(lines):
    print(solution)

if __name__ == "__main__":
  main()
