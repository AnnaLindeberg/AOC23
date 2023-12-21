# Day 21 of Advent of Code 2023: Step Counter
# https://adventofcode.com/2023/day/21
import numpy as np

def isOutsideGrid(pos, width, height):
    x, y = pos
    return not (0 <= x and x < width and 0 <= y and y < height)

def main():
    grid = []
    with open("input21.txt") as file:
        for y, row in enumerate(file):
            grid.append(row.strip())
            if 'S' in grid[-1]:
                startPos = (grid[-1].index('S'), y)
    
    steps = 64
    currentPositions = set()
    currentPositions.add(startPos)
    width, height = len(grid[0]), len(grid)
    for _ in range(steps):
        newPositions = set()
        # print(currentPositions)
        for pos in currentPositions:
            pos = np.array(pos)
            for offSet in [np.array([1,0]), np.array([-1,0]), np.array([0,1]), np.array([0,-1])]:
                newPos = pos + offSet
                if isOutsideGrid(tuple(newPos), width, height) or grid[newPos[1]][newPos[0]] == '#':
                    continue
                newPositions.add(tuple(newPos))
        currentPositions = newPositions
                
    print(f"Task 1: {len(currentPositions)}\nTask 2: {0}")


if __name__ == '__main__':
    main()
