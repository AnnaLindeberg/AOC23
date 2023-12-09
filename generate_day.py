try:
    day = input("Day?: ")
    int(day)
    title = input("Title?: ")
except ValueError:
    quit()

with open("template.py") as template:
    with open(f"day{day}.py", 'w') as out:
        for line in template:
            out.write(line.replace('XX', day).replace('YY', title))

with open("README.md", 'a') as f:
    f.write(f"## Day {day}: {title}\n")
