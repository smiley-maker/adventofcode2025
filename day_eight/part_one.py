import math

if __name__ == "__main__":
    # Load the data
    with open("./puzzle_input.txt") as f:
        lines = [l.strip().split(",") for l in f.readlines()]
    
    print(lines[:10])

    # Calculate all distances
    distances = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            p1 = [int(x) for x in lines[i]]
            p2 = [int(x) for x in lines[j]]
            # Euclidean distance
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
            distances.append((dist, i, j))

    # Sort to get the closest pairs
    distances.sort()
    print(distances[-1])

    # Initialize Union-Find
    # Each point starts in its own set
    parent = list(range(len(lines)))

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i]) # Path compression
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j # Merge the two sets
            return True
        return False

    # Connect the first 1000 pairs
    for dist, i, j in distances[:1000]: # Take only the top 1000
        union(i, j)

    # Count circuit sizes
    circuit_counts = {}
    for i in range(len(lines)):
        root = find(i)
        circuit_counts[root] = circuit_counts.get(root, 0) + 1

    sizes = sorted(circuit_counts.values(), reverse=True)

    # Calculate result
    answer = sizes[0] * sizes[1] * sizes[2]
    print(f"The answer is {answer}")

    # For part two, we need to multiply the x coordinates of the pair that 
    # connects everything into a single circuit, with no limit on the number of pairs.
    parent = list(range(len(lines)))
    total_pairs = 0
    # Loop through all distances until all points are connected
    answer_part_two = 0
    for dist, i, j in distances:
        if union(i, j):
            total_pairs += 1
            # Check if all points are connected
            if len(set(find(x) for x in range(len(lines)))) == 1:
                print(f"All points connected with {total_pairs} pairs.")
                print(f"The distance of the last pair added is {dist}.")
                answer_part_two = int(lines[i][0]) * int(lines[j][0])
                break
    
    print(f"The answer to part two is {answer_part_two}.")