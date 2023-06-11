import heapq
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
        y_coord = int(spot[1])-1
        if self.board[x_coord][y_coord] == '-':
            self.board[x_coord][y_coord] = player
            return True
        else:
            return False

    def is_player_win(self, board, player):
        win = None
        n = 3
        # Checking rows
        for i in range(n):
            win = True
            for j in range(n):
                if board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # Checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # Checking diagonals
        win = True
        for i in range(n):
            if board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win

        return False

    def is_board_filled(self, board):
        for row in board:
            for item in row:
                if item == '-':
                    return False
        return True

    def transform_to_index(self, spot):
        x_coord = spot_legend[spot[0]]
        y_coord = int(spot[1]) - 1
        return (x_coord, y_coord)

    def get_visited(self, check_board, computer_player):
        visited = []
        computer_visited = []
        board = check_board
        for row in range(3):
            for col in range(3):
                index = board[row][col]
                if index != '-':
                    letter = ''
                    col += 1
                    for item in spot_legend.items():
                        if item[1] == row:
                            letter = item[0]
                    spot = letter+str(col)
                    visited.append(spot)
                    if index == computer_player:
                        computer_visited.append(spot)
        return visited, computer_visited

    def heuristic(self, board, player):
        score = 0
        opponent = 'X' if player == 'O' else 'O'

        # Check rows
        for row in board:
            if row.count(opponent) == 2 and row.count('-') == 1:
                score -= 1
            elif row.count(player) == 2 and row.count('-') == 1:
                score += 1

        # Check columns
        for col in range(3):
            column = [board[row][col] for row in range(3)]
            if column.count(opponent) == 2 and column.count('-') == 1:
                score -= 10
            elif column.count(player) == 2 and column.count('-') == 1:
                score += 20

        # Check diagonals
        diagonal1 = [board[i][i] for i in range(3)]
        diagonal2 = [board[i][2-i] for i in range(3)]
        if diagonal1.count(opponent) == 2 and diagonal1.count('-') == 1:
            score -= 10
        elif diagonal1.count(player) == 2 and diagonal1.count('-') == 1:
            score += 20

        if diagonal2.count(opponent) == 2 and diagonal2.count('-') == 1:
            score -= 10
        elif diagonal2.count(player) == 2 and diagonal2.count('-') == 1:
            score += 20

        # Additional condition for making a draw
        if score == 0:
            score += 10

        return score


    def a_star_search(self, board, player):
        frontier = []
        initial_state = (board, [], 0)
        heapq.heappush(frontier, (self.heuristic(board, player), initial_state))
        visited = set()
        while frontier:
            curr_board, moves, depth = heapq.heappop(frontier)[1]
            if self.is_player_win(curr_board, player):
                return moves[-1]
            visited.add(tuple(map(tuple, curr_board)))
            possible_moves = [spot for spot in TTT_graph.keys()
                            if spot not in self.get_visited(curr_board, player)[0]]
            for move in possible_moves:
                index = self.transform_to_index(move)
                new_board = [row[:] for row in curr_board]
                new_moves = moves + [move]
                new_board[index[0]][index[1]] = player
                if tuple(map(tuple, new_board)) not in visited:
                    heapq.heappush(frontier, (self.heuristic(new_board, player),
                                            (new_board, new_moves, depth + 1)))

        return None


    def random_player(self, board, player):
        possible_spots = [spot for spot in TTT_graph.keys()
                          if spot not in self.get_visited(board, player)[0]]
        if len(possible_spots) > 0:
            spot = random.choice(possible_spots)
            self.fix_position(spot, player)

    def get_random_first_player(self):
        return random.randint(0, 1)

    def show_board(self):
        print()
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def start_against_random(self):
        self.create_board()
        player = 'X' if self.get_random_first_player() == 1 else 'O'

        while True:
            if player == 'X':
                self.random_player(self.board, player)
            else:
                try:
                    move=self.a_star_search(self.board, player)
                    self.fix_position(move, player)
                except:
                    self.random_player(self.board, player)

            if self.is_player_win(self.board, player):
                if player == 'X':
                    return -1
                else:
                    return 1

            if self.is_board_filled(self.board):
                print('draw')
                return 0

            player = 'O' if player == 'X' else 'X'

    def start(self):
        self.create_board()
        player = 'X' if self.get_random_first_player() == 1 else 'O'
        while True:
            if player == 'X':
                print(f"Player {player} turn")
                move = self.a_star_search(self.board, player)
                self.fix_position(move, player)
                self.show_board()
                print('Computer has made a move!')
            else:
                all_visited = self.get_visited(self.board, player)[0]
                print(f"Player {player} turn")
                self.show_board()
                spot = None
                while spot is None:
                    spot = self.human_player(all_visited)
                self.fix_position(spot, player)

            if self.is_player_win(self.board, player):
                print(f"Player {player} wins the game!")
                break
            if self.is_board_filled(self.board):
                print("Match Draw!")
                break

            print()
            self.show_board()

            player = 'X' if player == 'O' else 'O'

    def human_player(self, all_visited):
        while True:
            spot = input(
                'Enter a spot (first row: a, b, c; columns: 1, 2, 3): ')
            if spot in list(TTT_graph.keys()):
                if spot not in all_visited:
                    return spot
                else:
                    print('Enter a valid and unoccupied spot!')
                    print(all_visited)
            else:
                print('Enter a valid and unoccupied spot!')
                print(all_visited)

def test():
    samples = 5
    summation_score_per_gameplay = 0
    for _ in range(samples):
        score = 0
        game_plays = 100
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

# # use below code if you want to play against computer
# game = TicTacToe()
# game.start()
