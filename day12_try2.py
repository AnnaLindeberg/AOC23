def parseRow(row):
    hotSprings, broken = row.strip().split()
    broken = list(map(int, broken.split(',')))
    return hotSprings, broken

def countConfigs(hotSpringMap, brokenSeq):
    L = [(hotSpringMap, brokenSeq)]
    count = 0
    while len(L) > 0:
        newL = []
        for smallMap, seq in L:
            if len(seq) == 0 and '#' not in smallMap:
                count += 1
                continue
            elif len(seq) == 0 or len(smallMap) == 0:
                continue

            firstChar = smallMap[0]
            firstNum = seq[0]

            if firstChar == '.':
                newL.append((smallMap[1:], seq))
            elif firstChar == '#':
                if (len(smallMap) == firstNum or (len(smallMap) > firstNum and smallMap[firstNum] in ['.','?'])) and '.' not in smallMap[:firstNum]:
                    newL.append((smallMap[firstNum+1:], seq[1:]))
                else:
                    continue
            elif firstChar == '?':
                if (len(smallMap) == firstNum or (len(smallMap) > firstNum and smallMap[firstNum] in ['.','?'])) and '.' not in smallMap[:firstNum]:
                    newL.append((smallMap[firstNum+1:], seq[1:]))
                newL.append((smallMap[1:], seq))
        L = newL
    return count
            

def main():
    totCount = 0
    with open("input12.txt") as file:
        for row in file:
            hotSprings, broken = parseRow(row)
            c = countConfigs(hotSprings, broken)
            # print(hotSprings, broken, c)
            totCount += c

    print(f"Task 1: {totCount}\nTask 2: {0}")


if __name__ == '__main__':
    main()