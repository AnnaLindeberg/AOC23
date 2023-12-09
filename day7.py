# Day 7 of Advent of Code 2023: Camel Cards
# https://adventofcode.com/2023/day/7
from collections import Counter
# sorry for this
fs = frozenset

def whatHand(cards, useJokers = False):
    signatureScore = {fs([(1,5)]):0, fs([(2,1),(1,3)]): 1, fs([(2,2),(1,1)]): 2, fs([(3,1),(1,2)]): 3,
                      fs([(3,1),(2,1)]): 4, fs([(4,1),(1,1)]): 5, fs([(5,1)]): 6}
    jokerMaps = {fs([(1,4)]): fs([(2,1),(1,3)]), fs([(2,1),(1,2)]): fs([(3,1),(1,2)]), 
                 fs([(2,2)]): fs([(3,1),(2,1)]), fs([(3,1),(1,1)]): fs([(4,1),(1,1)]),
                 fs([(4,1)]): fs([(5,1)]), fs([(1,3)]): fs([(3,1),(1,2)]), fs([(2,1),(1,1)]): fs([(4,1),(1,1)]),
                 fs([(3,1)]): fs([(5,1)]), fs([(1,2)]): fs([(4,1),(1,1)]), fs([(2,1)]): fs([(5,1)]),
                 fs([(1,1)]): fs([(5,1)]), fs(): fs([(5,1)])}
    # hacky
    if useJokers:
        cards = cards.replace('J','')
    # not my proudest or most readable code..... see readme
    signature = fs((k,v) for k,v in Counter(Counter(cards).values()).items())
    if useJokers and len(cards) < 5:
        signature = jokerMaps[signature]
    
    return signatureScore[signature]


def sortHands(hands, useJokers = False):
    if useJokers:
        cardOrder = "J23456789TQKA"
    else:    
        cardOrder = "23456789TJQKA"
    def customCompare(hand):
        return (whatHand(hand[0], useJokers), cardOrder.index(hand[0][0]),  cardOrder.index(hand[0][1]), cardOrder.index(hand[0][2]),  cardOrder.index(hand[0][3]),  cardOrder.index(hand[0][4]))
    return sorted(hands, key=customCompare)

def calcWinnings(hands, useJokers = False):
    hands = sortHands(hands, useJokers)
    
    winnings = 0
    for rank, hand in enumerate(hands, start=1):
        bid = hand[1]
        winnings += rank * bid
    return winnings

def main():
    hands = []
    with open("input7.txt") as file:
        for row in file:
            hand, bid = row.strip().split()
            bid = int(bid)
            hands.append((hand, bid))
    
    print(f"Task 1: {calcWinnings(hands)}\nTask 2: {calcWinnings(hands, useJokers=True)}")


if __name__ == '__main__':
    main()
