# Tic-Tac-Toe Game

This is a simple implementation of the Tic-Tac-Toe game in Python. It allows two players to take turns and plays out the game until a player wins or the board is filled with no winner.

## Board Design

a1 |a2 |a3 |
____________
b1 |b2 |b3 |
____________
c1 |c2 |c3 |
____________

## How to Use

1. Clone the repository .

2. Run one of the files using Python (each file implements a differnet algorithm for the computer).

3. The game will prompt the players to enter their moves. The board is represented by a 3x3 grid, where each spot is identified by a letter (a, b, c) and a number (1, 2, 3). For example, `a1` represents the top-left spot, and `c3` represents the bottom-right spot.

4. Players take turns entering their moves by typing in the spot they want to place their symbol (X or O).

5. The game will display the updated board after each move and indicate the winner if there is one. If the board is filled with no winner, the game ends in a tie.

## Code Overview

The code consists of the following components:

- `TicTacToe` class: Represents the game and provides methods for creating the board, fixing positions, checking for a win, and determining if the board is filled.

- `spot_legend` dictionary: Maps spots (e.g., 'a1', 'b2') to their corresponding indices on the board.

- `TTT_graph` dictionary: Represents a graph that defines the possible moves on the Tic-Tac-Toe board.

## Customization

If you want to extend or customize the game, you can modify the code as follows:

- Add additional validation or rules to the `fix_position` method to enforce specific game rules.

- Implement alternative win-checking algorithms in the `is_player_win` method.

- Modify the user interface to suit your needs (e.g., add a graphical interface or implement player vs. computer functionality).


