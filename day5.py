# Day 5 of Advent of Code 2023: If You Give A Seed A Fertilizer
# https://adventofcode.com/2023/day/5
from collections import namedtuple
from operator import attrgetter

Range = namedtuple('Range', ['dest_start', 'source_start','len'])

class GardenMap:
    def __init__(self, ranges, nameRow) -> None:
        splitName = nameRow.split('-')
        self.input = splitName[0]
        self.output = splitName[-1].split()[0]
        self.ranges = sorted(ranges, key=attrgetter('source_start'))
        self.firstRangeStart = self.ranges[0].source_start
    
    def __getitem__(self, idx):
        if isinstance(idx, int):
            if idx < self.firstRangeStart:
                return idx
            for range in self.ranges:
                if range.source_start <= idx < range.source_start + range.len:
                    return range.dest_start + (idx - range.source_start)
                elif range.source_start > idx:
                    return idx
            return idx
        if isinstance(idx, slice):
            start, end= idx.start, idx.stop
            if (idx.step is not None) or (None in [start, end]) or (end < start):
                raise TypeError("invalid slicing")

            image = []
            for range in self.ranges:
                # range is [a,b)
                a, b = range.source_start, range.source_start + range.len
                if start >= b:
                    continue
                elif end <= a:
                    image.append((start, end))
                    return image
                elif start < a:
                    if end <= b:
                        image.append((start, a)) 
                        image.append((range.dest_start, range.dest_start + (end - a)))
                        return image
                    else:
                        image.append((start,a))
                        image.append((range.dest_start, range.dest_start + range.len))
                        start = a
                else: # ie a <= start < b
                    if end <= b:
                        image.append((range.dest_start + (start-a), range.dest_start + (end - a)))
                        return image
                    else:
                        image.append((range.dest_start + (start-a), range.dest_start + range.len))
                        start = b
            if start < end:
                image.append((start,end))
            return image

        else:
            raise TypeError("invalid index")
    
    def __str__(self) -> str:
        return f"{self.input}-to-{self.output}"
    
    def __repr__(self) -> str:
        return f"{self.input}-to-{self.output}"
        

def minLocation(allMaps, seeds):
    locations = []
    for seed in seeds:
        currentType = 'seed'
        source = seed
        while currentType != 'location':
            currentMap = allMaps[currentType]
            source = currentMap[source]
            currentType = currentMap.output
        locations.append(source) 
    return(min(locations))

def main():
    allMaps = dict()
    with open("input5.txt") as file:
        seeds = list(map(int, file.readline().strip().split()[1:]))
        file.readline()
        ranges = []
        name = ""
        for row in file:
            if len(row.strip()) == 0:
                newMap = GardenMap(ranges, name)
                allMaps[newMap.input] = newMap

                ranges = []
            elif not row[0].isnumeric():
                name = row
            else:
                r = Range(*map(int, row.strip().split()))
                ranges.append(r)
        # don't forget the last one (extra blankline didn't work?)
        newMap = GardenMap(ranges, name)
        allMaps[newMap.input] = newMap
    
    #mostly for debug...
    del r, ranges, newMap, row, file, name

    task1ans = minLocation(allMaps, seeds)
    
    
    # for second task: locate intervals in input
    intervals = []
    for i in range(0, len(seeds), 2):
        intervals.append((seeds[i], seeds[i]+seeds[i+1]))
    
    # then map intervals to intervals rather than ints to ints
    possibleMin = []
    for interval in intervals:
        currentType = 'seed'
        images = [interval]
        while currentType != 'location':
            updatedImages = []
            currentMap = allMaps[currentType]
            for s, e in images:
                updatedImages += currentMap[s:e]
            images = updatedImages
            currentType = currentMap.output
        
        possibleMin.append(min(min(images)))
    
    task2ans = min(possibleMin)
    
    print(f"Task 1: {task1ans}\nTask 2: {task2ans}")

if __name__ == '__main__':
    main()
