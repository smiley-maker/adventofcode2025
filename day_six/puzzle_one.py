import pandas as pd

def rotate_matrix(m):
    """Rotates a 2D matrix so that the rows become columns

    Args:
        m (list[list]): 2D matrix to be rotated.
    """

    transposed = [list(row) for row in zip(*m)]
    rotated = [row[::-1] for row in transposed]
    return rotated

def solve_problem(row : list) -> int:
    """Solves a math problem for a given row where the operation is the first element.

    Args:
        row (list): List of numbers and an operation to do with all the numbers (e.g. +, *)
    """

    # Get the operation and data
    operation = row[0]
    data = [int(r.strip()) for r in row[1:] if r.strip() != '']

    # roll up the data with the operation
    if operation == "+":
        return sum(data)
    
    elif operation == "*":
        product = 1
        for d in data:
            product *= d
        
        return product
    
    return 0


def reformulate_row(row : list) -> list:
    """The row [123, 456, 789] needs to reformatted as [147, 258, 369] considering each 
        place in the numbers it's own row.

    Args:
        row (list): single row of data

    Returns:
        list: transformed data
    """

    # need one column to be made from the first index of each number, and so on. 
    # need the first bit, second bit, third bit, and so on from each number if it exists. 
    max_num_len = max([len(r) for r in row])
    result = []
    for i in range(max_num_len):
        new_num = ''
        for j in range(len(row)):
            if i < len(row[j]):
                new_num += row[j][i]
        result.append(new_num)
    return result



if __name__ == "__main__":
    # The data is stored in a really weird format
    with open("./puzzle_input.txt", "r") as f:
        lines = f.readlines()

    lines = [l.split(" ") for l in lines]

    data = []
    for l in range(len(lines)):
        # list of values
        data.append([])
        for i in range(len(lines[l])):
            if lines[l][i] != '':
                data[l].append(lines[l][i])

    data = rotate_matrix(data)

    total = 0
    for l in data:
        total += solve_problem([l[0]] + reformulate_row(l[1:]))
    
    print(total)