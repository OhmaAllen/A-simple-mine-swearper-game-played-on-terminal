"""Programming Assignment #2 - Functions"""
# you may use random and re.
import random
import re


###################################################################################################

"""
My algorithm is to use o, M represent safe cell and mines respectively. But I will use @o and @M in the true board to represent
marked safe cell or marked mines. but when display the board to the player, o or M will not be shown to them. The marked cell or mines
will also only show @.
"""
def initalize_board_random(board_height: int, board_width: int, mine_count: int, seed: int = 20) -> list[list]:
    """
    Generates a new board with height rows and width columns, and randomly places 
    mine_count mines on it.
    - Returns a 2D list with all cells initialized to 'o' (unvisited).
    
    Parameters:
    - board_height: int, the number of rows in the board (4 <= board_height <= 50)
    - board_width: int, the number of columns in the board (4 <= board_width <= 26)
    - mine_count: int, the number of mines to place on the board (5 <= mine_count < total cells)
    - seed: int, optional seed for random generator for reproducibility
    
    Raises:
    - TypeError: If any of the inputs are not integers.
    - ValueError: If any input values are outside of valid ranges.
    
    Returns:
    - A 2D list representing the initialized board, where 'M' represents mines and 'o' represents unvisited cells.
    """

    #make sure the inputs are integers
    if not isinstance(board_height, int):
        raise ValueError("Board height must be an integer.")
    if not isinstance(board_width, int):
        raise ValueError("Board width must be an integer.")
    if not isinstance(mine_count, int):
        raise ValueError("Mine count must be an integer.")
    if not isinstance(seed, int):
        raise ValueError("Seed must be an integer.")

    #validate the board dimensions and mine count
    if board_height < 4 or board_height > 50:
        raise ValueError("Board height must be between 4 and 50.")
    if board_width < 4 or board_width > 26:
        raise ValueError("Board width must be between 4 and 26.")
    if mine_count < 5 or mine_count >= board_height * board_width:
        raise ValueError("The mine count must be at least 5 and less than the total number of cells.")

    random.seed(seed)

    #initialize the board with 'o' representing unvisited, unmarked, no mines cells
    board = [['o' for i in range(board_width)] for j in range(board_height)]

    #place mines
    mine_positions = set() #universal set to get rid of duplicated ones
    while len(mine_positions) < mine_count:
        row = random.randint(0, board_height - 1)
        col = random.randint(0, board_width - 1)
        mine_positions.add((row, col))
    
    #store mine information with "M" to represent unvisited, unmarked mines
    for row, col in mine_positions:
        board[row][col] = 'M'

    return board



