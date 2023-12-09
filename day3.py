# Day 3 of Advent of Code 2023: Gear Ratios
# https://adventofcode.com/2023/day/3

def coordsAround(pos, len):
    coords = []
    x,y = pos
    for r in range(x-len-1,x+1):
        coords.append((r,y-1))
        coords.append((r,y+1))
    coords += [(x,y),(x-(len+1),y)]
    return coords

def filterCoords(coords, maxWidth, maxHeight):
    res = []
    for x,y in coords:
        if x < 0 or y < 0 or x >= maxWidth or y >= maxHeight:
            continue
        else:
            res.append((x,y))
    return res

def symbolsThatAppear(coords, grid):
    res = dict()
    for x,y in coords:
        s = grid[y][x]
        if s != '.' and not s.isnumeric():
            if s not in res:
                res[s] = [(x,y)]
            else:
                res[s].append((x,y))
            
    return res

def main():
    with open("input3.txt") as file:
        grid = list(map(lambda x: x.strip(), file.readlines()))

    for i, row in enumerate(grid):
        grid[i] = row + '.'
    
    width, height = len(grid[0]), len(grid)

    # for part 1
    sumPartNo = 0
    # for part 2
    gearInfo = dict()
    for y in range(height):
        activeNum = False
        currentNum = ''
        for x in range(width):
            charHere = grid[y][x]
            if charHere.isnumeric() and activeNum:
                currentNum += charHere
            elif charHere.isnumeric():
                activeNum = True
                currentNum = charHere
            elif activeNum: # at the position right after a number
                positions2check = filterCoords(coordsAround((x,y), len(currentNum)), width, height)
                symbsAround = symbolsThatAppear(positions2check, grid)
                # print(f"{currentNum}, {symbsAround}")
                
                #part 1: if there's a symbol around this number, add the part no to running total
                if len(symbsAround) > 0:
                    sumPartNo += int(currentNum)
                
                # part 2: store information about part numbers related to each '*' – those are potential gears
                if '*' in symbsAround:
                    for gearPos in symbsAround['*']:
                        if gearPos in gearInfo:
                            gearInfo[gearPos].append(int(currentNum))
                        else:
                            gearInfo[gearPos] = [int(currentNum)]

                activeNum = False
                currentNum = ''
    
    # for part 2: single out the actual gears. no great variable names here, gearInfo might contain non-gears...
    gearRatioSum = 0
    for gear in gearInfo.values():
        if len(gear) == 2:
            gearRatio = gear[0]*gear[1]
            gearRatioSum += gearRatio

    print(f"Task 1: {sumPartNo}\nTask 2: {gearRatioSum}")


if __name__ == '__main__':
    
    main()
