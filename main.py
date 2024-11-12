"""Minesweeper Game"""
# TODO: implement a game that uses your pa2.py functions to play the game. 
# We will grade this during the code review, but this program will NOT be 
# automatically graded.
# In main.py

from pa2 import (
    initalize_board_random,
    display_board,
    visit,
    change_mark,
    validate_game,
    display_true_board #this is to display the true value of each cell in a board
)

def main():
    print("Welcome to my Minesweeper!")
    
    while True:
        try:
            board_height = int(input("Enter board height (4-50): "))
            board_width = int(input("Enter board width (4-26): "))
            mine_count = int(input("Enter the number of mines (5 or more): "))
            board = initalize_board_random(board_height, board_width, mine_count)
            break
        except ValueError as e:
            print(f"Error: {e}. Please enter valid numbers.")
        except TypeError as e:
            print(f"Error: {e}. Please enter integers for the board dimensions and mine count.")

    print("Here is the initial game board:")
    print(display_board(board))

    #Main game loop
    while True:
        action = int(input("What would you like to do? (visit(1)/change_mark(2)/validate(3)): ")) #takes input as 1,2,3(int)

        if action not in [1, 2, 3]:
            print("Invalid action. Please choose 'visit(1)', 'change_mark(2)', or 'validate(3)'.")
            continue

        if action == 3:
            try:
                result = validate_game(board)
                print(result)
                if result == "YOU WIN!!!":
                    print("Congratulations! You've won the game!")
                    break
            except RuntimeError as e:
                print(e)
            continue

        #ask for the cell coordinates
        try:
            row = int(input("Enter the row number: "))
            col = input("Enter the column letter (A-Z): ").strip().upper()
            if len(col) != 1 or not col.isalpha():
                raise ValueError("Invalid column input. Please enter a single letter between A and Z.")
        except ValueError as e:
            print(f"Error: {e}")
            continue

        try:
            if action == 1:
                visit(board, row, col)
            elif action == 2:
                change_mark(board, row, col)

            #display the updated board after each action
            print(display_board(board))
        except ValueError as e:
            print(f"Error: {e}")
        except RuntimeError as e:
            print(f"Error: {e}")
            if "GAME OVER" in str(e):
                print("You've hit a mine. Game over!")
                print(display_true_board(board))  #show the true board after the game ends
                break
        except TypeError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()


