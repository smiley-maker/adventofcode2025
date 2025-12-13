if __name__ == "__main__":
    # We want to determine how many ingredients are fresh (fall in a range). 
    # First we need to load the file, which first lists the ranges, than an 
    # empty line, than the ingredients to check. 

    with open("./puzzle_input.txt") as f:
        data = f.readlines() # Returns a list of strings for each line
    
    print(data[:10])
    # Check how many lines there are until we get to the empty line. 
    line_count = 0
    for line in data:
        if line == "\n":
            break
        
        line_count += 1
    
    # This gives us a list of strings. The first line_count of them are ranges. 
    ranges = data[:line_count]
    ingredients = data[line_count+2:]

    # The ranges have the format x-y. Let's get a tuple of start and end points (ints) 
    # for each range in the list. 
    ranges = [(int(r.split("-")[0]), int(r.split("-")[1])) for r in ranges]

    # Now we can go through each item and check if it is in any range. 
    fresh_count = 0
    for ingredient in ingredients:
        for r in ranges:
            if int(ingredient) >= r[0] and int(ingredient) <= r[1]:
                fresh_count += 1
                break
    
    # print fresh count
    print(f"There are {fresh_count} fresh ingredients.")

    # For part two we need to count all the values in the ranges. 
    # It's inclusive, so we have (1,5) going to 1, 2, 3, 4, 5. 
    # Or (7, 9) going to 7, 8, 9. y-x+1. 
    # What about (0, 99)? 99-0+1 = 100 (yep)
    # The mathematical idea was good, but we need to eliminate numbers if we've seen them in 
    # a range before. We need the maximum covered area without overlaps. 

    # Basically we want the maximum non-overlapping ranges. 
    # sort the intervals based on their start time. 
    ranges.sort()
    merged = [ranges[0]]

    for interval in ranges:
        if interval[0] <= merged[-1][1]: # this interval starts before the last one ended.
            # Updated the stored range. 
            merged[-1] = (merged[-1][0], max(interval[1], merged[-1][1]))
        else:
            merged.append(interval)
    
    # Now we have a condensed list of intervals, we just take the numbers for each of them. 
    output = 0
    for interval in merged: 
        output += (interval[1] - interval[0]) + 1
    
    print(f"The number of fresh ingredients is {output}")
