def rotate(direction : str, amount : int, base : int) -> int:
    """Determines the degree value of a circular lock after rotating
       degrees from amount in the given direction.

    Args:
        direction (str): L or R for left or right
        amount (_type_): The amount to rotate
        base (_type_): The starting position

    Returns:
        int: The value of the lock after rotation
    """
    if direction == "R":
        base = (base + amount) % 100
    elif direction == "L":
        base = (base - amount) % 100
    return base

def calculate_sequence(instructions : list[str]) -> tuple[int, int]:
    """Calculates the rotations provided in a sequence of instructions.

    Args:
        instructions (list): List of instructions to rotate the lock

    Returns:
        tuple[int, int]: Returns the final base position and the count of times
                         the lock returned to position 0
    """
    base = 50
    zero_count = 0
    for instruction in instructions:
        direction = instruction[0]
        amount = int(instruction[1:])
        base = rotate(direction, amount, base)
        if base == 0:
            zero_count += 1
    return base, zero_count

if __name__ == "__main__":
    # Read instructions from file
    with open("./puzzle_one_input.txt", "r") as file:
        instructions = file.read().strip().split("\n")

    final_base, zero_count = calculate_sequence(instructions)
    print(f"Final base position: {final_base}")
    print(f"Number of times returned to base (0): {zero_count}")