import random

spot_legend = {
    'a': 0,
    'b': 1,
    'c': 2
}

TTT_graph = {
    'a1': ['a2', 'b1', 'b2'],
    'a2': ['a1', 'a3', 'b1', 'b2', 'b3'],
    'a3': ['a2', 'b2', 'b3'],
    'b1': ['a1', 'a2', 'b2', 'c1', 'c2'],
    'b2': ['a1', 'a2', 'a3', 'b1', 'b3', 'c1', 'c2', 'c3'],
    'b3': ['a2', 'a3', 'b2', 'b3', 'c2', 'c3'],
    'c1': ['b1', 'b2', 'c2'],
    'c2': ['b1', 'b2', 'b3', 'c1', 'c3'],
    'c3': ['c2', 'b2', 'b3']
}


class TicTacToe:
    def __init__(self):
        self.board = []

    def create_board(self):
        self.board = [['-' for _ in range(3)] for _ in range(3)]

    def fix_position(self, spot, player):
        x_coord = spot_legend[spot[0]]
        y_coord = int(spot[1]) - 1
        if self.board[x_coord][y_coord] == '-':
            self.board[x_coord][y_coord] = player
            return True
        else:
            return False

    def is_player_win(self, board, player):
        win_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]

        for combination in win_combinations:
            cells = [board[row][col] for row, col in combination]
            if all(cell == player for cell in cells):
                return True

        return False

    def is_board_filled(self, board):
        for row in board:
            if '-' in row:
                return False
        return True
    
    def get_available_spots(self, board):
        available_spots = []
        for spot in TTT_graph.keys():
            x_coord = spot_legend[spot[0]]
            y_coord = int(spot[1]) - 1
            if board[x_coord][y_coord] == '-':
                available_spots.append(spot)
        return available_spots

    def get_opponent(self, player):
        return 'O' if player == 'X' else 'X'

    def heuristic(self, board, player):
        opponent = self.get_opponent(player)
        
        # Check if player can win
        for spot in TTT_graph.keys():
            x, y = spot_legend[spot[0]], int(spot[1]) - 1
            if board[x][y] == '-':
                board[x][y] = player
                if self.is_player_win(board, player):
                    board[x][y] = '-'
                    return 1
                board[x][y] = '-'
        
        # Check if opponent can win and block
        for spot in TTT_graph.keys():
            x, y = spot_legend[spot[0]], int(spot[1]) - 1
            if board[x][y] == '-':
                board[x][y] = opponent
                if self.is_player_win(board, opponent):
                    board[x][y] = '-'
                    return -1
                board[x][y] = '-'
        
        # If a win is not possible, return 0 for a draw
        return 0

    def alpha_beta_search(self, board, player, alpha, beta, depth):
        if self.is_player_win(board, 'X'):
            return -1
        elif self.is_player_win(board, 'O'):
            return 1
        elif self.is_board_filled(board) or depth == 0:
            return self.heuristic(board, player)

        opponent = self.get_opponent(player)
        best_value = float('-inf') if player == 'O' else float('inf')

        available_spots = self.get_available_spots(board)

        if player == 'O':
            for spot in available_spots:
                x, y = spot_legend[spot[0]], int(spot[1]) - 1
                board[x][y] = player
                value = self.alpha_beta_search(board, opponent, alpha, beta, depth - 1)
                board[x][y] = '-'
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
        else:
            for spot in available_spots:
                x, y = spot_legend[spot[0]], int(spot[1]) - 1
                board[x][y] = player
                value = self.alpha_beta_search(board, opponent, alpha, beta, depth - 1)
                board[x][y] = '-'
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if alpha >= beta:
                    break

        return best_value

    def computer_player(self, board, player):
        best_value = float('-inf')
        best_move = None
        available_spots = self.get_available_spots(board)
        opponent = self.get_opponent(player)

        for spot in available_spots:
            x, y = spot_legend[spot[0]], int(spot[1]) - 1
            board[x][y] = player
            value = self.alpha_beta_search(board, opponent, float('-inf'), float('inf'), 5)
            board[x][y] = '-'

            if value == 1:
                return spot

            if value > best_value:
                best_value = value
                best_move = spot

        return best_move
    
    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def start_against_random(self):
        self.create_board()
        player = random.choice(['X','O'])
        while True:
            if player == 'X':
                spot = self.computer_player(self.board, player)
                self.fix_position(spot, player)
            else:
                available_spots = self.get_available_spots(self.board)
                spot = random.choice(available_spots)
                self.fix_position(spot, player)

            if self.is_player_win(self.board, player):
                if player == 'X':
                    print(self.board)
                    return 1
                else:
                    return -1

            if self.is_board_filled(self.board):
                print('draw')
                return 0

            player = 'O' if player == 'X' else 'X'
            

    def play(self):
        self.create_board()
        print("Tic Tac Toe - Play against AI")
        self.print_board()
        player = random.choice(['X','O'])
        while True:
            if player == 'X':
                spot = input("Enter the spot (e.g., 'a1', 'b2', 'c3'): ")
                if not self.fix_position(spot, player):
                    print("Invalid spot. Try again.")
                    continue
            else:
                spot = self.computer_player(self.board, player)
                self.fix_position(spot, player)
                print("AI chose spot:", spot)

            self.print_board()

            if self.is_player_win(self.board, player):
                print("Congratulations! You won!")
                break
            elif self.is_board_filled(self.board):
                print("It's a tie!")
                break

            player = 'X' if player=='O' else 'O'

# game = TicTacToe()
# game.play()

def test():
    samples = 5
    summation_score_per_gameplay = 0
    for _ in range(samples):
        score = 0
        game_plays = 10
        for _ in range(game_plays):
            game = TicTacToe()
            result = game.start_against_random()
            if result == 1 or result==0:
                score += 1
        summation_score_per_gameplay += score/game_plays
        print(score/game_plays)

    print('The A* agent won or atleast had a draw', (summation_score_per_gameplay/samples)
          * 100, '%', 'of times on average')

# runs 5 different samples each of 1000 games, and returns average win rates of the computer against a random
test()