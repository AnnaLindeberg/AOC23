# Day 17 of Advent of Code 2023: Clumsy Crucible
# https://adventofcode.com/2023/day/17
import math
from collections import defaultdict, deque
from queue import PriorityQueue


def isOutsideGrid(pos, width, height):
    x,y = pos
    return not (0 <= x and 0 <= y and x < width and y < height)

def addPos(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]

def subPos(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]

def minDistQueueElement(queue, dist):
    minVal = math.inf
    for pos, x, y in queue:
        if dist[pos] <= minVal:
            minEl = pos, x, y
            minVal = dist[pos]
    return minEl

def tooLongStraightPath(node, neighborOffset, prev):
    last3offsets = []
    current = node
    for _ in range(3):
        if current in prev:
            last3offsets.append(subPos(current, prev[current]))
            current = prev[current]
        else:
            break
    if len(last3offsets) == 3 and len(set(last3offsets)) == 1 and neighborOffset == subPos(node, prev[node]):
        return True
    else:
        return False


def Dijkstra(grid, source, target):
    width, height = len(grid[0]), len(grid)
    # dist = defaultdict(lambda: math.inf)
    # dist[source] = 0
    # prev = dict()
    # a queue/visited element: (dist, (position, offset from last pos))
    Q = PriorityQueue()
    Q.put((0, (source, None)))
    visited = set()
    targetMin = math.inf
 
    while not Q.empty():
        # u ← vertex in Q with min dist[u]
        u = Q.get_nowait()

        distToCurrent, tmp = u
        currentPos, currentOffset = tmp
        visited.add((currentPos, currentOffset))

        turnsToTake = [(0,1),(0,-1),(1,0),(-1,0)]
        if currentOffset is not None:
            turnsToTake.remove(currentOffset)
            turnsToTake.remove((currentOffset[0]*(-1), currentOffset[1]*(-1)))

        for newOffset in turnsToTake:
            for i in range(1,4):
                neighbor = addPos(currentPos, (newOffset[0]*(i), newOffset[1]*(i)))
                if isOutsideGrid(neighbor, width, height):
                    break

                costBetween = 0
                for j in range(1,i+1):
                    x, y = addPos(currentPos, (newOffset[0]*(j), newOffset[1]*(j)))
                    costBetween += grid[y][x]

                altDist = distToCurrent + costBetween
                if neighbor == target and altDist < targetMin:
                    targetMin = altDist
                if neighbor == target:
                    break
                if (neighbor, newOffset) not in visited and altDist <= targetMin:
                    Q.put((altDist, (neighbor, newOffset)))
    return targetMin



def printPath(grid, prev, source, target):
    pathChars = {}
    offsetToChar = {(1,0):'>', (-1,0):'<',(0,1):'v',(0,-1):'^'}
    current = target
    while current != source:
        pathChars[current] = offsetToChar[subPos(current,prev[current])]
        current = prev[current]
    s = ''
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x,y) in pathChars:
                s += pathChars[(x,y)]
            else:
                s += str(grid[y][x])
        s+= '\n'
    print(s)


def main():
    grid = []
    with open("input17.txt") as file:
        for row in file:
            grid.append(list(map(int, row.strip())))

    D = Dijkstra(grid, (0,0), (len(grid[0])- 1, len(grid) - 1))


    print(f"Task 1: {D}\nTask 2: {0}")


if __name__ == '__main__':
    main()
