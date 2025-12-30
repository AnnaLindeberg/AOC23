# Day 17 of Advent of Code 2023: Clumsy Crucible
# https://adventofcode.com/2023/day/17
import networkx as nx


def assign_weights(graph: nx.DiGraph, grid: list[list[int]]):
    for edge in graph.edges:
        u, v = edge
        xdiff, ydiff = v[0]-u[0], v[1]-u[1]
        offset = (xdiff//abs(xdiff), 0) if xdiff else (0, ydiff//abs(ydiff))
        weight = grid[v[1]][v[0]]
        i = 1
        while u[0] + offset[0]*i != v[0] or u[1] + offset[1]*i != v[1]:
            weight += grid[u[1] + offset[1]*i][u[0] + offset[0]*i]
            i += 1
        
        graph.edges[u, v]['weight'] = weight
    

def grid_to_graph(grid: list[list[int]], step_range) -> nx.DiGraph:
    G = nx.DiGraph()
    x_max, y_max = len(grid[0]), len(grid)
    for y in range(y_max):
        for x in range(x_max):
            from_left = [((x,y,'L'),(x, y-i, 'D')) for i in step_range] + [((x,y,'L'),(x, y+i, 'U')) for i in step_range]
            from_up = [((x,y,'U'),(x-i,y,'R')) for i in step_range] + [((x,y,'U'),(x+i,y,'L')) for i in step_range]
            from_down = [((x,y,'D'),(x-i,y,'R')) for i in step_range] + [((x,y,'D'),(x+i,y,'L')) for i in step_range]
            from_right = [((x,y,'R'),(x, y-i, 'D')) for i in step_range] + [((x,y,'R'),(x, y+i, 'U')) for i in step_range]
            for edges in (from_left, from_right, from_down, from_up):
                G.add_edges_from(edges)
    
    out_of_grid = []
    for node in G:
        if 0 <= node[0] < x_max and 0 <= node[1] < y_max:
            if G.in_degree(node) == 0:
                out_of_grid.append(node)
        else:
            out_of_grid.append(node)

    G.remove_nodes_from(out_of_grid)
    assign_weights(G, grid)
    G = nx.relabel_nodes(G, {(0,0,'D'):'S', (0,0,'U'):'S', (0,0,'L'):'S', (0,0,'R'):'S',
                         (x_max-1,y_max-1,'D'):'T', (x_max-1,y_max-1,'U'):'T', (x_max-1,y_max-1,'L'):'T', (x_max-1,y_max-1,'R'):'T'})
    return G

def main():
    grid = []
    with open("input17.txt") as file:
        for row in file:
            grid.append(list(map(int, row.strip())))

    G = grid_to_graph(grid, range(1,4))
    res1 = nx.shortest_path_length(G, source='S', target='T', weight='weight')
    G = grid_to_graph(grid, range(4,11))
    res2 = nx.shortest_path_length(G, source='S', target='T', weight='weight')
    print(f"Task 1: {res1}\nTask 2: {res2}")


if __name__ == '__main__':
    main()
