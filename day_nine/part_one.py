import numpy as np

if __name__ == "__main__":
    """
    Part one:
    The movie theater has a big tile floor with an interesting pattern. Elves here are redecorating the theater 
    by switching out some of the square tiles in the big grid they form. Some of the tiles are red; the Elves 
    would like to find the largest rectangle that uses red tiles for two of its opposite corners. They even have 
    a list of where the red tiles are located in the grid (your puzzle input).

    Using two red tiles as opposite diagonal corners, what is the largest area of any rectangle you can make?
    Puzzle input looks like:
    97926,50400
    97926,51618
    98025,51618
    98025,52819
    97711,52819
    97711,54079
    98234,54079
    ...
    where each line is a point (x,y).
    """

    """
    This code implements a brute-force solution for part one by comparing every pair of red tiles
    to calculate the area of the rectangle they would form as opposite corners. It keeps track of
    the maximum area found. 
    Might explore more efficient algorithms later if needed, such as sweep line or segment trees.
    """
    with open("./puzzle_input.txt") as f:
        # Ensure we handle the splitting correctly
        points = []
        for line in f:
            if line.strip():
                x, y = map(int, line.strip().split(','))
                points.append((x, y))

    max_area = 0

    # Compare every point i with every point j
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Calculate dimensions (including the tiles at the boundaries)
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            
            area = width * height
            
            if area > max_area:
                max_area = area

    print(f"The largest rectangle area is {max_area}")

    # Part two:
    """
    In your list, every red tile is connected to the red tile before and after 
    it by a straight line of green tiles. The list wraps, so the first red tile 
    is also connected to the last red tile. Tiles that are adjacent in your 
    list will always be on either the same row or the same column.

    In addition, all of the tiles inside this loop of red and green tiles are 
    also green. 

    The remaining tiles are never red nor green.

    The rectangle you choose still must have red tiles in opposite corners, but any 
    other tiles it includes must now be red or green. This significantly limits your options.

    Using two red tiles as opposite corners, what is the largest area of any rectangle you 
    can make using only red and green tiles?
    """

    """
    The code below implements a solution for part two. It uses a Maximum Empty Rectangle by Coordinate Compression
    approach combined with a point-in-polygon test to determine which compressed grid cells are inside the polygon 
    formed by the red tiles. It then finds the largest rectangle that can be formed using only red and green tiles.
    Polygon Definition: Use the red cells as vertices to define the boundary segments of a rectilinear polygon.
    Coordinate Compression: Create a non-uniform grid by drawing lines through every x and y coordinate from the red tiles.
    Inside-Outside Mapping: Build a binary matrix where each cell is True if its midpoint is inside the polygon (calculated via Ray Casting).
    Histogram Heights: Process the matrix row-by-row, tracking the "cumulative height" of consecutive True cells.
    Area Maximization: For each row, treat the heights as a histogram and find the largest rectangle that fits under it 
    (ideally using the O(N) monotonic stack algorithm), while filtering for those specific Red Tile Corner coordinates.
    
    """

    def is_inside(x, y, poly):
        """
        Standard Ray Casting algorithm.
        x, y: Midpoint of the compressed cell.
        poly: List of (x, y) tuples representing red tiles in order.
        """
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            
            # Check if the ray (horizontal line to the right) crosses the edge
            # We use a strict inequality on one side to handle vertices
            if min(p1y, p2y) < y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        # Calculate the x-coordinate where the edge crosses height y
                        x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    
                    # If the point is to the left of the intersection, it's a hit
                    if p1x == p2x or x <= x_intersect:
                        inside = not inside
            p1x, p1y = p2x, p2y
            
        return inside

    def solve_part_2(poly):
        # 1. Get unique coordinates and sort them
        sorted_x = sorted(list(set(p[0] for p in poly)))
        sorted_y = sorted(list(set(p[1] for p in poly)))
        
        # Map coordinates to their index for quick lookup
        x_map = {val: i for i, val in enumerate(sorted_x)}
        y_map = {val: i for i, val in enumerate(sorted_y)}
        
        # 2. Create a compressed grid (M-1 x K-1)
        # grid[i][j] is True if the rectangle between sorted_x[i]:sorted_x[i+1] 
        # and sorted_y[j]:sorted_y[j+1] is inside the polygon
        rows, cols = len(sorted_y) - 1, len(sorted_x) - 1
        grid = np.zeros((rows, cols), dtype=bool)
        
        for r in range(rows):
            for c in range(cols):
                # Check midpoint of the compressed cell
                mid_x = (sorted_x[c] + sorted_x[c+1]) / 2
                mid_y = (sorted_y[r] + sorted_y[r+1]) / 2
                if is_inside(mid_x, mid_y, poly):
                    grid[r, c] = True

        # 3. Largest Rectangle in Binary Matrix (using original dimensions)
        max_area = 0
        heights = np.zeros(cols)
        
        for r in range(rows):
            # Update heights based on valid cells
            for c in range(cols):
                if grid[r, c]:
                    # Height here is the physical Y-distance
                    heights[c] += (sorted_y[r+1] - sorted_y[r])
                else:
                    heights[c] = 0
            
            # Calculate max rectangle in this 'histogram'
            # We need to consider the physical widths of the bins
            row_max = calculate_max_histogram(heights, sorted_x, sorted_y[r], sorted_y[r+1], set(poly))
            max_area = max(max_area, row_max)

        return max_area

    def calculate_max_histogram(heights, sorted_x, current_y_min, current_y_max, red_tiles_set):
        """
        heights: The current vertical spans of green/red tiles.
        sorted_x: The x-coordinates of our grid 'fences'.
        current_y_min/max: The top and bottom Y-coordinates of the current histogram row.
        red_tiles_set: A set of (x, y) tuples for O(1) lookup.
        """
        max_a = 0
        n = len(heights)
        
        # We check every possible sub-span of the current histogram row
        for left in range(n):
            min_h = float('inf')
            for right in range(left, n):
                # The height of a rectangle spanning from 'left' to 'right' 
                # is the minimum height in that range
                min_h = min(min_h, heights[right])
                
                if min_h == 0:
                    break # Cannot form a rectangle here
                
                # Potential corners of this rectangle
                x_start = sorted_x[left]
                x_end = sorted_x[right + 1]
                y_start = current_y_max - min_h
                y_end = current_y_max
                
                # THE RED TILE RULE:
                # Check if (x_start, y_start) and (x_end, y_end) are red tiles
                # OR if (x_start, y_end) and (x_end, y_start) are red tiles
                corner_pair_1 = ((x_start, y_start) in red_tiles_set and 
                                (x_end, y_end) in red_tiles_set)
                corner_pair_2 = ((x_start, y_end) in red_tiles_set and 
                                (x_end, y_start) in red_tiles_set)
                
                if corner_pair_1 or corner_pair_2:
                    width = (x_end - x_start) + 1
                    height = (y_end - y_start) + 1
                    max_a = max(max_a, width * height)
                    
        return max_a
    
    part_two_answer = solve_part_2(points)
    print(f"The largest rectangle area using red and green tiles is {part_two_answer}")