def calculate_sequence(instructions : list[str]) -> int:
    """Calculates the total number of times the lock passes position 0
       during a sequence of rotations.

    Args:
        instructions (list[str]): List of instructions to rotate the lock

    Returns:
        int: Total number of times the lock passed position 0
    """
    base = 50  # Start at 50 per instructions
    total_zeros = 0
    
    for instruction in instructions:
        if not instruction: continue
            
        direction = instruction[0]
        amount = int(instruction[1:])
        
        if direction == "R":
            # Count multiples of 100 crossed moving up
            # (Excludes start, Includes end)
            passes = (base + amount) // 100 - base // 100
            total_zeros += passes
            
            base = (base + amount) % 100

        elif direction == "L":
            # Count multiples of 100 crossed moving down
            # (Includes end, Excludes start)
            passes = (base - 1) // 100 - (base - amount - 1) // 100
            total_zeros += passes
            
            base = (base - amount) % 100
            
    return total_zeros

if __name__ == "__main__":
    with open("./puzzle_one_input.txt", "r") as file:
        instructions = file.read().strip().split("\n")

    ans = calculate_sequence(instructions)
    print(f"Total zero visits: {ans}")