###################################################################################################
def initalize_board_file(board_height: int, board_width: int, filename: str) -> list[list]:
    """
    Generates a new board with height rows and width columns, and places the mines from the 
    coordinates listed in the file. The board characteristics are the same as in `initialize_board_random`.
    
    Parameters:
    - board_height: number of rows (1 to N).
    - board_width: number of columns (A to Z).
    - filename: utf-8 encoded text file with one mine coordinate per line in the format (row,col). 
    
    Returns:
    - A zero-indexed 2D list representing the board, where 'M' represents a mine, and 'o' represents 
      an unvisited, unmarked cell.
    
    Raises:
    - ValueError: For invalid board dimensions or improper formatting.
    - FileNotFoundError: If the provided file does not exist.
    """
    if not isinstance(board_height, int):
        raise ValueError("Board height must be an integer.")
    if not isinstance(board_width, int):
        raise ValueError("Board width must be an integer.")
    if not isinstance(filename, str):
        raise ValueError("Mine count must be an integer.")
    if board_height < 4 or board_height > 50:
        raise ValueError("Board height must be between 4 and 50.")
    if board_width < 4 or board_width > 26:
        raise ValueError("Board width must be between 4 and 26.")

    #create a board initialized with 'o' for unvisited, unmarked cells
    board = [['o' for _ in range(board_width)] for _ in range(board_height)]

    #generate the allowed columns (A-Z) based on board width
    allowed_columns = [chr(65 + i) for i in range(board_width)] 

    #define a pattern to match valid coordinates (e.g., (1, A))
    pattern = re.compile(r'\(\s*(\d+)\s*,\s*([A-Za-z])\s*\)')

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                #ignore lines starting with '#' or empty lines
                if not line or line.startswith('#'):
                    continue

                #match the line against the pattern for coordinates
                match = pattern.search(line)
                if match:
                    row_str, col_str = match.groups()

                    try:
                        #cnvert row string to integer and column string to uppercase letter
                        row = int(row_str)
                        col = col_str.upper()

                        #validate row and column range
                        if row < 1 or row > board_height:
                            raise ValueError(f"Row {row} is out of range. It must be between 1 and {board_height}.")
                        if col not in allowed_columns:
                            raise ValueError(f"Column {col} is invalid. It must be between A and {allowed_columns[-1]}.")

                        #convert to zero-indexed format
                        row_idx = row - 1
                        col_idx = allowed_columns.index(col)

                        #place a mine at the valid coordinate
                        board[row_idx][col_idx] = 'M'

                    except ValueError as ve:
                        raise ValueError(f"Invalid coordinate format in line: '{line}'. Error: {ve}")

                else:
                    #if no valid match, raise a value error for improper format
                    raise ValueError(f"Invalid coordinate format: '{line}'. Expected format is (row, column).")

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{filename}' not found.")

    return board

###################################################################################################
def validate_board_dimensions(board: list[list]) -> bool:
    """Validates the board to ensure it is a 2D list with valid dimensions."""

    if not isinstance(board, list):
        raise ValueError("Board should be a list.")
    if any(not isinstance(row, list) for row in board):
        raise ValueError("Board must be a two-dimensional list (list of lists).")
    if len(board) == 0:
        raise ValueError("Board should have at least one row.")
    for row in board:
        if not isinstance(row, list):
            raise ValueError("Board should be a 2D list.")
    row_length = len(board[0])
    if row_length == 0:
        raise ValueError("Board should have at least one column.")
    for row in board:
        if len(row) != row_length:
            raise ValueError("Each row should have the same number of columns.")
    
    #assert that the board size is within allowed limits
    if not (4 <= len(board) <= 50):
        raise ValueError("Board must have between 4 and 50 rows.")
    if not (4 <= row_length <= 26):
        raise ValueError("Board must have between 4 and 26 columns.")

    return True



###################################################################################################
def display_board(board: list[list]) -> str:
    ''' 
    Returns a string to print the board as the player would see it, using the following format:
        |---| A | B | C | D |...
        |001| o | 1 | o |   |...
        |002| o | @ | o | o |...
        |003| o | o | 2 | o |...
        ...
    - A number (1-8) means the number of mines in the neighbors (visited).
    - A space (' ') means no mines surround the cell (visited).
    - A 'o' (lowercase letter 'o') means that the cell is unvisited and not marked.
    - A '@' means that the user marked that cell as a possible bomb.
    
    Returns:
        - The string with the player-visible representation described.
    '''
    #first, ensure the board is a valid 2D list
    if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
        raise ValueError("Invalid board format, must be a 2D list.")

    rows = len(board)
    if rows == 0:
        raise ValueError("Board should have at least one row.")
    
    cols = len(board[0]) if rows > 0 else 0
    if cols == 0:
        raise ValueError("Board should have at least one column.")
    
    #validate that all rows have the same number of columns
    for row in board:
        if len(row) != cols:
            raise ValueError("Each row must have the same number of columns.")
    
    #headers
    header = "|---| " + " | ".join(chr(65 + i) for i in range(cols)) + " |"
    board_rep = [header]

    #iterate through the rows to build the board
    for i in range(rows):
        row_label = f"|{i+1:03d}|"
        row_values = []

        for cell in board[i]:
            if isinstance(cell, str):
                if cell == 'o' or cell == 'M':  #unvisited cell or mine (hidden from user)
                    row_values.append('o')
                elif cell == '@o' or cell == '@M':  #marked cell, either safe or mine
                    row_values.append('@')
                elif cell == ' ':  #visited cell with no surrounding mines will be represented by ' '
                    row_values.append(' ')
                else:
                    row_values.append(str(cell))  # Fallback for unexpected string values
            elif isinstance(cell, int):  #visited cell with surrounding mines
                row_values.append(str(cell))
            else:
                raise ValueError(f"Unexpected cell type: {type(cell)} at row {i+1}, col {chr(65 + board[i].index(cell))}")

        #add the row to the board representation
        board_rep.append(f"{row_label} {' | '.join(row_values)} |")

    return "\n".join(board_rep)+"\n"




