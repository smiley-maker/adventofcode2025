def solve_part_two(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    # ways[r][c] = number of timelines where a beam is at this cell
    ways = [[0] * cols for _ in range(rows)]
    
    # Find the starting point S
    for c in range(cols):
        if grid[0][c] == 'S':
            ways[0][c] = 1

    for r in range(rows - 1):
        for c in range(cols):
            if ways[r][c] == 0:
                continue
            
            # Current number of timelines passing through this cell
            current_ways = ways[r][c]
            target_cell = grid[r+1][c]
            
            if target_cell == "^":
                # Splitting logic: This timeline branches into two!
                # One timeline where it goes left, one where it goes right.
                if c - 1 >= 0:
                    ways[r+1][c-1] += current_ways
                if c + 1 < cols:
                    ways[r+1][c+1] += current_ways
            else:
                # Regular path: Timeline continues straight down
                ways[r+1][c] += current_ways
                
    # The answer is the sum of all timelines that reached the bottom row
    return sum(ways[-1])

if __name__ == "__main__":
    with open("./puzzle_input.txt") as f:
        # Using .strip() to avoid newline issues and converting to list of lists
        grid = [list(line.strip()) for line in f.readlines()]

    rows = len(grid)
    cols = len(grid[0])
    splits = 0

    # Iterate row by row
    for r in range(rows - 1): # Stop at the second to last row since we look at r+1
        for c in range(cols):
            # If the current cell contains a beam (S or |)
            if grid[r][c] == "S" or grid[r][c] == "|":
                
                # Check the cell directly below
                target_cell = grid[r+1][c]
                
                if target_cell == "^":
                    # We hit a splitter! 
                    splits += 1
                    # Propagate left and right in the row below if within bounds
                    if c - 1 >= 0:
                        grid[r+1][c-1] = "|"
                    if c + 1 < cols:
                        grid[r+1][c+1] = "|"
                else:
                    # No splitter, just move the beam straight down
                    grid[r+1][c] = "|"
    
    print(f"There were {splits} splits.")

    # Part Two:
    # At each split, the particle has two options (left or right). 
    # That means that for a series of n splits, there should be 2^n-1 total combinations.
    ans = solve_part_two(grid)
    print(ans)