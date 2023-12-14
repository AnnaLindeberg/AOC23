def parseRow(row):
    hotSprings, broken = row.strip().split()
    broken = list(map(int, broken.split(',')))
    return hotSprings, broken

def countConfigs(hotSpringMap, brokenSeq):
    L = [(0, 0)]
    count = 0
    while len(L) > 0:
        newL = []
        for smallMapIdx, seqIdx in L:
            smallMap = hotSpringMap[smallMapIdx:]
            seq = brokenSeq[seqIdx:]
            if len(seq) == 0 and '#' not in smallMap:
                count += 1
                continue
            elif len(seq) == 0 or len(smallMap) == 0:
                continue

            firstChar = smallMap[0]
            firstNum = seq[0]

            if firstChar == '.':
                newL.append((smallMapIdx + 1, seqIdx))
            elif firstChar == '#':
                if (len(smallMap) == firstNum or (len(smallMap) > firstNum and smallMap[firstNum] in ['.','?'])) and '.' not in smallMap[:firstNum]:
                    newL.append((smallMapIdx + firstNum + 1, seqIdx + 1))
                else:
                    continue
            elif firstChar == '?':
                if (len(smallMap) == firstNum or (len(smallMap) > firstNum and smallMap[firstNum] in ['.','?'])) and '.' not in smallMap[:firstNum]:
                    newL.append((smallMapIdx + firstNum + 1, seqIdx + 1))
                newL.append((smallMapIdx + 1, seqIdx))
        L = newL
    return count
            

def main():
    ans1tot = 0
    ans2tot = 0
    with open("input12.txt") as file:
        for row in file:
            hotSprings, broken = parseRow(row)
            c1 = countConfigs(hotSprings, broken)
            c2 = countConfigs('?'.join([hotSprings]*5), broken*5)
            # print(hotSprings, broken, c)
            ans1tot += c1
            ans2tot += c2

    print(f"Task 1: {ans1tot}\nTask 2: {ans2tot}")


if __name__ == '__main__':
    main()