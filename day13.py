# Day 13 of Advent of Code 2023: Point of Incidence
# https://adventofcode.com/2023/day/13

def colsOf(grid):
    res = []
    for col in range(len(grid[0])):
        res.append("".join(grid[i][col] for i in range(len(grid))))
    return res

def duplicateAndAlmost(strings):
    equal = set()
    almostEqual = set()
    for i, s1 in enumerate(strings):
        for j, s2 in enumerate(strings[i+1:], start=i+1):
            diffCount = 0
            for c1, c2 in zip(s1, s2):
                if c1 != c2:
                    diffCount += 1
                if diffCount > 1:
                    break
            if diffCount == 0:
                equal.add((i,j))
            elif diffCount == 1:
                almostEqual.add((i,j))
    return equal, almostEqual

def checkReflect(matches, strLen):
    flips = []
    for flipIdx in range(1, strLen):
        pairCount = min(flipIdx, strLen - flipIdx)
        neededPairs = [(flipIdx - 1 - j, flipIdx + j) for j in range(pairCount)]
        if all([pair in matches for pair in neededPairs]):
            flips.append(flipIdx)
    if len(flips) == 0:
        return 0
    else:
        if len(flips) > 1:
            print("something weird here")
        return max(flips)

def checkAlmostReflect(matches, almostMatches, strLen):
    flips = []
    for flipIdx in range(1, strLen):
        pairCount = min(flipIdx, strLen - flipIdx)
        neededPairs = [(flipIdx - 1 - j, flipIdx + j) for j in range(pairCount)]
        if len(list(filter(lambda t: t in matches, neededPairs))) == len(neededPairs) - 1:
            for pair in matches:
                if pair in neededPairs:
                    neededPairs.remove(pair)
            # know neededPairs have just one element
            if neededPairs[0] in almostMatches:
                flips.append(flipIdx)
    if len(flips) == 0:
        return 0
    else:
        if len(flips) > 1:
            print("something weird here")
        return max(flips)

def main():
    ans1tot = 0
    ans2tot = 0
    with open("input13.txt") as file:
        pattern = []
        for row in file:
            row = row.strip()
            if len(row) == 0:
                # print(pattern)
                equalRows, almostEqualRows = duplicateAndAlmost(pattern)
                equalCols, almostEqualCols = duplicateAndAlmost(colsOf(pattern))
                # print(equalRows, equalCols)
                ans1tot += 100 * checkReflect(equalRows, len(pattern))
                ans1tot += checkReflect(equalCols, len(pattern[0]))

                ans2tot += 100 * checkAlmostReflect(equalRows, almostEqualRows, len(pattern))
                ans2tot += checkAlmostReflect(equalCols, almostEqualCols, len(pattern[0]))

                pattern = []
            else:
                pattern.append(row)

    print(f"Task 1: {ans1tot}\nTask 2: {ans2tot}")


if __name__ == '__main__':
    main()

# 16743 too low