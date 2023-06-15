# linear regression with TTT
import random


class TicTacToe:
    def __init__(self):
        self.board = [['-' for _ in range(3)] for _ in range(3)]

    def is_player_win(self, board, player):
        win_combinations = [
            [[0, 0], [0, 1], [0, 2]],  # rows
            [[1, 0], [1, 1], [1, 2]],
            [[2, 0], [2, 1], [2, 2]],
            [[0, 0], [1, 0], [2, 0]],  # columns
            [[0, 1], [1, 1], [2, 1]],
            [[0, 2], [1, 2], [2, 2]],
            [[0, 0], [1, 1], [2, 2]],  # diagonals
            [[0, 2], [1, 1], [2, 0]]
        ]
        for combination in win_combinations:
            if all(board[x][y] == player for x, y in combination):
                return True
        return False

    def display_board(self):
        board = self.board
        print(
            f' {board[0][0]} | {board[0][1]} | {board[0][2]}\n',
            '------------\n',
            f'{board[1][0]} | {board[1][1]} | {board[1][2]}\n',
            '------------\n',
            f'{board[2][0]} | {board[2][1]} | {board[2][2]}',
        )

    def linear_regression_player(self, board, player):
        self.random_player(board, player)

    def get_available_spots(self, board):
        available_spots = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    available_spots.append((i, j))
        return available_spots

    def random_player(self, board, player):
        available_spots = self.get_available_spots(board)
        while True:
            x_coord = random.randint(0, 2)
            y_coord = random.randint(0, 2)
            if (x_coord, y_coord) in available_spots:
                board[x_coord][y_coord] = player
                break

    def start_against_random(self):
        player = random.choice(['X', 'O'])
        while True:
            player = 'O' if player == 'X' else 'X'
            if player == 'X':
                self.linear_regression_player(self.board, player)
            else:
                self.random_player(self.board, player)

            if self.is_player_win(self.board, player):
                self.display_board()
                print(player)
                return 1 if player == 'X' else -1
            if len(self.get_available_spots(self.board)) == 0:
                self.display_board()
                print(player)
                return 0


game = TicTacToe()
game.start_against_random()
