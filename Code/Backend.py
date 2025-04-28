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




def load_matrix_from_json(matrix_name):
    """
    Loads a specific matrix from a JSON file based on the matrix name.
    
    Args:
        matrix_name (str): The name of the matrix to be loaded.
    Returns:
        list: The matrix corresponding to the provided matrix_name, or None if not found.
    """

    
    with open("store", "r") as file:
        matrices = json.load(file)
    
    # Search for the matrix by name
    for matrix_data in matrices:
        if matrix_data["nombre"] == matrix_name:
            return matrix_data["matriz"]
    return None


def delete_matrix_from_json(matrix_name):
    """
    Deletes a specific matrix from the JSON file based on the matrix name.
    
    Args:
        matrix_name (str): The name of the matrix to be deleted.
    Returns:
        bool: True if the matrix was found and deleted, False otherwise.
    """

    with open("store", "r") as file:
        matrices = json.load(file)
    
    initial_length = len(matrices)
    matrices = [matrix for matrix in matrices if matrix["nombre"] != matrix_name]
    
    if len(matrices) < initial_length:
        with open("store", "w") as file:
            json.dump(matrices, file)
        return True
    return False



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


def get_matrix_names_from_json():
    """
    Returns a list of matrix names from the given JSON file.
    
    Returns:
        list: A list of matrix names.
    """
    if not os.path.exists("store"):
        return []  # If the file doesn't exist, return an empty list
    
    with open("store", "r") as file:
        matrices = json.load(file)
    
    # Extract the names of the matrices and return them as a list
    matrix_names = [matrix_data["nombre"] for matrix_data in matrices]
    
    return matrix_names










def create_modified_matrix(matrix, start, goal):
    """
    Modifies the given matrix to generate additional paths (1's) between the start (2) and the goal (3).
    
    Args:
        matrix (list): The 2D list representing the maze.
        start (tuple): The coordinates of the start point (2).
        goal (tuple): The coordinates of the goal point (3).
    
    Returns:
        list: The modified matrix with additional paths or None if no new path is found.
    """
    # Directly modify the original matrix
    modifications = 0  # Counter for how many walls are modified

    # Randomly change some walls (0's) to paths (1's), but not touching the start (2) or goal (3)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0 and (i, j) != start and (i, j) != goal:
                if random.random() < 0.5:  # Modify 50% of the walls to paths
                    matrix[i][j] = 1
                    modifications += 1

    # If no modifications were made, return None
    if modifications == 0:
        return None
    
    # Check if the new matrix has a valid path between start and goal
    if is_connected(matrix, start, goal):
        return matrix
    else:
        return None



def find_path(matrix, start, goal):
    rows = len(matrix)
    cols = len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []

    def dfs(x, y):
        if x < 0 or y < 0 or x >= rows or y >= cols or matrix[x][y] == 0 or visited[x][y]:
            return False

        visited[x][y] = True
        path.append((x, y))

        if (x, y) == goal:
            return True

        for dx, dy in directions:
            if dfs(x + dx, y + dy):
                return True

        path.pop()  # If no path is found, backtrack
        return False

    if dfs(start[0], start[1]):
        return path
    else:
        return None


def get_all_paths(matrix):
    """
    Finds all paths from the start (2) to the goal (3) in the given matrix.
    Returns a list with all valid paths.

    Args:
        matrix (list): The 2D list representing the maze.

    Returns:
        list: A list containing all valid paths.
    """
    all_paths = []  # List to store valid paths

    # Find the positions of the start (2) and goal (3)
    start = None
    goal = None
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                start = (i, j)
            elif matrix[i][j] == 3:
                goal = (i, j)

    # Find the first path (shortest) using DFS or backtracking
    first_path = find_path(matrix, start, goal)
    if first_path:
        all_paths.append(first_path)  # Save the first path
    
    # Generate additional paths
    while len(all_paths) < 2:  # Change 3 to 2 to find 2 paths
        new_matrix = create_modified_matrix(matrix, start, goal)  # Modify the matrix
        if new_matrix:
            # Adjust the probability of generating 1's instead of 0's
            for i in range(len(new_matrix)):
                for j in range(len(new_matrix[0])):
                    if new_matrix[i][j] == 0 and random.random() < 0.2:  # 20% probability to change 0 to 1
                        new_matrix[i][j] = 1
            
            new_path = find_path(new_matrix, start, goal)
            if new_path:
                # Check if the new path is unique (not duplicated)
                if not any(len(path) == len(new_path) for path in all_paths):
                    all_paths.append(new_path)  # Save the new path
            else:
                break  # Exit if no valid path is found
        else:
            break  # Exit if the matrix cannot be modified to add a new path

    return all_paths


def create_two_more_paths(matrix):
    """
    Given a matrix with one valid path, generate two more paths and return the modified matrix.
    
    Args:
        matrix (list): The 2D list representing the maze with one valid path.

    Returns:
        list: The modified matrix with three valid paths.
    """
    # Find the positions of the start (2) and goal (3)
    start = None
    goal = None
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                start = (i, j)
            elif matrix[i][j] == 3:
                goal = (i, j)

    # List to store the found paths
    all_paths = []

    # Find the first path (shortest) using DFS or backtracking
    first_path = find_path(matrix, start, goal)
    if first_path:
        all_paths.append(first_path)  # Save the first path
    
    # Generate additional paths
    while len(all_paths) < 2:
        new_matrix = create_modified_matrix(matrix, start, goal)  # Modify the matrix
        if new_matrix:
            new_path = find_path(new_matrix, start, goal)
            if new_path:
                # Verify if the path is new (not duplicated)
                if not any(len(path) == len(new_path) for path in all_paths):
                    all_paths.append(new_path)  # Save the new path
            else:
                break  # Exit if no valid path is found
        else:
            break  # Exit if the matrix cannot be modified to add a new path

    # Return the modified matrix (with the two paths)
    if len(all_paths) == 2:  # Change 3 to 2
        return matrix
    else:
        return None  # If no two paths were found, return None


def create_matrix_with_two_paths(size):
    """
    Generates a matrix with at least 2 valid paths between the start (2) and the goal (3).
    
    Args:
        size (int): The size of the matrix (NxN).
    
    Returns:
        list: A 2D list representing the matrix with at least 2 valid paths.
    """
    while True:
        # Step 1: Create a valid matrix (it will have 1 valid path by default)
        matrix = create_valid_matrix(size)
        start = None
        goal = None
        
        # Step 2: Get the start and goal positions
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == 2:
                    start = (i, j)
                elif matrix[i][j] == 3:
                    goal = (i, j)
        
        # Step 3: Check if there are at least 2 valid paths
        all_paths = get_all_paths(matrix)
        if len(all_paths) >= 2:
            return matrix
        else:
            continue  # Regenerate matrix if not enough paths


