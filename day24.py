# Day 24 of Advent of Code 2023: Never Tell Me The Odds
# https://adventofcode.com/2023/day/24
import numpy as np
import numpy.linalg as npl
from collections import namedtuple
from itertools import combinations

HailStone = namedtuple('HailStone', ['startPoint', 'velocity'])


def crossingPoint(hailstoneA, hailstoneB, onlyFuture = True):
    if hailstoneA.velocity == hailstoneB.velocity:
        # parallell paths – none of infinitely many intersections
        return None

    velA, velB = np.array(hailstoneA.velocity), np.array(hailstoneB.velocity)
    startA, startB = np.array(hailstoneA.startPoint), np.array(hailstoneB.startPoint)
    m = np.array([velA, -velB]).T
    b = startB - startA 
    
    try:
        timeVals = npl.solve(m, b)
    except npl.LinAlgError:
        return None

    if onlyFuture and not all(abs(timeVals) == timeVals):
        return None

    return startA + timeVals[0]*velA

def isInTestArea(point, minCoord, maxCoord):
    x, y = point
    return minCoord <= x and minCoord <= y and x <= maxCoord and y <= maxCoord

def main():
    hailstonesP1 = []
    with open("input24.txt") as file:
        for row in file:
            startPoint, velocity = row.strip().split(' @ ')
            startPoint = tuple(map(int, startPoint.split(', ')))
            velocity = tuple(map(int, velocity.split(', ')))
            # for part 1: reduced dim
            hailstonesP1.append(HailStone(startPoint, velocity))
    
    res1 = 0
    for hsA, hsB in combinations(hailstonesP1, 2):
        hsA_2D = HailStone(hsA.startPoint[:-1], hsA.velocity[:-1])
        hsB_2D = HailStone(hsB.startPoint[:-1], hsB.velocity[:-1])
        point = crossingPoint(hsA_2D, hsB_2D)
        if point is None:
            continue
        if isInTestArea(point, 200000000000000, 400000000000000):
            res1 += 1

        if npl.matrix_rank(np.array([hsA.velocity, hsB.velocity]).T) == 1:
            print('parallell', hsA, hsB)
            


    print(f"Task 1: {res1}\nTask 2: {0}")


if __name__ == '__main__':
    main()
    # A = HailStone((19, 13), (-2, 1))
    # B =  HailStone((18, 19), (-1, -1))
    # print(crossingPoint(A, B))
