def largest_joltage(nums: str) -> int:
    """Finds the two batteries that form the largest number when concatenated."""
    max_joltage = 0
    for i in range(len(nums)):
        for j in range(i+1, len(nums)): # Not allowed to reorder or use the same battery
            concatenated = int(nums[i] + nums[j])
            if concatenated > max_joltage:
                max_joltage = concatenated
    return max_joltage

def largest_sequence_of_twelve(nums: str) -> int:
    """Finds the largest value produced by any twelve batteries in the string (doesn't have to be contiguous)."""
    # We can use a dynamic programming approach to find the largest concatenated value of length 12
    # The general idea is to maintain a table where dp[i][j] represents the largest value
    # that can be formed using the first i batteries to create a sequence of length j.
    # The final answer will be in dp[n][12] where n is the length of nums.
    n = len(nums)
    if n < 12:
        return 0  # Not enough batteries to form a sequence of 12
    dp = [[0] * (13) for _ in range(n + 1)]  # dp[i][j] = largest value using first i batteries to form j-length sequence
    for i in range(1, n + 1):
        for j in range(1, min(i, 12) + 1):
            # Option 1: Skip the current battery
            dp[i][j] = dp[i - 1][j]
            # Option 2: Use the current battery
            candidate = dp[i - 1][j - 1] * 10 + int(nums[i - 1])
            if candidate > dp[i][j]:
                dp[i][j] = candidate
    return dp[n][12]


if __name__ == "__main__":
    with open("./puzzle_three_input.txt", "r") as file:
        batteries = [line.strip() for line in file.readlines()]
        
    # Batteries is a list of strings. Loop through each and sum the largest joltages
    total_joltage = 0
    for battery in batteries:
        total_joltage += largest_joltage(battery)
    
    print(f"Total largest joltage from all batteries: {total_joltage}")

    # Now find the largest sequence of 12 in each battery and sum those
    total_sequence_joltage = 0
    for battery in batteries:
        total_sequence_joltage += largest_sequence_of_twelve(battery)

    print(f"Total largest sequence of 12 joltage from all batteries: {total_sequence_joltage}")