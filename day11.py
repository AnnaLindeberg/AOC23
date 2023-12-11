# Day 11 of Advent of Code 2023: Cosmic Expansion
# https://adventofcode.com/2023/day/11
from itertools import combinations

def distWithExpansion(a, b, emptyCoords):
    # one dimensional distance
    m, M = min(a,b), max(a,b)
    vastSpaceSteps = 0
    for i in range(m,M+1):
        if i in emptyCoords:
            vastSpaceSteps += 1
    return M - m - vastSpaceSteps, vastSpaceSteps

def distance(galaxy1, galaxy2, emptyRows, emptyColumns):
    x1, y1 = galaxy1
    x2, y2 = galaxy2
    xdist, xvastSpace = distWithExpansion(x1,x2,emptyColumns)
    ydist, yvastSpace = distWithExpansion(y1,y2,emptyRows)
    return xdist + ydist, xvastSpace + yvastSpace

def main():
    emptyRows = set()
    galaxies = set()
    with open("small_input11.txt") as file:
        for y, row in enumerate(file):
            emptyRow = True
            for x, pos in enumerate(row.strip()):
                if pos == '#':
                    emptyRow = False
                    galaxies.add((x,y))
            if emptyRow:
                emptyRows.add(y)
    
    del pos,row,file, emptyRow

    emptyCols = set([i for i in range(x)])
    for x, _ in galaxies:
        if x in emptyCols:
            emptyCols.remove(x)
    
    
    ans1 = 0
    ans2 = 0
    for galaxy1, galaxy2 in combinations(galaxies,2):
        normalDist, vastDist = distance(galaxy1, galaxy2, emptyRows, emptyCols)
        ans1 += normalDist + 2*vastDist
        ans2 += normalDist + 10**6*vastDist


    print(f"Task 1: {ans1}\nTask 2: {ans2}")


if __name__ == '__main__':
    main()
