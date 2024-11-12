# Programming Assignment 2: Minesweeper Game

## Before You Begin
- Read this document carefully. 
- Double check the timeline for this PA.
- We expect a comprenhensive use of exception handling and user input validation.

## Learning Objective:
- To assess students' master of Python basics, functions, lists, tuples, and dictionaries.
- To assess students' mastery of abstractions (implemented using functions).
- To assess students' understanding and use of black-box/white-box testing.

### Learning outcomes:
1. Read and write code in Python,
1. Analyze a problem and create a computer program to solve it,
1. Use top-down design and abstraction to write clean, readable, fixable code,


## Problem Description
You will implement a console version of the traditional MS-Windows&reg; Minesweeper. 
If you never played, [here is an online version](https://minesweeper.online/game/3815444623)

The game starts with a board ($9\times 9$ for beginners but can be any size) in which each tile (cell) represents a space in the terrain. 

![](https://people.duke.edu/~jap169/courses/2024.08/mines_.png)

Your goal is to find a given number of mines without stepping into one. 
You achieve this by clicking on one of these tiles. 
If the tile didn't have a mine, it will show you a number representing how many mines are around it.

![](https://people.duke.edu/~jap169/courses/2024.08/mines_started.jpg)

If you think there is a mine on a particular tile, you can mark it (flag it) as suspicious. 

![](https://people.duke.edu/~jap169/courses/2024.08/mines_flagged.png)

Of course, if you step on a tile that has a mine, well... GAME OVER.

![](https://people.duke.edu/~jap169/courses/2024.08/mines_boom.png)

Your goal is to have stepped into (visited) all but the mines, and have the mines flagged. 

## Functions `pa2.py`

In this file you implement the funtions to run the program, but **not** the main program.

The main map (`board`) is implemented as a **zero-indexed 2D list**, but what you store there is totally up to you. 
Keep in mind, we will assess whether you used the data structures we discussed so far efficiently.


- `initalize_board_random`
    - Generates a new board with height rows and width columns, and randomly places 
    mine_count mines on it.
    - The minimum board size is 4x4.
    - The board cannot have more than 26 columns and more than 50 rows, and there must be at 
    least 5 mines in the board
    - **Parameters**:
        - `board_height`: number of rows. Rows will be input from 1 to N
        - `board_width`: number of cols. Colls will be input from A to Z
        - `mine_count`: the number of mines to randomly place.
        - `seed`: to initialize the random generator. _If you don't set this before the first use 
        of random, you may not pass all tests. Just use it once!
    - **Returns**:
        - A zero-indexed 2D list, indexed by row,column.
- `initalize_board_file`
    - Generates a new board with height rows and width columns, and places the mines from the 
    coordinates listed in the file. 
    - The board characteristics are the same from `initialize_board_random`.
    - **Parameters**:
        - `board_height`: number of rows. Rows will be input from 1 to N
        - `board_width`: number of cols. Colls will be input from A to Z
        - `filename`: must be a utf-8 encoded text file with one mine coordinate per line in the 
        format `(x,y)`. Spaces/tabs may be added and should not impact the outcome. 
        If the line contains anything else but a coordinate in the formate described, 
        just ignore that line. x represents a row number (1-N) and y a column (A-Z). 
        You need to check the integrity of the file (i.e., that the file makes sense
        for your board). Invalid entries are just ignored.
    - **Returns**:
        - A **zero-indexed 2D list**, indexed by row,column.
- `validate_board_dimensions`
    - This function validates that the argument is a 2D list and validates whether it is a valid 
    board or not. It DOES NOT LOOK at the content. 
    - When somenthing is not right, it returns a `ValueError` with an appropiate description.
    - Returns True when all validations passed (otherwise an exception was raised.)
- `display_board`
    - Returns a string to print the board using the following format:
    ```
    |---| A | B | C | D |...
    |001| o | 1 | o |   |...
    |002| o | @ | o | o |...
    |003| o | o | 2 | o |...
    ...
    ```
    - A *number* (1-8) means number of mines in the neighbors. The user visited that cell.
    - A *space* means that in the neighbors there are NO mines. The user visited that cell.
    - A `o` (lowercase letter o) means that the cell was NOT visited and not marked.
    - A `@` means that the user marked that place as a possible bomb.
    - **Return**:
        - the string with the representation described.
- `visit`
    - The user visits (steps into) that cell (tile). 
    - If there is no mine, then you need to take the actions to mark that cell as visited. 
    - If there is a mine, rase a `RuntimeError` with message "`BOOM! GAME OVER!`".
    - If the cell was marked as possible mine, unmark it and visit it.
    - If the cell was previously visited, then raise a `ValueError`. 
    - **Params**:
        - `board`: is the 2D board list. 
        - `row`: an integer between 1 and N (the number of rows)
        - `col`: a character between A-Z. 
- `change_mark`
    - The user marks/unmarks this cell as a possible mine. 
        - The user does **NOT** visit this cell by marking it.
        - If the cell is marked, then this unmarks it. If it is not marked, it marks it. 
        - If the cell was visited, then this raises a `ValueError` exception. 
    - **Params**:
        - `board`: is the 2D board list. 
        - `row`: an integer between 1 and N (the number of rows)
        - `col`: a character between A-Z. 

- `validate_game`
    - Validates the Game. 
        - When the board is all visited and all not visited cells are marked, we validate whether
        the user won or not. 
        - If there are unvisited and unmarked cells, raise `RuntimeError` with "`User Defeated`" message.
        - If all cells are marked or visited, check that all marked cells have a mine. 
        - When there are marked cells without mines, raise `RuntimeError` '`USER LOST-Not a mine at x,y.`'
        (x,y must be 1-N, A-Z accordingly)
        - When all the marked cells contain mines, return "`YOU WIN!!!`"

- `actions_from_file`
    - Reads actions from file (utf-8 encoded).
       - Each action is represented in 2 lines. 
       - The first line will either say `M` (for mark) or `V` for visit.
       - The nest line will have the coordinate (same format as initialize.)
       - If the action is not `M` or `V`, raise a `RuntimeError`. 
       The coordinate handling is as described for initialization.
       - The file is expected to have (Action\nCoord)* if the format is not correct, raise a 
       `RuntimeError`.


## Use of Abstraction
You were given with the 'interface' of the program. 
The set of functions that allows us to generalize (up to a point) this application.

However, you can (and should) add more functions to make your program more readable, simpler, less redundant. 
This is also going to be assessed during the code review.

## Main Program `main.py`
You must implement your main program to run the game as you like. 
We will not test this automatically but during the code review. 


### Coordinates
The user will use numbers (1-N) to refer to the rows of the map, and capital letters (A-Z) to refer to the columns 
of the map. In such a way that `(1,A)` is the top-left and `(9,I)` is the bottom-right tile in a $9\times9$ map.
Note that your functions (implemented on `pa2.py`) will receive these type of coordinates, and your code must handle them appropiatelly.

### Example main program:
- Initialize the board with user inputs.
- Give the user the options to:
    - step into a tile (visit)
    - Flag/unflag (mark) a tile
    - Check for victory (beware that if it is not complete, the user will lose. )

## Tests `user_tests.py`
This file is provided for you to write `pytest` functions. 
You will be provided with a function to get access to our solution module for you to conduct tests. 

*More information will come during Testing module in the lectures and how to use this with ADTG.*


## Files
- Three files are provided as samples:
- `mines1.txt`: coordinate files with valid and invalid inputs. For a $9\times9$ board.
- `mines2.txt`: coordinate files with valid coordinate inputs and invalid inputs (all starting with #). For a $4\times4$ board.
- `actions2.txt`: action files for the `mines2.txt` map for $4\times4$ board. This outcome on the user wining the game. 


## Example Interaction:
This is just an example of **printing the map** and iterating over the `mines2.txt` map. 
*The only output that you must match is the map.*

```
Invalid coordinate [#4x4 1-4, ABCD, 5 mines]
Invalid coordinate [#]
Invalid coordinate [#@@@1]
Invalid coordinate [#@@31]
Invalid coordinate [#221.]
Invalid coordinate [#....]
|---| A | B | C | D |
|001| o | o | o | o |
|002| o | o | o | o |
|003| o | o | o | o |
|004| o | o | o | o |

Action[V] -- Coord Line: [(1,D)]
Action[V] -- Coord Line: [(2,C)]
Action[V] -- Coord Line: [(2,D)]
Action[M] -- Coord Line: [(1,A)]
Action[M] -- Coord Line: [(1,B)]
Action[M] -- Coord Line: [(1,C)]
Action[M] -- Coord Line: [(2,A)]
Action[M] -- Coord Line: [(2,B)]
Action[V] -- Coord Line: [(3,A)]
Action[V] -- Coord Line: [(3,B)]
Action[V] -- Coord Line: [(3,C)]
Action[V] -- Coord Line: [(3,D)]
Action[V] -- Coord Line: [(4,A)]
Action[V] -- Coord Line: [(4,B)]
Action[V] -- Coord Line: [(4,C)]
Action[V] -- Coord Line: [(4,D)]
|---| A | B | C | D |
|001| @ | @ | @ | 1 |
|002| @ | @ | 3 | 1 |
|003| 2 | 2 | 1 |   |
|004|   |   |   |   |

YOU WIN!!!
```

## TIMELINE
1. You recived this Programming Assigment on *October 7th*. 
1. Validating your Tests
    - Use ADTG to run **your test cases** against your solution and our solution in the platfom.
    - This will be available from **October 11th 8am.** to *October 18th, 7:59am*. 
    - You will require **5 tokens** to run the test cases.
    - The more test cases you write, the more thoroughly your will validating your implementation and your understanding. 
1. Automatic grading
    - ADTG will use **our** test cases to validate your code.
    - This will be available from **October 18th 8am** until the submission deadline. 
    - You will require **50 tokens** to grade this assessment. 
1. Submission deadline is **October 20th, 11:59pm.**. 
    - After the deadline, the grader will output a **zero** for your grade. 

_**Note:** the grading in advance for this assessment is limited! Just one day and the weekend._ **_We may not be available during the weekend_.**
One of the goals of this assessment is to _assess how comprenhensive your testing is_. 
By running your tests again our solution, you will have the tools to identify question points, issues on your program and fix it. 

## HINTS
- Carefully think the solution for your assigment. 
- The minimum map size is $4\times4$ which is manegeable to run on paper (run one example).
    - You have one example already! 


## Restrictions
- Only **`random`** and **`re`** modules are allowed. 
- You will be using `pytest` to desing and implement your test cases. 

## Submission:
- Your functions must be implemented on `pa2.py`
- Your main program in `main,py`. We'll review this during Code Review
- Your tests must be implemented in `user_tests.py`.
- *No other files will be uploaded to the grader*.

## Rubric:
- **Automatic Testing** counts for $70\%$ of the assignment. 
- **Code Review** counts for $30\%$ of the assignment. 
    - This includes (but not limited to):
        - correct use of data structures, constrol statements, variable names, use of comments, and programming style. 
        - correct use of abstraction (encapsulating code in functions to reuse)
        - appropiate comments
        - correct use of typehints

