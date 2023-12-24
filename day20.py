# Day 20 of Advent of Code 2023: Pulse Propagation
# https://adventofcode.com/2023/day/20
from collections import namedtuple, deque

FlipFlop = namedtuple('FlipFlop', ['name', 'isOn', 'outModules'])
Conjuction = namedtuple('Conjuction', ['name', 'recentPulses', 'outModules'])
Broadcaster = namedtuple('Broadcaster', ['name', 'outModules'])
UnTyped = namedtuple('UnTyped', ['name'])


LOW = 0
HIGH = 1
 
# Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

# Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

# There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.

def dealWithPulse(module, pulseType, sentFrom = None):
    if isinstance(module, FlipFlop):
        if pulseType is LOW:
            updatedModule = FlipFlop(module.name, not module.isOn, module.outModules)
            if module.isOn:
                pulsesSent = [(module.name, toMod, LOW) for toMod in module.outModules]
            else:
                pulsesSent = [(module.name, toMod, HIGH) for toMod in module.outModules]
            return updatedModule, pulsesSent
        else:
            return module, []
    elif isinstance(module, Conjuction):
        newStatus = tuple((name, prevPulse) if name != sentFrom else (name, pulseType) for name, prevPulse in module.recentPulses)
        updatedModule = Conjuction(module.name, newStatus, module.outModules)
        areAllHIGH = all(t[-1] for t in newStatus)
        if areAllHIGH:
            pulsesSent = [(module.name, toMod, LOW) for toMod in module.outModules]
        else:
            pulsesSent = [(module.name, toMod, HIGH) for toMod in module.outModules]
        return updatedModule, pulsesSent
    elif isinstance(module, Broadcaster):
        pulsesSent = [(module.name, toMod, pulseType) for toMod in module.outModules]
        return module, pulsesSent
    else: # is an untyped module
        return None, None

def pushButton(modules):
    highPulseCount, lowPulseCount = 0, 0
    pulsesToDealWith = deque()
    pulsesToDealWith.append(('button', 'broadcaster', LOW))
    while pulsesToDealWith:
        fromModule, toModule, pulseType = pulsesToDealWith.popleft()
        if pulseType is LOW:
            lowPulseCount += 1
        else:
            highPulseCount += 1

        if toModule == 'rx' and pulseType == LOW:
            print("hey")

        updatedModule, newPulses = dealWithPulse(modules[toModule], pulseType, fromModule)

        if updatedModule is None:
            continue

        modules[updatedModule.name] = updatedModule
        for pulse in newPulses:
            pulsesToDealWith.append(pulse)

    return highPulseCount, lowPulseCount, modules

def pushButtonManyTimes(modules, n):
    originalModules = modules.copy()
    highPulseCount, lowPulseCount = 0, 0
    i = 1
    while i <= n:
        hc, lc, modules = pushButton(modules)
        highPulseCount += hc
        lowPulseCount += lc
        if modules == originalModules:
            highPulseCount = highPulseCount*(n//i)
            lowPulseCount = lowPulseCount*(n//i)
            break
        else:
            i += 1
    return highPulseCount, lowPulseCount
        
    

def parseFile(name):
    modules = {}
    sendsTo = []
    with open(name) as file:
        for row in file:
            if row[0] == '%':
                # flop flop module found
                name, destinationModules = row[1:].strip().split(' -> ')
                destinationModules = tuple(destinationModules.split(', '))
                modules[name] = FlipFlop(name, False, destinationModules)
                sendsTo += [(name, mod) for mod in destinationModules]
            elif row[0] == '&':
                name, destinationModules = row[1:].strip().split(' -> ')
                destinationModules = tuple(destinationModules.split(', '))
                # don't know where it receives pulses from yet – will fix that later
                modules[name] = Conjuction(name, (), destinationModules) 
                sendsTo += [(name, mod) for mod in destinationModules]
            else:
                #found the broadcaster
                destinationModules = (row.strip().split(' -> ')[-1]).split(', ')
                modules['broadcaster'] = Broadcaster('broadcaster', tuple(destinationModules))
                sendsTo += [('broadcaster', mod) for mod in destinationModules]
    
    for fromMod, toMod in sendsTo:
        if toMod not in modules:
            modules[toMod] = UnTyped(toMod)
        if isinstance(modules[toMod], Conjuction):
            extendedRecieveModules = tuple(list(modules[toMod].recentPulses) + [(fromMod, LOW)])
            modules[toMod] = Conjuction(toMod, extendedRecieveModules, modules[toMod].outModules)
    
    return modules

def main():
    modules = parseFile("input20.txt")
    modCopy = modules.copy()
    highCount, lowCount = pushButtonManyTimes(modules, 100000)
    res1 = highCount*lowCount



    print(f"Task 1: {res1}\nTask 2: {0}")


if __name__ == '__main__':
    main()
