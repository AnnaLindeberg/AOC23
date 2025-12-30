# Day 23 of Advent of Code 2023: A Long Walk
# https://adventofcode.com/2023/day/23
from dataclasses import dataclass
from collections import deque, defaultdict
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class Coord:
    x: int
    y: int
    
    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y)
    
    def __mul__(self, factor: int) -> Coord:
        return Coord(self.x *factor, self.y * factor)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    

DIRECTIONS = [Coord(0,1), Coord(0,-1), Coord(1,0), Coord(-1,0)]

@dataclass
class State:
    pos: Coord
    dir: Coord
    dist: int

class Forest:
    def __init__(self, layout) -> None:
        self.layout = layout
        self.max_x = len(layout[0])
        self.max_y = len(layout)

    def __getitem__(self, coord:Coord):
        if 0 <= coord.x < self.max_x and 0 <= coord.y < self.max_y:
            return self.layout[coord.y][coord.x]
        else:
            return 


def sol_part1(target: Coord, forest: Forest) -> int:
    allowed_next = {Coord(1,0):['.','>'], Coord(-1,0):['.','<'], Coord(0,1):['.','v'], Coord(0,-1):['.','^']}
    queue: deque[State] = deque()
    start = State(Coord(1,0), Coord(0,1), 0)
    queue.append(start)
    found_walk_lengths: list[int] = []

    while queue:
        state = queue.popleft()
        
        new_pos, new_dist = state.pos, state.dist
        while forest[new_pos + state.dir] == '.':
            new_pos += state.dir
            new_dist += 1
        
        if new_pos == target:
            found_walk_lengths.append(state.dist)
        
        directions_to_scan = DIRECTIONS.copy()
        directions_to_scan.remove(state.dir*(-1))
        for new_dir in directions_to_scan:
            if forest[new_pos + new_dir] in allowed_next[new_dir]:
                new_state = State(new_pos+new_dir, new_dir, new_dist + 1)
                # print(f"Added {new_state}")
                queue.append(new_state)
    
    # print(found_walk_lengths)
    return max(found_walk_lengths)

def build_graph(target: Coord, forest: Forest) -> nx.DiGraph:
    graph = nx.DiGraph()
    allowed_next = {Coord(1,0):['.','>'], Coord(-1,0):['.','<'], Coord(0,1):['.','v'], Coord(0,-1):['.','^']}
    queue: deque[State] = deque()
    start = State(Coord(1,0), Coord(0,1), 0)
    queue.append(start)
    found_walk_lengths: list[int] = []

    while queue:
        state = queue.popleft()
        
        new_pos, new_dist = state.pos, state.dist
        while forest[new_pos + state.dir] == '.':
            new_pos += state.dir
            new_dist += 1
        
        if new_pos == target:
            found_walk_lengths.append(state.dist)
        
        directions_to_scan = DIRECTIONS.copy()
        directions_to_scan.remove(state.dir*(-1))
        for new_dir in directions_to_scan:
            if forest[new_pos + new_dir] in allowed_next[new_dir]:
                new_state = State(new_pos+new_dir, new_dir, new_dist + 1)
                # print(f"Added {new_state}")
                queue.append(new_state)
                graph.add_edge(state.pos, new_state.pos, weight=new_state.dist - state.dist)
    
    # print(found_walk_lengths)
    return graph

def suppress_graph(graph: nx.Graph):
    suppressable = [v for v, deg in graph.degree() if deg == 2] # type: ignore
    for v in suppressable:
        n1, n2 = graph.neighbors(v)
        weight = graph.get_edge_data(n1, v)['weight'] + graph.get_edge_data(v, n2)['weight']
        graph.add_edge(n1, n2, weight=weight)
        graph.remove_node(v)
        
    

def main():
    map = []
    with open("small_input23.txt") as file:
        for row in file:
            map.append(row.strip())

    TARGET = Coord(len(map[0])-2, len(map)-1)
    forest = Forest(map)
    res1 = sol_part1(TARGET, forest)
    G = build_graph(TARGET, forest)
    print(f"nx: {nx.dag_longest_path_length(G)}")

    G2 = G.to_undirected()

    # layout = nx.layout.bfs_layout(G2, Coord(1,0))
    # nx.draw_networkx(G2, pos=layout, node_size=100, labels=defaultdict(str)) # type: ignore
    # nx.draw_networkx_edge_labels(G2, pos=layout, edge_labels = {e:G2.get_edge_data(*e)['weight'] for e in G2.edges})
    # plt.show()
    
    suppress_graph(G2)
    layout = nx.layout.forceatlas2_layout(G2)
    nx.draw_networkx(G2, pos=layout, node_size=100, labels=defaultdict(str)) # type: ignore
    nx.draw_networkx_edge_labels(G2, pos=layout, edge_labels = {e:G2.get_edge_data(*e)['weight'] for e in G2.edges})
    plt.show()


    print(f"Task 1: {res1}\nTask 2: {0}")


if __name__ == '__main__':
    main()
