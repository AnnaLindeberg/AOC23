# Day 19 of Advent of Code 2023: Aplenty
# https://adventofcode.com/2023/day/19
from collections import namedtuple
import operator
Part = namedtuple('Part', ['x','m','a','s'])
PartRanges  = namedtuple('PartRanges', ['nextWF', 'x','m','a','s'])

def workFlowFactory(ifConditions, finalOutput):
    def workFlow(part):
        attMap = {'x':part.x, 'm':part.m,'a':part.a, 's':part.s}
        for attribute, comparison, num, output in ifConditions:
            if comparison(attMap[attribute], num):
                return output
        return finalOutput
    return workFlow

def parseWF(row):
    # px{a<2006:qkq,m>2090:A,rfg}
    # should become
    # 'px', [('a', lt, 2006, 'qkq'), ('m', gt, 2090, 'A')], 'rfg'
    id, tmp = row.rstrip('}\n').split('{')
    tmp = tmp.split(',')
    out, tmp = tmp[-1], tmp[:-1]
    instr = []
    for strInstr in tmp:
        ifStat, thisout = strInstr.split(':')
        if '<' in ifStat:
            att, num = ifStat.split('<')
            comp = operator.lt
        else:
            att, num = ifStat.split('>')
            comp = operator.gt
        instr.append((att, comp, int(num), thisout))
    return id, instr, out

def parsePart(row):
    row = row.rstrip('}\n').lstrip('{').split(',')
    nums = [int(s[s.index('=')+1:]) for s in row]
    return Part(*nums)

def partsWithTheseSpecs(partRange):
    assert partRange.nextWF == 'A'
    res = 1
    for attribute in [partRange.x, partRange.m, partRange.a, partRange.s]:
        if attribute[0] < attribute[1]:
            res *= attribute[1] - attribute[0] + 1
        else:
            res = 0
    return res

def dictsToPartRange(name, minVals, maxVals):
    # assuming input dicts in same key-order (BAD but come on)
    ranges = list(zip(minVals.values(), maxVals.values()))
    return PartRanges(name, *ranges)

def main():
    workflows = {}
    workflowDescriptions = {}
    parts = []
    readingWorkflows = True
    with open("input19.txt") as file:
        for row in file:
            if len(row.strip()) == 0:
                readingWorkflows = False
                continue
            if readingWorkflows:
                id, instr, out = parseWF(row)
                workflowDescriptions[id] = (instr, out)
                workflows[id] = workFlowFactory(instr, out)
            else:
                parts.append(parsePart(row))

    # for part 1
    accepted = 0
    for part in parts:
        currentWorkFlowName = 'in'
        while currentWorkFlowName not in ['A', 'R']:
            currentWorkFlow = workflows[currentWorkFlowName]
            currentWorkFlowName = currentWorkFlow(part)
        if currentWorkFlowName == 'A':
            accepted += sum(part)
    
    ans1 = accepted
    # for part 2
    undealt = [PartRanges('in', (1,4000), (1,4000), (1,4000), (1,4000))]
    accepted = 0
    while len(undealt) > 0:
        newUndealt = []
        for partSpec in undealt:
            if partSpec.nextWF == 'A':
                accepted += partsWithTheseSpecs(partSpec)
                continue
            elif partSpec.nextWF == 'R':
                continue

            ifConds, elseOut = workflowDescriptions[partSpec.nextWF]
            xmas_min = {name: att[0] for att,name in [(partSpec.x,'x'), (partSpec.m,'m'), 
                                                      (partSpec.a,'a'), (partSpec.s, 's')]}
            xmas_max = {name: att[1] for att,name in [(partSpec.x,'x'), (partSpec.m,'m'), 
                                                      (partSpec.a,'a'), (partSpec.s, 's')]}
            for cond in ifConds:
                att, comparison, num, out = cond
                # create instance where this is achieved, and store the failing-cond in dicts
                if comparison == operator.lt:
                    tmp = xmas_max[att]
                    xmas_max[att] = num - 1
                    # succeeds
                    newUndealt.append(dictsToPartRange(out, xmas_min, xmas_max))
                    # restore swapped value and store failing it instead
                    xmas_max[att] = tmp
                    xmas_min[att] = num
                else: # comparison == operator.gt
                    tmp = xmas_min[att]
                    xmas_min[att] = num + 1
                    newUndealt.append(dictsToPartRange(out, xmas_min, xmas_max))
                    xmas_min[att] = tmp
                    xmas_max[att] = num
            # and finally the case when all if-conditions fail
            newUndealt.append(dictsToPartRange(elseOut, xmas_min, xmas_max))
        undealt = newUndealt

    print(f"Task 1: {ans1}\nTask 2: {accepted}")


if __name__ == '__main__':
    main()
