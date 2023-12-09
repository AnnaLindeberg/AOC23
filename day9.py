# Day 9 of Advent of Code 2023: Mirage Maintenance
# https://adventofcode.com/2023/day/9

def diffSeq(seq):
    res = []
    for i, j in zip(seq, seq[1:]):
        res.append(j-i)
    return res

def predictNext(seq):
    if seq == [0]*len(seq):
        return 0
    else:
        return seq[-1] + predictNext(diffSeq(seq))

def extapolateBackwards(seq):
    if seq == [0]*len(seq):
        return 0
    else:
        return seq[0] - extapolateBackwards(diffSeq(seq))

def main():
    task1sum = 0
    task2sum = 0
    with open("input9.txt") as file:
        for row in file:
            seq = list(map(int, row.strip().split()))
            task1sum += predictNext(seq)
            task2sum += extapolateBackwards(seq)

    print(f"Task 1: {task1sum}\nTask 2: {task2sum}")


if __name__ == '__main__':
    main()
