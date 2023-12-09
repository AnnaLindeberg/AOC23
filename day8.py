# Day 8 of Advent of Code 2023: Haunted Wasteland
# https://adventofcode.com/2023/day/8
from math import gcd, lcm

def walkTo(startAt, endAt, directions, LRseq, LRidx = 0):
    currentPos = startAt
    stepCount = LRidx
    while currentPos != endAt:
        LR = LRseq[stepCount % len(LRseq)]
        currentPos = directions[currentPos][LR]
        stepCount += 1
    return stepCount - LRidx 

def main():
    instructions = dict()
    with open("input8.txt") as file:
        LRseq = file.readline().strip()
        file.readline()
        for row in file:
            place, instruction = row.strip().split(' = ')
            left, right = instruction[1:-1].split(', ')
            instructions[place] = {'L': left, 'R': right}

    print(f"Task 1: {walkTo('AAA', 'ZZZ', instructions, LRseq)}")


    startsToEnds = dict()
    for position in instructions:
        if position[-1] != 'A':
            continue
        
        stepCount = 0
        currentPos = position
        while currentPos[-1] != 'Z':
            LR = LRseq[stepCount % len(LRseq)]
            currentPos = instructions[currentPos][LR]
            stepCount += 1
        startsToEnds[position] = currentPos

    someLoops = dict()
    for startPos in startsToEnds:
        loops = []
        LRidx = 0
        fromPos = startPos
        for _ in range(2):
            stepsTaken = walkTo(fromPos, startsToEnds[startPos], instructions, LRseq, LRidx)
            loops.append(stepsTaken)
            LRidx = stepsTaken % len(LRseq)
            fromPos = instructions[startsToEnds[startPos]][LRseq[LRidx]]
        someLoops[startPos] = loops

    # pattern so far: each startpos loop to endpos after a + b*i steps, for i = 0,1...

    consts = [pair[0] for pair in someLoops.values()]
    modulos = [pair[1] for pair in someLoops.values()]

    # I thought it would be this answer
    print(lcm(*(consts + modulos)))

    # but for some reason it's just this???
    print(f"Task 2: {lcm(*consts)}")


if __name__ == '__main__':
    main()
