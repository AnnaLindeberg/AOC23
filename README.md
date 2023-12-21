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

## Day 11: Cosmic Expansion

I figured things would just get large in part 2, and indeed that was what happened. Thus the approach of counting "normal" steps in x resp y-direction separately from steps over vast space (empty rows and columns, whose indices were parsed into separate sets) for part 1 meant part 2 was written with only two extra rows. Possibly my quickest solution to part 2 after part 1 ever?

## Day 12: Hot Springs

Alright: rewrote the code for part 1 from scratch and got it to work – although I didn't really re-think the solution? Oh well. Now pondering the second part, I *think* you need to be clever about it, but I think I'll try to just brute-force it first...

Update: it did, as expected, nt work to just do the same thing :) I'm now thinking some sort of dynamic programming approach... For later, if ever.

## Day 13: Point of Incidence

Had to actually finish another before trying day 12 again – day 13 was manageable. First I somehow made it much more complicated than it needed to be – I think I assumed that the input grids would be much, much larger (not just many grids), so after I singled out pairs of indices (i,j) of rows (or columns) that are equal I tried to infer what symmetry axis was valid from that – turned out to be tricky to actually figure out *how* though. Got it to work on the example, but something was repeatedly off with the real input. To get it to work I  instead generated what pairs of indices where needed for a fold between two indices (iterating over all possible lines of symmetry), checking if all those were present in the set of equal-row-pairs (resp. equal-column-pairs). That was easy to write and worked fine – instant runtime, even with an added almost-equal-check required by part 2 (that by luck, I suppose, was very easy to add on top of the code for part 1).

## Day 14: Parabolic Reflector Dish

Made a clever ("clever") solution on part 1 where I didn't actually move any stones, just computed the load from the initial configuration directly. Unfortunately, I *had* to move stones on the second part either way, so that was a bit all-for-nothing. For the second part I falsely assumed the loop would start at the initial configuration, though, and didn't get it to work for quite some time. Oh well, realized the mistake just before falling asleep and got the solution after 2 minutes this morning. Should clean up the code for this one –– I'll probably never though that...

## Day 15: Lens Library

This was very easy to be day 15?? Possible well-suited for python, but really just parsing text into code and nothing else.

## Day 16 : The Floor Will Be Lava

Well it sounded straightforward with part 1, and it was by just using a queue and a sort of BFS. Thought it would be harder in part 2 (moving around mirrors?) but I could brute-force it by testing all possible starting positions and the runtime was still only a couple of seconds (didn't even have time to think of interrupting it). Still at it, in other words! I usually give up around here each year...

## Day 17: Clumsy Crucible

Aaah okay a modified Dijkstras (or not really, I guess it's really a question on how you generate the graph?) works on the small input, but my implementation is too slow to run on the full thing. If I get the time and urge, I'll test building a networkX-graph from the grid and use their shortest-path algorithm instead. Also: I should really, really start using numpy-arrays instead of tuples for coordinates, so that I stop doing ad-hoc addition of vectors etc.

## Day 18: Lavaduct Lagoon

I did part 1 of this quite similarly as the loop-counting on day 10 (with the pipes), in essence reading left-to-right. Kept track of what points where interior on the row before to keep track of passing over bends though, as this couldn't be figured out from the #-symbols though. For part 2 I realized that I needed to use my initial idea of counting sub-areas while reading the input. In essence, it would be counting area horizontally only, storing down/up steps in a stack. There's some details missing right now, but it is a fun little problem so I might come back to it later!

## Day 21: Step Counter

Took a break for a couple of days, and wrote the solution for part 1 very quickly and brute-force-ish. Don't really know how part 2 would be solved...