def display_true_board(board: list[list]) -> str:
    '''- Returns a string to print the board using the following format. 
    ###################!!!!this function dis play the real inside of the board(only when game over)##################
        |---| A | B | C | D |...
        |001| o | 1 | o |   |...
        |002| o | @ | o | o |...
        |003| o | o | 2 | o |...
        ...
        - A number (1-8) means number of mines in the neighbors. The user visited that cell.
        - A space means that in the neighbors there are NO mines. The user visited that cell.
        - A o (lowercase letter o) means that the cell was NOT visited and not marked.
        - A @ means that the user marked that place as a possible bomb.
    - Return:
        - the string with the representation described.
    '''
    #check if it is a 2-D list
    if not isinstance(board, list):
        raise ValueError("Board should be a list.")
    if any(not isinstance(row, list) for row in board):
        raise ValueError("Board must be a two-dimensional list (list of lists).")
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    #same header
    header = "|---| " + " | ".join(chr(65 + i) for i in range(cols)) + " |"
    board_rep = [header] 

    for i in range(rows):
        row_label = f"|{i+1:03d}|"
        row_values = " | ".join(str(cell) for cell in board[i])
        board_rep.append(f"{row_label} {row_values} |")
    
    return "\n".join(board_rep)


###################################################################################################
def visit(board: list[list], row: int, col: str) -> None:
    """
    Allows the user to visit a cell on the board.
    Raises appropriate errors if the action is invalid.
    
    Parameters:
    - board: 2D list representing the Minesweeper board.
    - row: integer representing the row number (1-based index).
    - col: character ('A'-'Z') representing the column letter.
    
    Raises:
    - ValueError: If the cell is already visited or if the row/column is invalid.
    - RuntimeError: If the cell contains a mine.
    - TypeError: If the row or col inputs are not of the expected types.
    """

    if not isinstance(board, list):
        raise ValueError("Board should be a list.")
    if any(not isinstance(row, list) for row in board):
        raise ValueError("Board must be a two-dimensional list (list of lists).")
    
    #type checking for the row and col inputs
    if not isinstance(row, int):
        raise ValueError("Row must be an integer.")
    if not isinstance(col, str) or len(col) != 1 or not col.isalpha():
        raise ValueError("Column must be a single letter (A-Z).")
    
    #convert the column letter to a zero-based index (A -> 0, B -> 1, etc.)
    col_index = ord(col.upper()) - ord('A')

    #convert the row number to zero-based index
    row_index = row - 1

    #ensure the provided row and column are valid
    if not (0 <= row_index < len(board)) or not (0 <= col_index < len(board[0])):
        raise ValueError("Invalid row or column.")
    
    cell_value = board[row_index][col_index]

    #make sure the cell hasn't already been visited (visited cells are numbers or spaces)
    if isinstance(cell_value, int) or cell_value == ' ':
        raise ValueError("This cell was already visited.")

    #if the cell contains a mine, raise an error
    if cell_value in ['M', '@M']:
        raise RuntimeError("BOOM! GAME OVER!")

    #if the cell is safe (assumed to be 'o' or '@o'), mark it as visited
    if cell_value in ['o', '@o']:
        #count the number of surrounding mines
        surrounding_mines = count_surrounding_mines(board, row_index, col_index)
        
        #if no surrounding mines, mark the cell as visited with an empty space (' ')
        if surrounding_mines == 0:
            board[row_index][col_index] = ' '
        else:
            #mark the cell as visited with the number of surrounding mines
            board[row_index][col_index] = surrounding_mines




