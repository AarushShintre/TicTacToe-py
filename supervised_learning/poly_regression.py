import random
import copy
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


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

    def weight_update(self, weights, learning_constant, train_val, approx, features):
        for i in range(len(weights)):
            weights[i] = weights[i] + learning_constant * \
                (train_val - approx) * features[i]

    def get_board_features(self, board, player, degree):
        features = [0.0 for _ in range((degree + 1) * 10)]

        player_color = player
        enemy_color = 'O' if player == 'X' else 'X'

        for i in range(3):
            own_rows = 0
            enemy_rows = 0
            empty_rows = 0
            own_columns = 0
            enemy_columns = 0
            empty_columns = 0

            for j in range(3):
                if board[i][j] == player_color:
                    own_rows += 1
                elif board[i][j] == enemy_color:
                    enemy_rows += 1
                else:
                    empty_rows += 1

                if board[j][i] == player_color:
                    own_columns += 1
                elif board[j][i] == enemy_color:
                    enemy_columns += 1
                else:
                    empty_columns += 1

            features[own_rows] += 1
            features[3 + own_columns] += 1
            features[6] += 1 if own_rows + own_columns == 2 else 0

        for i in range(2):
            own_diagonal = 0
            enemy_diagonal = 0
            empty_diagonal = 0

            for j in range(3):
                if i == 0:
                    diagonal = board[2 - j][j]
                else:
                    diagonal = board[j][j]

                if diagonal == player_color:
                    own_diagonal += 1
                elif diagonal == enemy_color:
                    enemy_diagonal += 1
                else:
                    empty_diagonal += 1

            features[9] += 1 if own_diagonal == 2 else 0

        features = np.array(features).reshape(1, -1)
        polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)
        transformed_features = polynomial_features.fit_transform(features)

        return transformed_features[0].tolist()

    def train(self, num_iterations, learning_constant, degree):
        weights = [0.0 for _ in range((degree + 1) * 10)]
        for _ in range(num_iterations):
            self.board = [['-' for _ in range(3)] for _ in range(3)]
            curr_player = 'X'
            while True:
                available_moves = self.get_available_moves()
                if not available_moves:
                    break
                move = random.choice(available_moves)
                self.make_move(move[0], move[1], curr_player)
                features = self.get_board_features(self.board, curr_player, degree)
                if self.is_player_win(self.board, curr_player):
                    self.weight_update(
                        weights, learning_constant, 1, self.evaluate(self.board, curr_player), features)
                    break
                elif self.is_player_win(self.board, 'O' if curr_player == 'X' else 'X'):
                    self.weight_update(
                        weights, learning_constant, -1, self.evaluate(self.board, curr_player), features)
                    break
                elif len(available_moves) == 1:
                    self.weight_update(
                        weights, learning_constant, 0, self.evaluate(self.board, curr_player), features)
                    break
                else:
                    self.weight_update(
                        weights, learning_constant, 0, self.evaluate(self.board, curr_player), features)
                    curr_player = 'O' if curr_player == 'X' else 'X'
        return weights

    def make_move(self, row, col, player):
        self.board[row][col] = player

    def get_available_moves(self):
        available_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    available_moves.append((i, j))
        return available_moves

    def evaluate(self, board, player):
        if self.is_player_win(board, player):
            return 1
        elif self.is_player_win(board, 'O' if player == 'X' else 'X'):
            return -1
        else:
            return 0

    def get_random_move(self, board, player):
        available_spots = self.get_available_moves()
        while True:
            x_coord = random.randint(0, 2)
            y_coord = random.randint(0, 2)
            if (x_coord, y_coord) in available_spots:
                return (x_coord, y_coord)

    def play(self, weights):
        count_win = 0
        count_draw = 0
        count_loss = 0
        for i in range(1000):
            self.board = [['-' for _ in range(3)] for _ in range(3)]
            curr_player = 'X'
            while True:
                if curr_player == 'X':
                    move = self.get_best_move(weights, curr_player)
                    self.make_move(move[0], move[1], curr_player)
                else:
                    move = self.get_random_move(weights, curr_player)
                    self.make_move(move[0], move[1], curr_player)
                if self.is_player_win(self.board, curr_player):
                    if curr_player == 'X':
                        count_win += 1
                    else:
                        count_loss += 1
                    break
                elif len(self.get_available_moves()) == 1:
                    count_draw += 1
                    break
                else:
                    curr_player = 'O' if curr_player == 'X' else 'X'
        print('Wins: ' + str(count_win))
        print('Draws: ' + str(count_draw))
        print('Losses: ' + str(count_loss))

    def get_best_move(self, weights, player):
        best_move = None
        best_value = float('-inf')

        for move in self.get_available_moves():
            self.board[move[0]][move[1]] = player
            features = self.get_board_features(self.board, player, degree)
            value = sum(feature * weight for feature,
                        weight in zip(features, weights))
            self.board[move[0]][move[1]] = '-'
            if value > best_value:
                best_value = value
                best_move = move

        return best_move


if __name__ == '__main__':
    tictactoe = TicTacToe()
    degree = 2  # Degree of the polynomial features
    weights = tictactoe.train(10000, 0.001, degree)
    tictactoe.play(weights)
