# polynomial regression with TTT
import random
import copy


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

    def weight_update(self, weights, learningConstant, train_val, approx, features):
        for i in range(len(weights)):
            weights[i] = weights[i] + learningConstant * \
                (train_val - approx) * features[i]

    
    def get_board_features(self, board, player):
        x0 = 1  # Constant
        x1 = 0  # Number of rows/columns/diagonals with two of our own pieces and one emtpy field
        x2 = 0  # Number of rows/columns/diagonals with two of opponent's pieces and one empty field
        x3 = 0  # Is our own piece on the center field
        x4 = 0  # Number of own pieces in corners
        x5 = 0  # Number of rows/columns/diagonals with one own piece and two empty fields
        x6 = 0  # Number of rows/columns/diagonals with three own pieces

        if board[1][1] == player:
            x3 += 1
        if board[0][0] == player:
            x4 += 1
        if board[2][2] == player:
            x4 += 1
        if board[0][2] == player:
            x4 += 1
        if board[2][0] == player:
            x4 += 1
        if player == 'x':
            enemy_color = 'o'
        else:
            enemy_color = 'x'

        for i in range(3):
            own_rows = 0
            own_columns = 0
            enemy_rows = 0
            enemy_columns = 0
            empty_rows = 0
            empty_columns = 0
            for j in range(3):
                if board[i][j] == 0:
                    empty_rows += 1
                elif board[i][j] == player:
                    own_rows += 1
                elif board[i][j] == enemy_color:
                    enemy_rows += 1
                if board[j][i] == 0:
                    empty_columns += 1
                elif board[j][i] == player:
                    own_columns += 1
                elif board[j][i] == enemy_color:
                    enemy_columns += 1

            if own_rows == 2 and empty_rows == 1:
                x1 += 1
            if enemy_rows == 2 and empty_rows == 1:
                x2 += 1
            if own_columns == 2 and empty_columns == 1:
                x1 += 1
            if enemy_columns == 2 and empty_columns == 1:
                x2 += 1

            if own_rows == 1 and empty_rows == 2:
                x5 += 1
            if own_columns == 1 and empty_columns == 2:
                x5 += 1
            if own_rows == 3:
                x6 += 1
            if own_columns == 3:
                x6 += 1

        for i in range(2):
            own_diagonal = 0
            enemy_diagonal = 0
            empty_diagonal = 0
            for j in range(3):
                if i == 0:
                    diagonal = board[2-j][j]
                else:
                    diagonal = board[j][j]
                if diagonal == player:
                    own_diagonal += 1
                if diagonal == 0:
                    empty_diagonal += 1
                if diagonal == enemy_color:
                    enemy_diagonal += 1
            if own_diagonal == 2 and empty_diagonal == 1:
                x1 += 1
            if enemy_diagonal == 2 and empty_diagonal == 1:
                x2 += 1
            if own_diagonal == 1 and empty_diagonal == 2:
                x5 += 1
            if own_diagonal == 3:
                x6 += 1

        return [x0, x1, x2, x3, x4, x5, x6]

    def evalApproximation(self, features, weights):
        val = 0.0
        for i in range(len(weights)):
            val += features[i] * weights[i]
        return val

    def linear_regression_player(self, board, weights, player):
        new_boards = list()
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = player
                    new_boards.append((new_board, (i, j)))
        val = -9999999
        best_move = ''
        for i in new_boards:
            features = self.get_board_features(i[0], player)
            curr_val = self.evalApproximation(features, weights)
            if val < curr_val:
                val = curr_val
                best_move = i[1]
        if best_move:
            board[best_move[0]][best_move[1]] = player
        else:
            return False

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

    def train(self):
        weights = [1.0 for _ in range(7)]
        lr = 0.00005
        player = random.choice(['X', 'O'])
        print('Start Training ...')
        for _ in range(100000):
            board = copy.deepcopy(self.board)  # Fix: Create a deep copy of the board
            while True:
                pre_features = self.get_board_features(board, player)
                pre_approx = self.evalApproximation(pre_features, weights)

                if player == 'X':
                    self.linear_regression_player(board, weights, player)
                else:
                    self.random_player(board, player)

                if self.is_player_win(board, player):
                    if player == 'X':
                        result = 1
                    else:
                        result = -1

                    curr_features = self.get_board_features(board, player)
                    curr_approx = self.evalApproximation(curr_features, weights)
                    self.weight_update(weights=weights, learningConstant=lr,
                                    train_val=result, approx=curr_approx, features=pre_features)
                    break

                if len(self.get_available_spots(board)) == 0:
                    result = 0
                    curr_features = self.get_board_features(board, player)
                    curr_approx = self.evalApproximation(curr_features, weights)
                    self.weight_update(weights=weights, learningConstant=lr,
                                    train_val=result, approx=curr_approx, features=pre_features)
                    break

                succ_features = self.get_board_features(board, player)
                succ_approx = self.evalApproximation(succ_features, weights)
                self.weight_update(weights=weights, learningConstant=lr, train_val=succ_approx, approx=pre_approx,
                                features=pre_features)
                player = 'X' if player == 'O' else 'O'

        print('Start Evaluation against Random Player')
        count_win = 0
        count_loss = 0
        count_draw = 0
        for _ in range(10000):
            board = [['-' for _ in range(3)] for _ in range(3)]  
            player = random.choice(['X', 'O'])
            while True:
                pre_features = self.get_board_features(board, player)
                pre_approx = self.evalApproximation(pre_features, weights)

                if player == 'X':
                    self.linear_regression_player(board, weights, player)
                else:
                    self.random_player(board, player)

                if self.is_player_win(board, player):
                    if player == 'X':
                        count_win += 1
                        break
                    else:
                        count_loss += 1
                        break

                if len(self.get_available_spots(board)) == 0:
                    count_draw += 1
                    break

                succ_features = self.get_board_features(board, player)
                succ_approx = self.evalApproximation(succ_features, weights)
                self.weight_update(weights=weights, learningConstant=lr, train_val=succ_approx, approx=pre_approx,
                                features=pre_features)
                player = 'X' if player == 'O' else 'O'

        print('Wins: ' + str(count_win))
        print('Draws: ' + str(count_draw))
        print('Losses: ' + str(count_loss))



game = TicTacToe()
game.train()
