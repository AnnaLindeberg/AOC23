# Day 18 of Advent of Code 2023: Lavaduct Lagoon
# https://adventofcode.com/2023/day/18
from collections import namedtuple, deque
import numpy as np

Segment = namedtuple('Segment', ['x', 'yStart', 'yEnd'])

def areaBetween(stackSeg, nonStackSeg, peakStackX):
    assert stackSeg.yEnd == nonStackSeg.yStart
    if (nonStackSeg.yStart < nonStackSeg.yEnd and nonStackSeg.yEnd < stackSeg.yStart) or (nonStackSeg.yStart > nonStackSeg.yEnd and nonStackSeg.yEnd > stackSeg.yStart):
        area = (abs(stackSeg.x - nonStackSeg.x))*abs(nonStackSeg.yEnd - nonStackSeg.yStart)
        stackSeg = Segment(stackSeg.x, stackSeg.yStart, nonStackSeg.yEnd)
        nonStackSeg = None
    elif abs(peakStackX - nonStackSeg.x) >= abs(stackSeg.x - nonStackSeg.x):
        area = (abs(stackSeg.x - nonStackSeg.x))*abs(nonStackSeg.yEnd - nonStackSeg.yStart)
        if stackSeg.yStart == nonStackSeg.yEnd:
            nonStackSeg = None
        else:
            nonStackSeg = Segment(stackSeg.x, stackSeg.yStart, nonStackSeg.yEnd)
        stackSeg = None
    else:
        area = (abs(stackSeg.x - nonStackSeg.x) - 1)*(abs(stackSeg.yEnd - stackSeg.yStart)-1) + abs(peakStackX - nonStackSeg.x)
        if stackSeg.yStart == nonStackSeg.yEnd:
            nonStackSeg = None
        else:
            nonStackSeg = Segment(stackSeg.x, stackSeg.yStart, nonStackSeg.yEnd)
        stackSeg = None
    return area, stackSeg, nonStackSeg

def runningCount(instructions):
    borderCount, interiorCount = 0, 0
    upDownStack = deque()
    stackDir = None
    xPos, yPos = 0, 0
    for dir, dist in instructions:
        borderCount += dist
        if dir == 'R':
            xPos += dist
        elif dir == 'L':
            xPos -= dist
        elif stackDir is None or dir == stackDir:
            stackDir = dir
            tmp = yPos
            if stackDir == 'D':
                yPos -= dist
            else:
                yPos += dist
            upDownStack.append(Segment(xPos, tmp, yPos))
        else:
            tmp = yPos
            if stackDir == 'D':
                yPos -= dist
            else:
                yPos += dist
            thisSeg = Segment(xPos, tmp, yPos)
            stackSeg = upDownStack.pop()
            while thisSeg is not None and stackSeg is not None:
                if len(upDownStack) > 0:
                    xSneakPeak = upDownStack[-1].x
                else:
                    xSneakPeak = stackSeg.x
                area, stackSeg, thisSeg = areaBetween(stackSeg, thisSeg, xSneakPeak)
                interiorCount += area
                if stackSeg is None and len(upDownStack) > 0:
                    stackSeg = upDownStack.pop()

            if thisSeg is None and stackSeg is None:
                stackDir = None
            elif stackSeg is None:
                upDownStack.append(thisSeg)
                stackDir = dir
    return borderCount + interiorCount 


def main():
    instr1 = []
    with open("small_input18.txt") as file:
        for row in file:
            dir, steps, hex = row.strip().split()
            steps = int(steps)
            instr1.append((dir, steps))
            
    ans1 = runningCount(instr1)
    print(f"Task 1: {ans1}\nTask 2: {0}")


if __name__ == '__main__':
    main()
