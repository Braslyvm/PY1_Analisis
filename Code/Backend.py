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


def save_matrix_to_json(matrix, filename):
    """
    Saves the matrix to a JSON file.
    
    Args:
        matrix (list): A 2D list representing the matrix to be saved.
        filename (str): The name of the file where the matrix will be saved.
    """
    with open(filename, "w") as file:
        json.dump(matrix, file)


def load_matrix_from_json(filename):
    """
    Loads a matrix from a JSON file.
    
    Args:
        filename (str): The name of the file to load the matrix from.
    
    Returns:
        tuple: A tuple containing the matrix, start position (2), and goal position (3),
               or None if there was an error loading the matrix.
    """
    if not os.path.exists(filename):
        return None
    
    with open(filename, "r") as file:
        matrix = json.load(file)
    
    start = None
    goal = None
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                start = (i, j)
            elif matrix[i][j] == 3:
                goal = (i, j)

    if start is None or goal is None:
        return None
    
    return matrix, start, goal


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


