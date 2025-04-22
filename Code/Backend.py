import random
import json
import os






# Function to display the size options and get the user's choice
def get_matrix_size():
    """
    Displays the available matrix sizes and prompts the user to choose one
    Returns the chosen size
    
    This function shows a list of possible matrix sizes and asks the user
    to select one. The user inputs a number, and the corresponding matrix size
    (in NxN format) is returned. If the user enters an invalid choice, it
    repeatedly asks for a valid input until a valid choice is made
    
    Returns:
        int: The chosen matrix size (example, 5 for a 5x5 matrix).
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


# Function to create a random matrix with 0s and 1s, and place 2 and 3 at random positions
def create_random_matrix(size):
    """
    Creates a random NxN matrix filled with 0s and 1s. It places the start (2) 
    and goal (3) at random positions within the matrix
    
    This function creates a matrix of a specified size (NxN), where the cells
    are randomly filled with 0s (representing walls) and 1s (representing paths)
    Then, it places the start point (2) and the goal (3) at random, ensuring they 
    do not overlap. The resulting matrix is returned
    
    Args:
        size (int): The size of the matrix (NxN)

    Returns:
        list: A 2D list representing the generated matrix with start and goal
    """
    matrix = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    
    pos_2 = (random.randint(0, size - 1), random.randint(0, size - 1))
    pos_3 = (random.randint(0, size - 1), random.randint(0, size - 1))

    while pos_2 == pos_3:
        pos_3 = (random.randint(0, size - 1), random.randint(0, size - 1))

    matrix[pos_2[0]][pos_2[1]] = 2
    matrix[pos_3[0]][pos_3[1]] = 3
    
    return matrix

# Function to print the matrix in a readable format
def print_matrix(matrix):
    """
    Prints the matrix in a readable format, with space-separated values for each row
    
    This function takes a 2D list (matrix) and prints each row on a new line. Each
    value in the row is separated by a space for better readability, making it easy to
    visually inspect the structure of the matrix
    
    Args:
        matrix (list): A 2D list representing the matrix to be printed
    """
    for row in matrix:
        print(" ".join(map(str, row)))

# Function to save the matrix to a JSON file
def save_matrix_to_json(matrix):
    """
    Saves the matrix to a JSON file specified by the user
    
    This function prompts the user for a filename, then serializes the matrix into
    JSON format and writes it to the specified file. The matrix can later be loaded
    back into the program for further use
    
    Args:
        matrix (list): A 2D list representing the matrix to be saved
    """
    filename = input("Please enter the filename to save the matrix (example, matrix.json): ")
    with open(filename, "w") as file:
        json.dump(matrix, file)
    print(f"Matrix saved to {filename}")

# Function to load a matrix from a JSON file
def load_matrix_from_json():
    """
    Loads a matrix from a JSON file provided by the user
    
    This function prompts the user for a filename and attempts to load the matrix
    stored in JSON format from the specified file. If the file does not exist or
    the matrix cannot be loaded, an error message is displayed
    
    Returns:
        tuple: A tuple containing the matrix, start position (2), and goal position (3),
               or None if there was an error loading the matrix
    """
    filename = input("Please enter the filename to load the matrix from (example, matrix.json): ")

    if not os.path.exists(filename):
        print("File does not exist!")
        return None
    
    with open(filename, "r") as file:
        matrix = json.load(file)
    
    print(f"Matrix loaded from {filename}")
    
    # Check for the presence of start (2) and goal (3)
    start = None
    goal = None
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                start = (i, j)
            elif matrix[i][j] == 3:
                goal = (i, j)

    if start is None or goal is None:
        print("Error: The matrix does not contain valid start (2) and/or goal (3) positions!")
        return None  # If no valid start and goal are found, return None
    
    # Return both the matrix and the positions of start and goal
    return matrix, start, goal

# Function to verify if start (2) and goal (3) are connected in the maze
def is_connected(maze, start, goal):
    """
    Verifies if there is a valid path between the start (2) and goal (3) in the matrix using DFS
    
    This function uses a depth first search (DFS) algorithm to explore all possible paths
    from the start point (2) to the goal point (3). If a path is found, it returns True;
    otherwise, it returns False.
    
    Args:
        maze (list): A 2D list representing the maze
        start (tuple): The coordinates of the start point (2)
        goal (tuple): The coordinates of the goal point (3)
    
    Returns:
        bool: True if a valid path exists, False otherwise
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

