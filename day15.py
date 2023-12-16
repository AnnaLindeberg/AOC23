# Day 15 of Advent of Code 2023: Lens Library
# https://adventofcode.com/2023/day/15
from collections import defaultdict

def HASH(string):
    res = 0
    for s in string:
        res += ord(s)
        res = (res*17) % 256
    return res

def HASHMAP(instr, boxes):
    if instr[-1] == '-':
        label = instr[:-1]
        box = HASH(label)
        if label in boxes[box]:
            del boxes[box][label]
    else:
        label, focalLen = instr.split('=')
        focalLen = int(focalLen)
        box = HASH(label)
        boxes[box][label] = focalLen

def focusingPower(lenses, boxNo):
    power = 0
    for slotNo, focalLen in enumerate(lenses.values(), start = 1):
        power += (boxNo + 1)*slotNo*focalLen
    return power

def main():
    with open("input15.txt") as file:
        initSeq = file.readline().strip().split(',')

    ans1 = 0
    boxes = defaultdict(dict)
    for instruction in initSeq:
        ans1 += HASH(instruction)
        HASHMAP(instruction, boxes)
        # print(boxes)

    ans2 = 0
    for boxNo, box in boxes.items():
        ans2 += focusingPower(box, boxNo)

    print(f"Task 1: {ans1}\nTask 2: {ans2}")


if __name__ == '__main__':
    main()
