# Day 12 of Advent of Code 2023: Hot Springs
# https://adventofcode.com/2023/day/12
import re
from collections import Counter

def afterThisGroup(hotSpringGroup, signature):
    if len(signature) == 0 or len(hotSpringGroup) < signature[0]:
        if '#' in hotSpringGroup:
            return []
        else:
            return [signature]
    firstNum = signature[0] 
    
    # from here know len(hotSpringGroup) >= signature[0], (and signature[0] exists)
    if hotSpringGroup[0] == '#':
        #must place firstNum broken ones here
        # that can be done if (a) precisely that many are left or 
        # (b) the one after can be picked to be .
        if len(hotSpringGroup) == firstNum:
            return [signature[1:]]
        elif hotSpringGroup[firstNum] == '?':
            return afterThisGroup(hotSpringGroup[firstNum+1:], signature[1:])
        else:
            return []
    elif hotSpringGroup[0] == '?':
        if len(hotSpringGroup) == firstNum:
            return [signature[1:]]
        elif hotSpringGroup[firstNum] == '?':
            # firstNum can be placed here, or skip it
            return afterThisGroup(hotSpringGroup[1:], signature) + afterThisGroup(
                hotSpringGroup[firstNum+1:], signature[1:])
        else:
            return afterThisGroup(hotSpringGroup[1:], signature)
        
def parseRow(row):
    hotsprings, broken = row.strip().split()
    hotsprings = re.sub(r"\.+", " ", hotsprings).strip().split()
    broken = list(map(int, broken.split(',')))
    return hotsprings, broken

def countRow(row):
    print(f"\nRow is {row.strip()}")
    hotsprings, signature = parseRow(row)
    signatures = [(signature, 1)]
    for group in hotsprings:
        newSignatures = []
        for signature, count in signatures:
            signaturesAfterThisGroup = afterThisGroup(group, signature)
            withCounts = Counter([tuple(x) for x in signaturesAfterThisGroup])
            newSignatures += [(list(s), count*c) for s, c  in withCounts.items()]
        signatures = newSignatures

    res = 0
    for remaining, count in signatures:
        if len(remaining) == 0:
            # print(count)
            res += count
    print(res)
    return res

def main():
    totCount = 0
    with open("input12.txt") as file:
        for row in file:
            totCount += countRow(row)

    print(f"Task 1: {totCount}\nTask 2: {0}")


if __name__ == '__main__':
    # main()
    print(countRow("#??#???.??#?#?#??#?. 6,8,2"))

# too low 5988
# wrong 6718
# too high 8498