# Function to create a valid matrix (ensure start and goal are connected)
def create_valid_matrix(size):
    """
    Keeps creating random matrices until one is valid (i.e., start and goal are connected)
    
    This function repeatedly generates random matrices and checks if they are valid,
    meaning that there is a connected path from the start (2) to the goal (3). It
    returns a valid matrix when one is found
    
    Args:
        size (int): The size of the matrix (NxN)
    
    Returns:
        list: A valid matrix with start and goal connected
    """
    while True:
        matrix = create_random_matrix(size)
        # Get start (2) and goal (3) positions
        start = None
        goal = None
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == 2:
                    start = (i, j)
                elif matrix[i][j] == 3:
                    goal = (i, j)
        
        # Check if start and goal are connected
        if is_connected(matrix, start, goal):
            print("A valid matrix has been created!")
            return matrix
        else:
            print("Matrix is not valid, creating a new one...")

# Function to solve the maze using backtracking and mark the path with 4
def solve_maze(maze, start, goal):
    """
    Solves the maze using the backtracking algorithm and marks the path with 4
    
    This function uses a recursive depth-first search (DFS) approach to explore all
    possible paths in the maze from the start point (2) to the goal point (3). If a
    path is found, it marks the path with 4. It ensures that the start and goal positions
    are not overwritten
    
    Args:
        maze (list): A 2D list representing the maze
        start (tuple): The coordinates of the start point (2)
        goal (tuple): The coordinates of the goal point (3)
    
    Returns:
        list: The path found by the backtracking algorithm
    """
    rows = len(maze)
    cols = len(maze[0])
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    def backtrack(x, y, path):
        if x < 0 or y < 0 or x >= rows or y >= cols or maze[x][y] == 0 or visited[x][y]:
            return False
        
        visited[x][y] = True
        path.append((x, y))
        
        if (x, y) == goal:
            return True
        
        for dx, dy in directions:
            if backtrack(x + dx, y + dy, path):
                return True
        
        path.pop()
        return False
    
    path = []
    
    if backtrack(start[0], start[1], path):
        # Mark the path with 4, but skip the start (2) and goal (3) cells
        for x, y in path:
            if maze[x][y] != 2 and maze[x][y] != 3:  # Avoid overwriting start and goal
                maze[x][y] = 4
        return path
    else:
        return None

# Main function to run the game
def run_game():
    """
    Runs the game, allowing the user to create a new maze or load an existing one, 
    check connectivity, solve the maze, and display the result
    
    This function displays the menu and handles the user's input for creating or loading
    a maze, solving the maze, and printing the result. It ensures the game runs smoothly
    by coordinating the matrix creation, solving, and displaying the final result
    """
    print("Welcome to the Matrix Program!")
    print("1. New Game (Create a new matrix)")
    print("2. Load Game (Load an existing matrix from a file)")
    print("3. Exit")
    
    choice = int(input("Please select an option (1-3): "))
    
    while choice < 1 or choice > 3:
        print("Invalid choice! Please select a number between 1 and 3.")
        choice = int(input("Please select an option (1-3): "))
    
    if choice == 1:
        selected_size = get_matrix_size()
        print(f"You have selected a {selected_size}x{selected_size} matrix.")
        # Create a valid matrix (that has a connected start and goal)
        valid_matrix = create_valid_matrix(selected_size)
        print("Here is your valid matrix:")
        print_matrix(valid_matrix)
        
        # Solve the maze and mark the path with 4
        start = None
        goal = None
        for i in range(selected_size):
            for j in range(selected_size):
                if valid_matrix[i][j] == 2:
                    start = (i, j)
                elif valid_matrix[i][j] == 3:
                    goal = (i, j)
        
        solve_maze(valid_matrix, start, goal)  # Solve and mark the path
        print_matrix(valid_matrix)  # Print the matrix with the path marked as 4
        
        save_matrix_to_json(valid_matrix)
    
    elif choice == 2:
        loaded_data = load_matrix_from_json()
        if loaded_data:
            loaded_matrix, start, goal = loaded_data
            print("Here is the loaded matrix:")
            print_matrix(loaded_matrix)
            
            if is_connected(loaded_matrix, start, goal):
                print("The start and goal are connected!")
                solve_maze(loaded_matrix, start, goal)  # Solve and mark the path
                print("\nPath found in the matrix:")
                print_matrix(loaded_matrix)
            else:
                print("The start and goal are NOT connected.")
    
    else:
        print("Exiting the program...")

# Run the game
run_game()



