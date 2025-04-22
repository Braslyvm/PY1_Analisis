import random
import json
import os

# Function to display the size options and get the user's choice
def get_matrix_size(choice):
    """
    Returns the matrix size based on the user's choice.
    
    Args:
        choice (int): The user's choice for matrix size (1-5).
    
    Returns:
        int: The chosen matrix size (e.g., 5 for a 5x5 matrix).
    """
    matrix_sizes = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25}
    
    if choice < 1 or choice > 5:
        return None  # Invalid choice
    
    return matrix_sizes[choice]


def create_random_matrix(size):
    """
    Creates a random matrix with 0s and 1s, and places 2 (start) and 3 (goal) at random positions.
    
    Args:
        size (int): The size of the matrix (NxN).
    
    Returns:
        list: A 2D list representing the generated matrix with start and goal.
    """
    matrix = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    
    pos_2 = (random.randint(0, size - 1), random.randint(0, size - 1))
    pos_3 = (random.randint(0, size - 1), random.randint(0, size - 1))

    while pos_2 == pos_3:
        pos_3 = (random.randint(0, size - 1), random.randint(0, size - 1))

    matrix[pos_2[0]][pos_2[1]] = 2
    matrix[pos_3[0]][pos_3[1]] = 3
    
    return matrix


def matrix_to_string(matrix):
    """
    Converts the matrix to a string format, so it can be displayed in the GUI.
    
    Args:
        matrix (list): A 2D list representing the matrix.
    
    Returns:
        str: The string representation of the matrix.
    """
    matrix_string = ""
    for row in matrix:
        matrix_string += " ".join(map(str, row)) + "\n"
    return matrix_string


def save_matrix_to_json(matrix,matrix_name):
    """
    Saves the matrix to a JSON file with the given name, in the specified file.
    
    Args:
        matrix (list): The 2D list representing the matrix to be saved.
        filename (str): The name of the file where the matrices will be saved.
        matrix_name (str): The name of the matrix.
    """
    # Check if the file exists and if it is empty
    if os.path.exists("store") and os.stat("store").st_size > 0:
        with open("store", "r") as file:
            matrices = json.load(file)
    else:
        matrices = []  # Initialize an empty list if the file doesn't exist or is empty

    # Create a dictionary for the new matrix
    matrix_data = {
        "nombre": matrix_name,
        "matriz": matrix
    }

    # Append the new matrix to the list
    matrices.append(matrix_data)

    # Save the updated list of matrices back to the file
    with open("store", "w") as file:
        json.dump(matrices, file, indent=4)

    
    return None




def load_matrix_from_json(filename, matrix_name):
    """
    Loads a specific matrix from a JSON file based on the matrix name.
    
    Args:
        filename (str): The name of the file to load the matrix from.
        matrix_name (str): The name of the matrix to be loaded.
    
    Returns:
        list: The matrix corresponding to the provided matrix_name, or None if not found.
    """
    if not os.path.exists(filename):
        print(f"Error: The file {filename} does not exist!")
        return None
    
    with open(filename, "r") as file:
        matrices = json.load(file)
    
    # Search for the matrix by name
    for matrix_data in matrices:
        if matrix_data["nombre"] == matrix_name:
            print(f"Matrix '{matrix_name}' loaded successfully.")
            return matrix_data["matriz"]
    
    print(f"Error: No matrix found with name '{matrix_name}'.")
    return None



def is_connected(maze, start, goal):
    """
    Verifies if there is a valid path between the start (2) and goal (3) in the matrix using DFS.
    
    Args:
        maze (list): A 2D list representing the maze.
        start (tuple): The coordinates of the start point (2).
        goal (tuple): The coordinates of the goal point (3).
    
    Returns:
        bool: True if a valid path exists, False otherwise.
    """
    rows = len(maze)
    cols = len(maze[0])
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    def dfs(x, y):
        if x < 0 or y < 0 or x >= rows or y >= cols or maze[x][y] == 0 or visited[x][y]:
            return False
        
        visited[x][y] = True
        
        if (x, y) == goal:
            return True
        
        for dx, dy in directions:
            if dfs(x + dx, y + dy):
                return True
        
        return False
    
    return dfs(start[0], start[1])


def create_valid_matrix(size):
    while True:
        matrix = create_random_matrix(size)
        start = None
        goal = None
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == 2:
                    start = (i, j)
                elif matrix[i][j] == 3:
                    goal = (i, j)
        
        if is_connected(matrix, start, goal):
            return matrix


def get_matrix_names_from_json(filename):
    """
    Returns a list of matrix names from the given JSON file.
    
    Args:
        filename (str): The name of the JSON file to read the matrices from.
    
    Returns:
        list: A list of matrix names.
    """
    if not os.path.exists(filename):
        return []  # If the file doesn't exist, return an empty list
    
    with open(filename, "r") as file:
        matrices = json.load(file)
    
    # Extract the names of the matrices and return them as a list
    matrix_names = [matrix_data["nombre"] for matrix_data in matrices]
    
    return matrix_names