###################################################################################################
def change_mark(board: list[list], row: int, col: str) -> None:
    """
    Allows the user to mark/unmark a cell as a possible mine.
    - If the cell is already marked ('@'), unmark it.
    - If the cell is unmarked and unvisited, mark it as a possible mine.
    - If the cell was already visited, raise a ValueError.
    
    Parameters:
        - board: 2D list representing the Minesweeper board.
        - row: integer representing the row number (1-based index).
        - col: character ('A'-'Z') representing the column letter.
    
    Raises:
        - TypeError: If the row is not an integer or the column is not a valid letter.
        - ValueError: If the cell is already visited or if the row/column is invalid.
    """

    if not isinstance(board, list):
        raise ValueError("Board should be a list.")
    if any(not isinstance(row, list) for row in board):
        raise ValueError("Board must be a two-dimensional list (list of lists).")
    #type checking for the row and col inputs
    if not isinstance(row, int):
        raise ValueError("Row must be an integer.")
    if not isinstance(col, str) or len(col) != 1 or not col.isalpha():
        raise ValueError("Column must be a single letter (A-Z).")

    #convert the column letter to a zero-based index (A -> 0, B -> 1, etc.)
    col_index = ord(col.upper()) - ord('A')

    #convert the row number to zero-based index
    row_index = row - 1

    #check if the provided row and column are valid
    if not (0 <= row_index < len(board)) or not (0 <= col_index < len(board[0])):
        raise ValueError("Invalid row or column.")
    
    #get the current value of the cell
    cell_value = board[row_index][col_index]

    #check if the cell has already been visited (visited cells are numbers or spaces)
    if isinstance(cell_value, int) or cell_value == ' ':
        raise ValueError("Cannot mark a visited cell.")

    #toggle the mark status of the cell
    if cell_value == 'o': 
        board[row_index][col_index] = '@o'
    elif cell_value == 'M': 
        board[row_index][col_index] = '@M'
    elif cell_value == '@o': 
        board[row_index][col_index] = 'o'
    elif cell_value == '@M':
        board[row_index][col_index] = 'M'




###################################################################################################
def validate_game(board: list[list]) -> str:
    """
    Validates the current state of the Minesweeper board.
    Returns "YOU WIN!!!" if the user won, raises errors if not.
    """
    if not isinstance(board, list):
        raise ValueError("Board should be a list.")
    if any(not isinstance(row, list) for row in board):
        raise ValueError("Board must be a two-dimensional list (list of lists).")
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    for i in range(rows):
        for j in range(cols):
            cell_value = board[i][j]

            #ensure no unmarked mines are left
            if cell_value == 'M':
                raise RuntimeError(f"USER LOST-There is an unmarked mine at {i+1},{chr(j + ord('A'))}.")

            #ensure no unvisited, unmarked cells are left
            if cell_value == 'o':  # Unvisited and unmarked cell
                raise RuntimeError("User Defeated")

            #ensure no invalid markings
            if cell_value == '@o':  # Marked but not a mine
                raise RuntimeError(f"USER LOST-Not a mine at {i+1},{chr(j + ord('A'))}.")

            #ensure all visited cells are correctly marked (either int or space)
            if not (isinstance(cell_value, int) or cell_value == ' ' or cell_value == '@M'):
                raise RuntimeError(f"Invalid cell state at {i+1},{chr(j + ord('A'))}: {cell_value}")

    return "YOU WIN!!!"













