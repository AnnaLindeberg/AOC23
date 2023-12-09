# Day 2 of Advent of Code 2023: Cube Conundrum
# https://adventofcode.com/2023/day/2

template_handful = {"red":0, "blue":0,"green":0}

def main():
    with open("input2.txt") as file:
        games = dict()
        for row in file:
            game, hands = row.strip().split(':')
            game = int(game.split()[-1])
            games[game] = []
            for hand in hands.strip().split(';'):
                handful = template_handful.copy()
                for cubes in hand.strip().split(','):
                    cubes = cubes.strip().split()
                    handful[cubes[-1]] = int(cubes[0])
                games[game].append(handful)
    
    # task 1: sum possible games where the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes
    sum = 0    
    # task 2: power(game) = multiplication of smallest no of possible cubes in each color. answer with sum of all powers
    powers = 0
    for g, game in enumerate(games.values(), start = 1):
        gameOK = True
        minR, minG, minB = 0, 0, 0
        for handful in game:
            # for task 1: determine if game is valid
            if handful['red'] > 12 or handful['green'] > 13 or handful['blue'] > 14:
                gameOK = False
            # for task 2: update min no of cubes in each color
            if handful['red'] > minR:
                minR = handful['red']
            if handful['green'] > minG:
                minG = handful['green']
            if handful['blue'] > minB:
                minB = handful['blue']
        
        # update count for task 1
        if gameOK:
            sum += g
        
        # update power for task 2
        powers += minR*minG*minB

    print(f"Task 1: {sum}\nTask 2: {powers}")


if __name__ == '__main__':
    main()
