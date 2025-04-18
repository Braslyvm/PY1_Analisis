import random
import json

# Function to display the size options and get the user's choice
def get_matrix_size():
    """
    Displays the available matrix sizes and prompts the user to choose one.
    The user is asked to input a number between 1 and 5 corresponding to a matrix size.
    Based on the choice, the corresponding matrix size is returned.

    Returns:
        int: The chosen matrix size in the format (NxN).
    """
    print("Please choose the size of the matrix:")
    print("1. 5x5")
    print("2. 10x10")
    print("3. 15x15")
    print("4. 20x20")
    print("5. 25x25")

    choice = int(input("Enter a number between 1 and 5: "))

    while choice < 1 or choice > 5:
        print("Invalid choice! Please enter a number between 1 and 5.")
        choice = int(input("Enter a number between 1 and 5: "))

    matrix_sizes = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25}
    return matrix_sizes[choice]

# Function to create a random matrix with 0s and 1s
def create_random_matrix(size):
    """
    Creates a matrix of the given size with random 0s and 1s.
    The matrix will have the dimensions size x size.

    Args:
        size (int): The size of the matrix (NxN).

    Returns:
        list: A 2D list representing the matrix filled with random 0s and 1s.
    """
    matrix = []
    for _ in range(size):
        row = [random.choice([0, 1]) for _ in range(size)]
        matrix.append(row)
    
    return matrix

# Function to print the matrix in a readable format
def print_matrix(matrix):
    """
    Prints the matrix in a human-readable format.

    Args:
        matrix (list): The 2D list representing the matrix.
    """
    for row in matrix:
        print(" ".join(map(str, row)))

# Function to save the matrix to a JSON file
def save_matrix_to_json(matrix, filename="matrix.json"):
    """
    Saves the matrix to a JSON file.

    Args:
        matrix (list): The 2D list representing the matrix.
        filename (str): The name of the file where the matrix will be saved.
    """
    filename = input("Please enter the filename to save the matrix (matrix.json): ")
    with open(filename, "w") as file:
        json.dump(matrix, file)
    print(f"Matrix saved to {filename}")

# Main program
selected_size = get_matrix_size()
print(f"You have selected a {selected_size}x{selected_size} matrix.")

# Generate and print the random matrix
random_matrix = create_random_matrix(selected_size)
print("Here is your random matrix:")
print_matrix(random_matrix)

# Save the matrix to a JSON file
save_matrix_to_json(random_matrix)
