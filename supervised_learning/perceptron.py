import random
import copy

class TicTacToe():
    def __init__(self):
        self.win_combinations = [
            [[0, 0], [0, 1], [0, 2]],  # rows
            [[1, 0], [1, 1], [1, 2]],
            [[2, 0], [2, 1], [2, 2]],
            [[0, 0], [1, 0], [2, 0]],  # columns
            [[0, 1], [1, 1], [2, 1]],
            [[0, 2], [1, 2], [2, 2]],
            [[0, 0], [1, 1], [2, 2]],  # diagonals
            [[0, 2], [1, 1], [2, 0]]
        ]
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.weights = [1.0 for _ in range(10)]
        self.learning_rate = 0.01

    def is_player_win(self, board, player):
        for combination in self.win_combinations:
            if all(board[x][y] == player for x, y in combination):
                return True
        return False

    def is_board_filled(self, board):
        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    return False
        return True

    def display_board(self):
        board = self.board
        print(
            f' {board[0][0]} | {board[0][1]} | {board[0][2]}\n',
            '------------\n',
            f'{board[1][0]} | {board[1][1]} | {board[1][2]}\n',
            '------------\n',
            f'{board[2][0]} | {board[2][1]} | {board[2][2]}',
        )

    def get_available_moves(self):
        available_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    available_moves.append((i, j))
        return available_moves

    def get_random_move(self):
        available_spots = self.get_available_moves()
        while True:
            x_coord = random.randint(0, 2)
            y_coord = random.randint(0, 2)
            if (x_coord, y_coord) in available_spots:
                return (x_coord,y_coord)

    def make_move(self, row, col, player):
        self.board[row][col] = player

    def update_weights(self, train_value, approx, features):
        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate * (train_value - approx) * features[i]

    def evaluate(self, board, player):
        if self.is_player_win(board, player):
            return 1  # self winning
        if self.is_player_win(board, player='O' if player == 'X' else 'X'):
            return -1  # opposite player winning
        if self.is_board_filled(board):
            return 0
        return 2  # return 2 if no conclusive point reached

    # add a function to evaluate board features and return these at each move
    def get_board_features(self, board, player):
        features = [0.0 for _ in range(10)]

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

        return features

    def map_moves(self, board, player):
        new_boards = list()
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = player
                    new_boards.append((new_board, (i, j)))
        return new_boards

    def linear_regression_player(self, board, weights, player):
        new_boards = list()
        for i in range(len(self.get_available_moves())): 
            new_boards.extend([board for board in self.map_moves(board, player) if board not in new_boards] ) 
            player = 'X' if player == 'O' else 'O'
            new_boards.extend([board for board in self.map_moves(board, player) if board not in new_boards] ) 
                    
        val = 0
        best_move = ''
        for i in new_boards:
            features = self.get_board_features(i[0], player)
            curr_val = sum(feature * weight for feature,
                        weight in zip(features, weights))
            if curr_val > 0:
                best_move = i[1]
                board[best_move[0]][best_move[1]] = player

        

    def get_available_spots(self, board):
        available_spots = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    available_spots.append((i, j))
        return available_spots
    
    def train(self, epochs):
        weights = self.weights
        player = random.choice(['X', 'O'])
        for i in range(epochs):
            board = self.board
            while (True):
                pre_features = self.get_board_features(board, player)
                pre_approx = sum(feature * weight for feature,
                        weight in zip(pre_features, weights))
                self.linear_regression_player(board, weights, player)
                if self.is_player_win(board, player):
                    if player == 'X':
                        result = 1

                    else:
                        result = -1

                    curr_features = self.get_board_features(board, player)
                    curr_approx = sum(feature * weight for feature,
                        weight in zip(curr_features, weights))
                    self.update_weights(train_value=result, approx=curr_approx, features=pre_features)
                    break
                if len(self.get_available_spots(board)) == 0:
                    result = 0
                    curr_features = self.get_board_features(board, player)
                    curr_approx = sum(feature * weight for feature,
                        weight in zip(curr_features, weights))
                    self.update_weights(train_value=result, approx=curr_approx, features=pre_features)
                    break

                succ_features = self.get_board_features(board, player)
                succ_approx = sum(feature * weight for feature,
                        weight in zip(succ_features, weights))
                print(succ_approx)
                self.update_weights(train_value=succ_approx, approx=pre_approx, features=pre_features)
                player = 'X' if player == 'O' else 'O'
        return weights

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
                    move = self.get_random_move()
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
            features = self.get_board_features(self.board, player)
            value = sum(feature * weight for feature,
                        weight in zip(features, weights))
            self.board[move[0]][move[1]] = '-'
            if value > best_value:
                best_value = value
                best_move = move

        return best_move

if __name__ == '__main__':
    tictactoe = TicTacToe()
    weights = tictactoe.train(10000)
    tictactoe.play(weights)
