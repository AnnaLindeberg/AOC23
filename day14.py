# Day 14 of Advent of Code 2023: Parabolic Reflector Dish
# https://adventofcode.com/2023/day/14

def stoneSeq(column):
    seq = []
    roundStoneCount = 0
    for idx, symb in enumerate(column, ):
        if symb == '.':
            continue
        elif symb == 'O':
            roundStoneCount += 1
        elif symb == '#':
            seq.append(('O', roundStoneCount))
            roundStoneCount = 0
            seq.append(('#', len(column) - idx))
    seq.append(('O', roundStoneCount))
    return seq

def roundStonePlacements(columns):
    res = []
    for column in columns:
        L = len(column)
        res.append(tuple(L - i for i,x in enumerate(column) if x == 'O'))
    return tuple(res)

def flipHorizontal(grid):
    res = []
    for row in grid:
        res.append(row)
    return res

def flipVertical(grid):
    res = []
    for row in grid:
        res.append(''.join(reversed(row)))
    return res

def transpose(grid):
    res = []
    for col in range(len(grid[0])):
        res.append("".join([grid[row][col] for row in range(len(grid))]))
    return res

def tiltWest(grid):
    res = []
    for row in grid:
        dotCount = 0
        newRow = ''
        for char in row:
            if char == '.':
                dotCount += 1
            elif char == 'O':
                newRow += 'O'
            elif char == '#':
                newRow += '.'*dotCount + '#'
                dotCount = 0
        newRow += '.'*dotCount
        res.append(newRow)
    return res

def tilt(grid, direction):
    if direction == 'W':
        return tiltWest(grid)
    if direction == 'E':
        return flipVertical(tiltWest(flipVertical(grid)))
    if direction == 'N':
        return transpose(tiltWest(transpose(grid)))
    if direction == 'S':
        return transpose(flipVertical(tiltWest(flipVertical(transpose(grid)))))
        
def tiltCycle(grid, cycles = 1):
    tiltSeq = ['N', 'W', 'S', 'E']
    for _ in range(cycles):
        for direction in tiltSeq:
            # print("\n".join(grid),'\n')
            grid = tilt(grid, direction)
    return grid


def groupLoad(stoneCount, maxLoad):
    # just an arithmetic sum maxLoad + (maxLoad - 1) + (maxLoad - 2) + ... + (maxLoad - stoneCount + 1)
    return stoneCount*(2*maxLoad - stoneCount + 1)//2 

def columnLoad(columnStoneSeq, columnLen):
    res = 0
    loadAbove = columnLen + 1
    for stoneType, x in columnStoneSeq:
        if stoneType == '#':
            loadAbove = x
        else:
            res += groupLoad(x, loadAbove - 1)
    return res

def main():
    grid = []
    with open("input14.txt") as file:
        for row in file:
            grid.append(row.strip())
    
    # ans1 = 0
    # for col in transpose(grid):
    #     ans1 += columnLoad(stoneSeq(col), len(col))

    Ngrid = tilt(grid, 'N')
    ans1_2 = sum(map(sum, roundStonePlacements(transpose(Ngrid))))
    
    
    # print("\n".join(grid),'\n')
    # print('\n'.join(tilt(grid, 'N')),'\n')
    # print("\n".join(tiltCycle(grid, 1)),'\n')
    # print("\n".join(tiltCycle(grid, 2)),'\n')
    # print("\n".join(tiltCycle(grid, 3)),'\n')
    totCycles = 1000000000

    newGrid = tiltCycle(grid)
    currentSeq = roundStonePlacements(newGrid)
    stoneSequences = {roundStonePlacements(grid): 0}
    cycleCount = 1
    while currentSeq not in stoneSequences:
        stoneSequences[currentSeq] = cycleCount
        # print("\n".join(newGrid),'\n')
        newGrid = tiltCycle(newGrid)
        cycleCount += 1
        currentSeq = roundStonePlacements(newGrid)
    
    cyclesToLoopStart = stoneSequences[currentSeq]
    repeatsAfter = cycleCount
    loopLen = repeatsAfter - cyclesToLoopStart
    for _ in range((totCycles - cyclesToLoopStart) % loopLen):
        newGrid = tiltCycle(newGrid)
    
    ans2 = sum(map(sum, roundStonePlacements(transpose(newGrid))))

    print(f"Task 1: {ans1_2}\nTask 2: {ans2}")


if __name__ == '__main__':
    main()
