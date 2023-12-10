# Day 10 of Advent of Code 2023: Pipe Maze
# https://adventofcode.com/2023/day/10
from collections import deque

def subtractCoord(c1, c2):
    return c1[0]-c2[0], c1[1]-c2[1]

def addCoord(c1, c2):
    return c1[0]+c2[0], c1[1]+c2[1]

def printLoopOnly(maze, pipesOnLoop, insideLoop = {}):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if (col,row) in pipesOnLoop:
                print(maze[row][col], end='')
            elif (col, row) in insideLoop:
                print('*', end='')
            else:
                print('.', end='')
        print('\n')

def main():
    maze =[]
    with open("input10.txt") as file:
        for i, row in enumerate(file):
            maze.append(row.strip())
            if 'S' in row:
                startPos = (row.index('S'), i)
    
    pipeConnections = {'|': [(0,-1), (0,1)], '-': [(-1,0), (1,0)], 'L': [(0,-1), (1,0)],
                       'J': [(-1,0), (0,-1)], '7': [(-1,0),(0,1)], 'F': [(0,1), (1,0)]}
    
    # manually populate it from starting pos :) Happened to be the same for both test and real input
    pipesOnLoop = set()
    pipesOnLoop.add(startPos)
    
    thisPos, lastPos, steps = addCoord(startPos, (0,1)), startPos, 1
    thisPipe = maze[thisPos[1]][thisPos[0]]

    while thisPipe != 'S':
        pipesOnLoop.add(thisPos)
        thisPipe = maze[thisPos[1]][thisPos[0]]
        if thisPipe == 'S':
            loopLength = steps
            break
        elif thisPipe == '.' or subtractCoord(lastPos, thisPos) not in pipeConnections[thisPipe]:
            continue
        connections = pipeConnections[thisPipe]
        thisPipeConnectsTo = addCoord(connections[(connections.index(subtractCoord(lastPos, thisPos)) + 1) % 2], thisPos)
        thisPos, lastPos, steps = thisPipeConnectsTo, thisPos, steps + 1
    
    #task1 is now finished
    task1ans = loopLength // 2

    # task 2
    insideCount = 0
    isInside = False
    positionsInside = set()
    currentBend = None
    for y, row in enumerate(maze):
        for x, pipe in enumerate(row):
            if pipe == 'S':
                pipe = '|'
            if (x,y) in pipesOnLoop and pipe == '|':
                isInside = not isInside
            elif (x,y) in pipesOnLoop and pipe in ['L', '7', 'J', 'F']:
                # found a bend
                if pipe in ['L', 'F']:
                    #start of bend
                    currentBend = pipe
                else:
                    # end of bend
                    # L-7 and F-J swaps isInside
                    # L-J and F-7 leaves isInside as-is
                    if (currentBend, pipe) in [('L', '7'), ('F', 'J')]:
                        isInside = not isInside
            elif (x,y) not in pipesOnLoop and isInside:
                positionsInside.add((x,y))
                insideCount += 1
    
    print(f"Task 1: {task1ans}\nTask 2: {insideCount}")


if __name__ == '__main__':
    main()
