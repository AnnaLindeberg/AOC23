# Day 18 of Advent of Code 2023: Lavaduct Lagoon
# https://adventofcode.com/2023/day/18
import numpy as np
from collections import deque
from bisect import insort

def BFSinteriorCount(startPos, trench):
    queue = deque()
    queue.append(startPos)
    visited = set()
    while len(queue) > 0:
        element = queue.popleft()
        visited.add(element)
        element = np.array(element)
        for shift in [np.array([1,0]), np.array([-1,0]), np.array([0,-1]), np.array([0,1])]:
            neighbor = tuple(element + shift)
            if neighbor in trench:
                continue
            elif neighbor not in visited:
                queue.append(neighbor)
    return len(visited)

def iterativeInteriorCount(trench, yMin, yMax):
    interiorInPrevRow = set()
    res = 0
    for y in range(yMin, yMax + 1):
        isInside = False
        interiorInThisRow = set()
        consecutiveTrenchLen = 0
        for x in range(trench[y][0], trench[y][-1] + 1):
            if x in trench[y]:
                consecutiveTrenchLen += 1
            else:
                # first check if you just arrived at a non-trench-spot
                if consecutiveTrenchLen == 1:
                    # Have passed past wall, in our out of interior
                    isInside = not isInside
                    consecutiveTrenchLen = 0
                elif consecutiveTrenchLen > 1:
                    # determined by whether the pos above is or isnt inside
                    isInside = x in interiorInPrevRow
                    consecutiveTrenchLen = 0
                
                # then deal with this position itself
                if isInside:
                    interiorInThisRow.add(x)
        res += len(interiorInThisRow)
        interiorInPrevRow = interiorInThisRow
    return res

def reevaluateExtremes(pos, xMin, xMax, yMin, yMax):
    return min(xMin, pos[0]), max(xMax, pos[0]), min(yMin, pos[1]), max(yMax, pos[1])

def printGrid(trench, xMin, xMax, yMin, yMax):
    for y in range(yMin, yMax + 1):
        for x in range(xMin, xMax + 1):
            if x in trench[y]:
                print('#', end='')
            else:
                print('.', end='')
        print('') 

def main():
    directions = {'R': np.array([1,0]), 'L': np.array([-1,0]), 'U': np.array([0,-1]), 'D': np.array([0,1])}
    currentPos = np.array([0,0])
    trench = {}
    xMin, xMax, yMin, yMax = 0, 0, 0, 0
    with open("small_input18.txt") as file:
        for row in file:
            dir, steps, hex = row.strip().split()
            steps = int(steps)
            dir = directions[dir]
            for _ in range(steps):
                if currentPos[1] in trench:
                    insort(trench[currentPos[1]], currentPos[0])
                else:
                    trench[currentPos[1]] = [currentPos[0]]
                
                xMin, xMax, yMin, yMax = reevaluateExtremes(currentPos, xMin, xMax, yMin, yMax)
                # trench.add(tuple(currentPos))
                currentPos += dir
    
    
    # printGrid(trench, xMin, xMax, yMin, yMax)
    interior = iterativeInteriorCount(trench, yMin, yMax) #BFSinteriorCount((1,1), trench)
    ans1 = interior + sum(map(len, trench.values()))
    print(f"Task 1: {ans1}\nTask 2: {0}")


if __name__ == '__main__':
    main()
