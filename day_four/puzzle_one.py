# Forklifts can access roll if there are fewer than four rolls of paper in the eight adjacent cells
# How many rolls of paper can the forklifts access?

def count_accessible_rolls(warehouse_grid: list[list[str]]) -> int:
    """Counts the number of rolls of paper accessible to forklifts in the warehouse.

    Args:
        warehouse_grid (list[list[str]]): 2D grid representing the warehouse layout

    Returns:
        int: Total number of accessible rolls of paper
    """
    rows = len(warehouse_grid)
    cols = len(warehouse_grid[0]) if rows > 0 else 0
    accessible_rolls = 0

    for r in range(rows):
        for c in range(cols):
            if warehouse_grid[r][c] == '@':  # Found a roll of paper
                adjacent_rolls = 0
                # Check all adjacent cells
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue  # Skip the current cell
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if warehouse_grid[nr][nc] == '@':
                                adjacent_rolls += 1
                if adjacent_rolls < 4:
                    accessible_rolls += 1

    return accessible_rolls

# Now we want to optimize for the forklifts to access the maximum number of rolls
# Maybe a dynamic programming approach or a greedy algorithm could work here
# We stop when the forklift cannot access any more rolls

# It's a path optimization problem now where we want to select the next position to maximize accessible rolls
def optimize_forklift_access(warehouse_grid: list[list[str]]) -> int:
    """Optimizes forklift access to maximize the number of rolls of paper accessed.

    Args:
        warehouse_grid (list[list[str]]): 2D grid representing the warehouse layout

    Returns:
        int: Maximum number of rolls of paper that can be accessed
    """
    rows = len(warehouse_grid)
    cols = len(warehouse_grid[0]) if rows > 0 else 0
    accessed = [[False for _ in range(cols)] for _ in range(rows)]
    total_accessed = 0

    def can_access(r: int, c: int) -> bool:
        """
        Checks if the forklift can access the roll at (r, c)
        based on the current state of accessed rolls.
        """
        if warehouse_grid[r][c] != '@' or accessed[r][c]:
            return False
        adjacent_rolls = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if warehouse_grid[nr][nc] == '@' and not accessed[nr][nc]:
                        adjacent_rolls += 1
        return adjacent_rolls < 4

    # Iteratively access rolls until no more can be accessed
    made_progress = True
    while made_progress:
        made_progress = False # Reset for this iteration
        for r in range(rows): # Loop through each cell
            for c in range(cols): # Loop through each cell
                if can_access(r, c): # If we can access this roll
                    accessed[r][c] = True # Mark it as accessed
                    total_accessed += 1 # Increment count
                    made_progress = True # We made progress this iteration which means we need to check again

    return total_accessed

# How could this be optimized further? Maybe a more advanced search algorithm?
# It's currently an O(n^2) approach with multiple passes through the grid
# If we wanted to get fancy we could implement A* or Dijkstra's algorithm to find optimal paths

if __name__ == "__main__":
    # Read warehouse layout from file
    with open("./puzzle_input.txt", "r") as file:
        warehouse_layout = [list(line.strip()) for line in file.readlines()]

    total_accessible_rolls = count_accessible_rolls(warehouse_layout)
    print(f"Total accessible rolls of paper: {total_accessible_rolls}")

    # Calculate optimized access
    optimized_access = optimize_forklift_access(warehouse_layout)
    print(f"Optimized accessible rolls of paper: {optimized_access}")