###################################################################################################
def actions_from_file(board: list[list], filename: str) -> None:
    """
    Reads actions from a file (UTF-8 encoded) and applies them to the board.
    - Each action is represented by 2 lines:
      - First line: 'M' for mark or 'V' for visit.
      - Second line: The coordinate in the format (row, column) e.g., (1,A).
    - If the action is not 'M' or 'V', raise a RuntimeError.
    - If the file format is incorrect, raise a RuntimeError.

    Parameters:
    - board: 2D list representing the Minesweeper board.
    - filename: the name of the file to read actions from.

    Raises:
    - RuntimeError: For invalid action or file format.
    - ValueError: If the row or column is invalid.
    - FileNotFoundError: If the file cannot be found.
    """
    #check if board is a 2-d list
    if not isinstance(board, list):
        raise ValueError("Board should be a list.")
    if any(not isinstance(row, list) for row in board):
        raise ValueError("Board must be a two-dimensional list (list of lists).")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            #check if the number of lines is even (each action has 2 lines)
            if len(lines) % 2 != 0:
                raise ValueError("File format is incorrect: Each action must have two lines.")

            #process each action (2 lines at a time)
            for i in range(0, len(lines), 2):
                action = lines[i].strip().upper()  # 'M' or 'V'
                coord = lines[i + 1].strip()  # Coordinate (row, col)

                #validate action
                if action not in ['M', 'V']:
                    raise ValueError(f"Invalid action: {action}. Only 'M' or 'V' are allowed.")

                #parse the coordinate, assuming format (row, col)
                if not coord.startswith('(') or not coord.endswith(')'):
                    raise ValueError(f"Invalid coordinate format: {coord}. Expected format is (row, col).")

                try:
                    row_str, col_str = coord[1:-1].split(',')
                    row = int(row_str.strip())
                    col = col_str.strip().upper() 
                except (ValueError, IndexError):
                    raise ValueError(f"Invalid coordinate format: {coord}. Expected format is (row, col).")

                #check if row and column are valid
                if not (1 <= row <= len(board)):
                    raise ValueError(f"Invalid row: {row}. Row must be between 1 and {len(board)}.")
                if not ('A' <= col <= chr(65 + len(board[0]) - 1)):
                    raise ValueError(f"Invalid column: {col}. Column must be between A and {chr(65 + len(board[0]) - 1)}.")

                #perform the corresponding action
                if action == 'M':
                    #mark or unmark the cell as a possible mine
                    change_mark(board, row, col)
                elif action == 'V':
                    #visit the cell
                    visit(board, row, col)

    except FileNotFoundError:
        raise RuntimeError(f"File not found: {filename}")
    except TypeError as e:
        raise TypeError(f"Type error occurred: {str(e)}")

    

def count_surrounding_mines(board: list[list], row: int, col: int) -> int:
    """
    Helper function to count the number of surrounding mines ('M' or '@M') around a given cell.
    Params:
        - board: 2D list representing the Minesweeper board.
        - row: the row index of the current cell (zero-based).
        - col: the column index of the current cell (zero-based).
    Returns:
        - The number of surrounding mines around the given cell.
    """
    if not isinstance(board, list):
        raise ValueError("Board should be a list.")
    if any(not isinstance(row, list) for row in board):
        raise ValueError("Board must be a two-dimensional list (list of lists).")
    mine_count = 0
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    #define the surroundings
    directions = [
        (-1, -1), (-1, 0), (-1, 1), 
        (0, -1),         (0, 1),  
        (1, -1), (1, 0), (1, 1)     
    ]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        #check if the new coordinates are within bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbor_cell = board[new_row][new_col]
            if neighbor_cell == 'M' or neighbor_cell == '@M':
                mine_count += 1

    return mine_count

