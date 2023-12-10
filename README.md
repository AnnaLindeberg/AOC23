# Advent of Code 2023

Coding on a deadline: end of nap time

## Day 2: Cube Conundrum

Well, I wrote stupid code to parse it and then stupid code to solve task 1 and then stupid code to solve task 2.

## Day 3: Gear Ratios

For task 1 I figured it was easier to look for each number and then look for symbols not equal to . in the positions around each number. This approach was pretty easy, but it only finds a number if there is a . after it: hence a quick-fix of appending a . to each line. Didn't catch that from the small example input... Of course also messed up the calculations of positions around the first time around: always best to do that type of thing on paper, I guess.

Luckily, the dictionary-approach of task 1 was very easy to adapt to finding the gears of task 2.

## Day 4: Scratchcards

This was very straightforward as well. Parse and count. But what do you actually win when you just win copies of scratchcards that win copies of scratchcards? Biggest question today.

## Day 5: If You Give A Seed A Fertilizer

Well now it got a bit interesting! First class of the year, one for each X-to-Y map. A good reminder about how to implement indexing of classes with `__getitem__`. Rather easy for the first task, but had to take a step back for the second. Tried to brute-force it at first, although I *new* it was pointless and stopped after say 30 sek. Slept on it. Then realized it's not too hard to determine what image a map of the natural numbers to the natural number have, given an interval. Then feed those intervals into the next map, and the next, etc. The case-distinction is a bit hairy and I for sure needed pen and paper, but then it, surprisingly, worked on the first try. Thanks to 5 years of math, I suppose. ps: could have merged intervals, but didn't. Works fast without it, so assume it isn't that big of a problem here.

## Day 6: Wait For It

Hehe thanks to math again. Count integer solutions for t of t(T-t) > M, given race time T and current record distance M. Same as solving -t^2+Tt-M = (t-R)(t+R) > 0 where R = (T +- sqrt(T^2 - 4M))/2. Solutions in interval [-R, R], where -R should be ceil:ed and R should be floor:ed. At least I thought: of course you get two solutions too much when M and T are so that R is an integer (eg T,M = 30,200). Kindly this was given in the test-input, so an easy catch. The rather crude (but working) solution for me was to offset R with a small amount.

## Day 7: Camel Cards

This has way, way, way to much manual work behind it, and som horribly unreadable pieces of code. Take:
```signature = frozenset((k,v) for k,v in Counter(Counter(cards).values()).items())```
which calculates a unique signature for each type of hand. The (rather neat, though) Counter from collections is new to me but makes a dict with value:count pairs, where the values come from an iterable. So `Counter('AQA7Q')` yield `{'A':2,'Q':2,'7':1}`. Then we need to forget about the keys and just determine the number of keys that have the same value, so use Counter *again*... That is, `Counter(Counter('AQA7Q').values())=Counter([2,2,1])={2:2,1:1}` That, I forced into an unmutable frosenzet so that I could use it as a key in another dict ':)'.

I don't want to defend my choice of manually finding what Joker-containing-hand should map to what best-possible-hand. It is what it is and it's both prone to error and without finesse. But it worked on the second try!

## Day 8: Haunted Wasteland

Hm. I did get two stars on this, but I am still not convinced as to why my solution to part 2 works. For one thing: I'm used to (informally, quickly) proving to my self that a written solution will work on the input, but here I made a lot of extractions from the input and used short patterns as proof (euw?). That is: each \*\*A (1) ends up in a loop, (2) ends up on a loop with only one \*\*Z and (3) the length of the LR-sequence somehow is irrelevant (mod = 0?!). It looked chinese remainder:y, but it isn't. Actually, it looks like there's numbers a and b for each start \*\*A such that it reaches its \*\*Z the first time after a steps, and then every b steps over and over (irrespectively of where in the LR-seq we're at). It's thus something like solving  `x = a_1 + b_1*i_1 = ... = a_6 + b_6*i_6` for minimal x, not knowing the i:s. But that was wrong (I plugged it into mathematica...)? playing around with the small input, lcm(a_1,a_2) worked there, and somehow, for the large input as well. What on earth?

## Day 9: Mirage Maintenance

Recursion is a girl's best friend?

## Day 10: Pipe Maze

OK this took some time. Or, task1 was straightforward, walking through the loop from the starting position (or actually a hardcoded position next to the starting position...), counting its length and dividing by two. For task two I had to think about it for a while, having some sort of idea of BFS from a position inside the loop (or outside, using some sort of exclusion in the end). That would have to use half-point coordinates though, to squeeze between pipes and that got difficult to understand. Then thought about expanding the maze to create space between all pipes, find positions inside the loop in one contiguous group, and remove all "added" coordinates from the expansion. Almost implemented but am glad I didn't. In the end much more straight-forward: when you pass over a `|`  from left to right, you step inside or outside of the loop, then need to be careful about patterns as `L-7` `L-J` `F-7` and `F-J`, ie bendy parts where you sometimes step in/out, sometimes not. Ended up with it working on all examples, but not the real input. Difficult debug since no examples I could think of failed. Culprit you asked? The damned 'S' indicating the starting position. AAAAA. Looked in the input and manually replaced it with `|` (during runtime) and all was well. Pfft.