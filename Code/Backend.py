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
    """
    Creates a valid matrix with at least one path from start (2) to goal (3).
    
    This function generates random matrices until it finds one where a valid 
    path exists between the start and the goal using the `is_connected` function.
    
    Args:
        size (int): The size of the matrix (NxN).
    
    Returns:
        list: A 2D list representing the valid matrix.
    """
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

def find_path_movements(matrix, start, goal):
    """
    This function finds the path movements in a matrix using depth-first search (DFS).
    It returns a list of movements as coordinates stored in lists (instead of tuples).
    
    Args:
        matrix (list of lists): The grid where the pathfinding occurs.
        start (list): Starting coordinates [x, y].
        goal (list): Goal coordinates [x, y].

    Returns:
        list: A list of movements, each represented as a list [x, y] of visited coordinates.
    """
    rows = len(matrix)  # Get the number of rows in the matrix
    cols = len(matrix[0])  # Get the number of columns in the matrix
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions for Up, Down, Left, Right
    visited = [[False for _ in range(cols)] for _ in range(rows)]  # Matrix to track visited cells
    path = []  # Stores the path of coordinates from start to goal
    movements = []  # Stores all visited coordinates during DFS

    def dfs(x, y):
        """
        Performs depth-first search recursively to find the path.
        
        Args:
            x (int): Current row position.
            y (int): Current column position.

        Returns:
            bool: True if the goal is reached, False otherwise.
        """
        # Check if the current position is valid
        if x < 0 or y < 0 or x >= rows or y >= cols or matrix[x][y] == 0 or visited[x][y]:
            return False

        if matrix[x][y] != 0:
            movements.append([x, y])  # Append the coordinates as a list instead of a tuple
        
        visited[x][y] = True  # Mark the current position as visited
        path.append([x, y])  # Add the current coordinates to the path

        # If the goal is reached, return True
        if [x, y] == goal:
            return True

        # Explore the neighboring cells in all directions
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            # Only continue if the new coordinates are within bounds
            if 0 <= new_x < rows and 0 <= new_y < cols:
                if dfs(new_x, new_y):  # If a path is found, continue recursion
                    return True

        path.pop()  # If no path is found, backtrack by removing the last position
        return False

    # Start DFS from the initial start position
    dfs(start[0], start[1])

    return movements  # Return the list of movements (visited coordinates) during DFS
    

def get_all_pathsA(matrix,start,goal):
    """
    Finds all paths from the start (2) to the goal (3) in the given matrix using DFS (Depth-First Search).
    
    This function recursively explores all possible paths in the matrix and stores all valid paths from the 
    start to the goal in the `all_paths` list. It uses a depth-first search approach and backtracking to find 
    all possible routes.
    
    Args:
        matrix (list): A 2D list representing the maze (NxN matrix).
        start (tuple): The coordinates of the start point (2).
        goal (tuple): The coordinates of the goal point (3).
    
    Returns:
        list: A list containing all valid paths from the start to the goal. 
              Each path is a list of tuples representing the coordinates.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []
    movements = []
    all_paths = []

    def dfs(x, y, path):
        """
        Recursive depth-first search to explore the matrix and find paths.
        
        Args:
            x (int): Current row position.
            y (int): Current column position.
            path (list): The current path being explored.
        """
        path.append((x, y))#Add current position to the path
        
        if x < 0 or y < 0 or x >= rows or y >= cols or matrix[x][y] == 0 or visited[x][y]:
            path.pop()
            return

        if (x, y) == goal:
            all_paths.append(path.copy())
            path.pop()
            return

        visited[x][y] = True #Mark current cell as visit

        for dx, dy in directions:
            dfs(x + dx, y + dy, path)

        visited[x][y] = False #Unmark cell for other paths (backtrack)
        path.pop()  # If no path is found, backtrack
        

    dfs(start[0], start[1], [])
    return all_paths
    



def find_path(matrix, start, goal):
    """
    Finds a path from the start (2) to the goal (3) in the matrix using DFS (Depth-First Search).
    
    This function explores the matrix recursively to find a valid path between the start and goal, 
    marking cells as visited to avoid revisiting them. If a valid path is found, it returns the list 
    of coordinates that form the path, otherwise, it returns `None`.
    
    Args:
        matrix (list): A 2D list representing the maze (NxN matrix).
        start (tuple): The coordinates of the start point (2).
        goal (tuple): The coordinates of the goal point (3).
    
    Returns:
        list: A list of coordinates representing the path from the start to the goal, 
              or `None` if no path is found.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []

    def dfs(x, y):
        """
        Recursive depth-first search to explore the matrix and find a path.
        
        Args:
            x (int): Current row position.
            y (int): Current column position.
        
        Returns:
            bool: `True` if a path is found, `False` otherwise.
        """
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

def remove_start(matrix):
    """
    Removes the start point (2) from the matrix and replaces it with a path (1).
    
    Args:
        matrix (list): The 2D list representing the maze.
    
    Returns:
        list: The modified matrix with the start (2) replaced by 1.
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                matrix[i][j] = 1  # Replace start point with a path
                return matrix
    return matrix  # Return the matrix unchanged if start point is not found


def get_start_and_goal(matrix):
    """
    Returns the coordinates of the start (2) and goal (3) in the matrix.
    
    Args:
        matrix (list): The 2D list representing the maze.
    
    Returns:
        tuple: A tuple containing two tuples. The first is the start coordinates (2), 
               and the second is the goal coordinates (3).
    """
    start = None
    goal = None
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                start = (i, j)  # Store the start coordinates
            elif matrix[i][j] == 3:
                goal = (i, j)  # Store the goal coordinates
    
    return start, goal  # Return both start and goal coordinates as a tuple

def quicksort(arr):
    """
    Mediator funtion to past a static value to frontend.
    
    Args:
        arr (list): List of lists to sort.
        
    Returns:
        list: Sorted list in ascending order by the length of the inner lists.
    """
    worstAndBestPaths = Quicksort(arr)
    return worstAndBestPaths 

def Quicksort(arr):
    """
    Sorts a list of lists based on the number of elements inside each list, from least to most.
    
    Args:
        arr (list): List of lists to sort.
        
    Returns:
        list: Sorted list in ascending order by the length of the inner lists.
    """
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2] 
        left = [x for x in arr if len(x) < len(pivot)]  
        middle = [x for x in arr if len(x) == len(pivot)] 
        right = [x for x in arr if len(x) > len(pivot)] 
        return Quicksort(left) + middle + Quicksort(right)

