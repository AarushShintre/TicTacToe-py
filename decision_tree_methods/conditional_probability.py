import random


class TicTacToe:
    def __init__(self):
        self.board = [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]

    def print_board(self):
        for i in range(3):
            print(" | ".join(self.board[i]))
            if i < 2:
                print("---------")

    def check_win(self, board, player):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == player:
                return True
            if board[0][i] == board[1][i] == board[2][i] == player:
                return True
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False

    def is_board_full(self, board):
        for row in board:
            if " " in row:
                return False
        return True

    def get_available_moves(self, board):
        available_spots = []
        for i in range(3):
            for j in range(3):
                if board[i][j] not in ['X', 'O']:
                    available_spots.append((i, j))
        return available_spots

    def conditional_probability(self, board, player):
        possible_moves = self.get_available_moves(board)
        win_dict = {}

        for move in possible_moves:
            win_dict[move] = [0, 0, 0, 0]  # [wins, ties, losses, total_games]

            curr_board = [row[:]
                          for row in board]  # Create a copy of the board
            curr_board[move[0]][move[1]] = player
            current_player = "O" if player == "X" else "X"

            while True:
                win_dict[move][3] += 1
                possible_moves = self.get_available_moves(curr_board)
                if possible_moves:
                    next_move = random.choice(possible_moves)
                    curr_board[next_move[0]][next_move[1]] = current_player
                    current_player = "O" if current_player == "X" else "X"

                if self.check_win(curr_board, current_player):
                    if current_player == player:
                        win_dict[move][0] += 1
                        break
                    else:
                        win_dict[move][2] += 0.5
                        break
                elif self.is_board_full(curr_board):
                    win_dict[move][1] += 0.75
                    break

        best_move = max(win_dict, key=lambda x: (
            win_dict[x][0] + win_dict[x][1] - win_dict[x][2]) / win_dict[x][3])
        return best_move

    def play_game(self):
        current_player = random.choice(['X', 'O'])
        while True:
            self.print_board()
            print()
            if current_player == "X":
                row, col = self.conditional_probability(
                    self.board, current_player)
                self.board[row][col] = current_player
            else:
                while True:
                    row = int(input("Enter the row (0-2): "))
                    col = int(input("Enter the column (0-2): "))
                    if self.board[row][col] == " ":
                        self.board[row][col] = current_player
                        break
                    else:
                        print("Invalid move. Try again.")
            if self.check_win(self.board, current_player):
                self.print_board()
                print(current_player + " wins!")
                break
            if self.is_board_full(self.board):
                self.print_board()
                print("It's a tie!")
                break
            current_player = "O" if current_player == "X" else "X"

    def start_against_random(self):
        current_player = random.choice(['X', 'O'])
        while True:
            if current_player == "X":
                row, col = self.conditional_probability(
                    self.board, current_player)
                self.board[row][col] = current_player
            else:
                try:
                    possible_moves = self.get_available_moves(self.board)
                    if possible_moves:
                        next_move = random.choice(possible_moves)
                        self.board[next_move[0]][next_move[1]] = current_player
                    else:
                        if self.check_win(self.board, current_player):
                            return 1 if current_player == 'X' else -1
                        if self.is_board_full(self.board):
                            return 0
                except:
                    if self.check_win(self.board, current_player):
                        return 1 if current_player == 'X' else -1
                    if self.is_board_full(self.board):
                        return 0
            if self.check_win(self.board, current_player):
                return 1 if current_player == 'X' else -1
            if self.is_board_full(self.board):
                return 0
            current_player = "O" if current_player == "X" else "X"


# Start the game
# game = TicTacToe()
# game.play_game()


def test():
    samples = 5
    summation_score_per_gameplay = 0
    for _ in range(samples):
        score = 0
        game_plays = 1000
        for _ in range(game_plays):
            game = TicTacToe()
            result = game.start_against_random()
            if result == 1 or result == 0:
                score += 1
        summation_score_per_gameplay += score / game_plays
    
    print('The conditional probability agent won, or had a draw ', (summation_score_per_gameplay / samples) * 100,
          '%', 'of times on average')

test()
