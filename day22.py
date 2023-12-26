# Day 22 of Advent of Code 2023: Sand Slabs
# https://adventofcode.com/2023/day/22
import numpy as np
from collections import namedtuple, defaultdict
Coord = namedtuple('Coord', ['x', 'y', 'z'])
Block = namedtuple('Block', ['no', 'start', 'end'])

def blockRange(block):
    start, end = np.array(block.start), np.array(block.end)
    if all(start == end):
        return [block.start]
    blockLen = sum(end - start)
    step = (end - start) // blockLen
    res = []
    for i in range(blockLen + 1):
        res.append(Coord(*(start + step*i)))
    return res

def fallsOn(higherBlock, lowerBlock):
    if higherBlock.start.z <= lowerBlock.end.z:
        return False
    for subBlock in blockRange(higherBlock):
        if subBlock.x in range(lowerBlock.start.x, lowerBlock.end.x + 1) and subBlock.y in range(lowerBlock.start.y, lowerBlock.end.y + 1):
            return True
    return False

def letBlocksFall(blocks):
    fallenBlocks = []
    liesOn = defaultdict(list)
    for block in blocks:
        fallen = False
        fallenBlocks.sort(key=lambda b: b.end.z)
        for fallenBlock in reversed(fallenBlocks):
            if fallen and fallenBlocks[-1].start.z > fallenBlock.end.z + 1:
                break
            if fallsOn(block, fallenBlock):
                if not fallen:
                    blockHeight = block.end.z - block.start.z
                    blockAfterFall = Block(block.no, 
                                        Coord(block.start.x, block.start.y, fallenBlock.end.z + 1),
                                        Coord(block.end.x, block.end.y, fallenBlock.end.z + blockHeight + 1))
                    fallenBlocks.append(blockAfterFall)
                    fallen = True
                liesOn[block.no].append(fallenBlock.no)
        if not fallen:
            blockHeight = block.end.z - block.start.z
            blockAfterFall = Block(block.no, 
                                Coord(block.start.x, block.start.y, 1),
                                Coord(block.end.x, block.end.y, blockHeight + 1))
            fallenBlocks.append(blockAfterFall)
            liesOn[block.no].append('ground')
    return liesOn

def findParents(children):
    parents = defaultdict(set)
    for block, itsChildren in children.items():
        for child in itsChildren:
            parents[child].add(block)
    return parents

def blocksThatFall(removedBlocks, knownFalls, parents, children):
    if len(removedBlocks) ==  0:
        knownFalls[frozenset(removedBlocks)] = set() # unclear if needed
        return knownFalls
    res = set()
    for block in removedBlocks:
        itsFallingParents = set(filter(lambda p: all(c in removedBlocks for c in children[p]), parents[block]))
        frozenParents = frozenset(itsFallingParents)
        if frozenParents not in knownFalls:
            knownFalls = blocksThatFall(itsFallingParents, knownFalls, parents, children)
        res.update(itsFallingParents)
        res.update(knownFalls[frozenParents])
    knownFalls[frozenset(removedBlocks)] = res
    return knownFalls            

def main():
    blocks = []
    with open("input22.txt") as file:
        for blockNo, row in enumerate(file):
            # 1,0,1~1,2,1
            # blockNo = 'ABCDEFGH'[blockNo]
            start, end = row.strip().split('~')
            start, end = Coord(*map(int,start.split(','))), Coord(*map(int,end.split(',')))
            blocks.append(Block(blockNo, start, end))
    
    # checked that b.start.u <= b.end.u for all b in blocks and all u in x,y,z
    blocks.sort(key = lambda b: b.start.z)

    liesOn = letBlocksFall(blocks)
    
    cantBeRemoved =  set()
    for block in blocks:
        supporters = liesOn[block.no]
        if len(supporters) == 1:
            cantBeRemoved.add(supporters[0])

    cantBeRemoved.remove('ground')
    res1 = len(blocks) - len(cantBeRemoved)

    res2 = 0
    knownFalls = {}
    supports = findParents(liesOn)
    for block in cantBeRemoved:
        knownFalls = blocksThatFall(set([block]), knownFalls, supports, liesOn)
        res2 += len(knownFalls[frozenset([block])])


    print(f"Task 1: {res1}\nTask 2: {res2}")


if __name__ == '__main__':
    main()
    # children = {'A':{'B'}, 'B':{'E'},'C':{'D'},'D':{'E', 'F'},'E':{'G'}, 'F':{'G','H'},'G':set(), 'H':set()}
    # parents = findParents(children)
    # res2 = 0
    # knownFalls = {}
    # for block in 'BEDG':
    #     knownFalls = blocksThatFall(set([block]), knownFalls, parents, children)
    #     res2 += len(knownFalls[frozenset([block])])
    # # print(knownFalls, res2)
    # knownFalls = blocksThatFall({'E','F'}, knownFalls, parents, children)
    # print(knownFalls)

# 63581 too low on p2 (should be 77070?)