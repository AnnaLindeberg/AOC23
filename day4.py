# Day 4 of Advent of Code 2023: Scratchcards
# https://adventofcode.com/2023/day/4

def calcWins(numbers, winners):
    count = 0
    for num in numbers:
        if num in winners:
            count +=1
    return count

def calcScore(wins):
    if wins > 0:
        return 2**(wins - 1)
    else:
        return 0

def main():
    winsPerCard = dict()
    with open("input4.txt") as file:
        for row in file:
            cardNo = int(row.split(':')[0].split()[-1])
            nums, winning = row.split(':')[-1].strip().split('|')
            nums = list(map(int, nums.strip().split()))
            winning = set(map(int, winning.strip().split()))
            
            winsPerCard[cardNo] = calcWins(nums, winning)

    # for task 1
    totScore = sum(map(calcScore, winsPerCard.values()))

    # for task 2
    copiesPerCard = dict()
    for card in range(1, len(winsPerCard)+1):
        copiesPerCard[card] = 1
    
    for card, wins in winsPerCard.items():
        copiesOfThisCard = copiesPerCard[card]
        for i in range(1, wins + 1):
            copiesPerCard[card + i] += copiesOfThisCard
    
    totCards = sum(copiesPerCard.values())

    print(f"Task 1: {totScore}\nTask 2: {totCards}")


if __name__ == '__main__':
    main()
