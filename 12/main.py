from sys import stdin
from dataclasses import dataclass
from functools import reduce
from itertools import product

@dataclass
class Node:
  coord: tuple[int, int]
  height: int

@dataclass
class Edge:
  a: Node
  b: Node

@dataclass
class Graph:
  nodes: list[Node]
  edges: list[Edge]

@dataclass
class Problem:
  graph: Graph
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
    return Edge(a, b) if b.height <= a.height + 1 else None
  def edge_reducer(edges, coord):
    potential_edges = [create_edge(coord, step) for step in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    return edges + [edge for edge in potential_edges if edge is not None]
  coords = product(range(len(node_grid)), range(len(node_grid[0])))
  return reduce(edge_reducer, coords, [])

def parse_problem(lines, highest_letter = 'z'):
  (nodes, start, end) = parse_nodes(lines, highest_letter)
  node_grid = [[nodes[i * len(lines[0]) + j] for j in range(len(lines[0]))] for i in range(len(lines))]
  edges = parse_edges(node_grid)
  return Problem(Graph(nodes, edges), start, end)

def search(problem):
  q = []
  explored = set()
  parent = dict()
  def get_path(v):
    return [v] if (p := parent.get(v, None)) is None else [*get_path(p), v]
  explored.add(problem.start.coord)
  q.append(problem.start)
  while q != []:
    v = q.pop(0)
    if v == problem.end:
      return get_path(v.coord)
    for w in [edge.b for edge in problem.graph.edges if edge.a == v]:
      if w.coord not in explored:
        explored.add(w.coord)
        parent[w.coord] = v.coord
        q.append(w)

def solve_puzzle(lines):
  problem = parse_problem(lines)
  return len(search(problem)) - 1

def main():
  lines = stdin.read().splitlines()
  print(solve_puzzle(lines))

if __name__ == "__main__":
  main()
