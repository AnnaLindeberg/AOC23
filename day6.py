# Day 6 of Advent of Code 2023: Wait For It
# https://adventofcode.com/2023/day/6
from math import sqrt, ceil, floor

def calcInterval(T, M):
    if 4*M > T**2:
        print("warning!!")
    offset = sqrt(T**2 - 4*M) - 0.000001
    #add a little bit of extra to avoid exactness (crude solution...)
    low = ceil((T-offset)/2)
    high = floor((T+offset)/2)
    return low, high

def main():
    # for task 1
    with open("input6.txt") as file:
        times = list(map(int, file.readline().strip().split()[1:]))
        dists = list(map(int, file.readline().strip().split()[1:]))
    
    TtoM = list(zip(times, dists))
    
    margin = 1
    for T, M in TtoM:
        low, high = calcInterval(T, M)
        # print(f"low {low} high {high} wins {high-low + 1}")
        margin *= high - low + 1
    
    # for task 2
    time = int("".join(map(str, times)))
    dist = int("".join(map(str, dists)))
    low, high = calcInterval(time, dist)
    ways2win = high-low +1

    print(f"Task 1: {margin}\nTask 2: {ways2win}")


if __name__ == '__main__':
    main()
