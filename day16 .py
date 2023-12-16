# Day 16  of Advent of Code 2023: The Floor Will Be Lava
# https://adventofcode.com/2023/day/16 
from collections import deque

def isOutsideGrid(pos, width, height):
    x,y = pos
    return not (0 <= x and 0 <= y and x < width and y < height)

def nextStraightPos(pos, direction):
    directionMap = {'L': (1,0), 'R': (-1,0), 'U' : (0,1), 'D': (0,-1)}
    return (pos[0] + directionMap[direction][0], pos[1] + directionMap[direction][1]), direction

def nextReflectorPos(pos, cameFrom, reflector):
    directionMap = {'/': {'L': (0, -1, 'D'), 'R': (0,1, 'U'), 'U': (-1,0,'R'), 'D': (1,0,'L')},
                    '\\': {'L': (0, 1,'U'), 'R': (0,-1,'D'), 'U': (1,0,'L'), 'D': (-1,0,'R')}}
    return (pos[0] + directionMap[reflector][cameFrom][0], pos[1] + directionMap[reflector][cameFrom][1]), directionMap[reflector][cameFrom][-1]

def nextSplitterPos(pos, cameFrom, splitter):
    splitsFrom = {'|': ['L', 'R'], '-':['U','D']}
    directionMap = {'|': ['D', 'U'], '-': ['R','L']}
    if cameFrom in splitsFrom[splitter]:
        return [nextStraightPos(pos, directionMap[splitter][0]),nextStraightPos(pos, directionMap[splitter][1])]
    else:
        return [nextStraightPos(pos, cameFrom)]

def energizedTiles(grid, startPos):
    width, height = len(grid[0]), len(grid)
    visited = set()
    undealtTiles = deque()
    undealtTiles.append(startPos)
    
    while undealtTiles:
        pos, cameFrom = undealtTiles.pop()
        x, y  = pos
        if isOutsideGrid(pos, width, height):
            continue
        gridChar = grid[y][x]
        visited.add((pos, cameFrom))

        if gridChar == '.':
            posPackage = nextStraightPos(pos, cameFrom)
            if posPackage not in visited:
                undealtTiles.appendleft(posPackage)
        elif gridChar in ['/', '\\']:
            posPackage = nextReflectorPos(pos, cameFrom, gridChar)
            if posPackage not in visited:
                undealtTiles.appendleft(posPackage)
        elif gridChar in ['|', '-']:
            for posPackage in nextSplitterPos(pos, cameFrom, gridChar):
                if posPackage not in visited:
                    undealtTiles.appendleft(posPackage)

    return set(pp[0] for pp in visited)

def main():
    grid = []
    with open("input16.txt") as file:
        for row in file:
            grid.append(row.strip())

    ans1 = len(energizedTiles(grid, ((0,0), 'L')))

    ans2 = ans1

    possibleStarts = [((x,0),'U') for x in range(len(grid[0]))] + [((x,len(grid)-1),'D') for x in range(len(grid[0]))]
    possibleStarts += [((0,y), 'L') for y in range(len(grid))] + [((len(grid[0])-1,y), 'R') for y in range(len(grid))]
    for start in possibleStarts:
        tilesHere = len(energizedTiles(grid, start))
        if tilesHere > ans2:
            ans2 = tilesHere

    print(f"Task 1: {ans1}\nTask 2: {ans2}")


if __name__ == '__main__':
    main()
