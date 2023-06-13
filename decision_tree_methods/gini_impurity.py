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
        return False

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

    def is_board_filled(self, board):
        for row in board:
            if '-' in row:
                return False
        return True

    def transform_to_index(self, spot):
        x_coord = spot_legend[spot[0]]
        y_coord = int(spot[1]) - 1
        return x_coord, y_coord

    def get_visited(self, computer_player):
        visited = []
        computer_visited = []
        for row in range(3):
            for col in range(3):
                index = self.board[row][col]
                if index != '-':
                    letter = chr(row + 97)
                    col += 1
                    spot = f"{letter}{col}"
                    visited.append(spot)
                    if index == computer_player:
                        computer_visited.append(spot)
        return visited, computer_visited

    def get_states(self, board, plays, player):
        results = [0, 0, 0]
        temp_board = [row[:] for row in board]
        for play in plays:
            x, y = self.transform_to_index(play)
            if temp_board[x][y] == '-':
                temp_board[x][y] = player
                if self.is_player_win(temp_board, player):
                    results[0] += 0.1 /len(plays)
                if self.is_board_filled(temp_board):
                    results[1] += 0.1 / len(plays)
                player = 'X' if player == 'O' else 'O'

        check_win_board_list = []
        for row in range(3):
            for col in range(3):
                if temp_board[row][col] == '-':
                    check_win_board = [row[:] for row in temp_board]
                    check_win_board[row][col] = player
                    check_win_board_list.append(check_win_board)

        for check_win_board in check_win_board_list:
            for row in range(3):
                for col in range(3):
                    if check_win_board[row][col] == '-':
                        check_win_board[row][col] = player
                        if self.is_player_win(check_win_board, player):
                            results[2] += 0.075 / len(plays)
                        if self.is_board_filled(check_win_board):
                            results[1] += 0.1 / len(plays)
                        temp_board[row][col] = '-'

        return results

    def map_game(self, board, player):
        temp_board = board
        queue = self.get_visited(player)[0]
        temp_visited = self.get_visited(player)[0]
        win_dict = {}

        if len(self.get_visited(player)[1]) == 0:
            for key in TTT_graph.keys():
                if key not in temp_visited:
                    win_dict[key] = self.get_states(temp_board, [key], player)
            return win_dict

        traversal_list = []
        while queue:
            current_node = queue.pop(0)
            for neighbor in TTT_graph[current_node]:
                if neighbor not in temp_visited:
                    win_dict[neighbor] = [0, 0, 0]
                    traversal = [current_node, neighbor]
                    queue.append(neighbor)
                    temp_visited.append(neighbor)
                    traversal_list.append(traversal)

        visited, _ = self.get_visited(player)
        for traversal in traversal_list:
            states = self.get_states(board, traversal, player)
            for key in traversal:
                if key not in visited:
                    for j in range(3):
                        win_dict[key][j] += states[j]

        return win_dict

    def gini_player(self, board, player):
        moves = self.map_game(board, player)
        lowest_gini = float('inf')
        spot = ''
        for key in moves.keys():
            gini_value = 1 - moves[key][0] - moves[key][1] + moves[key][2]
            if gini_value <= lowest_gini:
                lowest_gini = gini_value
                spot = key
        self.fix_position(spot, player)
        return True

    def random_player(self, player):
        temp_player = 'X' if player == 'O' else 'O'
        possible_spots = [spot for spot in TTT_graph.keys() if spot not in self.get_visited(temp_player)[0]]
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
                self.random_player(player)
            else:
                self.gini_player(self.board, player)

            if self.is_player_win(self.board, player):
                if player == 'X':
                    return -1
                else:
                    return 1

            if self.is_board_filled(self.board):
                return 0

            player = 'O' if player == 'X' else 'X'

    def start(self):
        self.create_board()
        player = 'X' if self.get_random_first_player() == 1 else 'O'
        while True:
            if player == 'X':
                print(f"Player {player} turn")
                self.gini_player(self.board, player)
                self.show_board()
                print('Computer has made a move!')
            else:
                temp_player = 'X' if player == 'O' else 'O'
                all_visited = self.get_visited(temp_player)[0]
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
            spot = input('Enter a spot (first row: a, b, c; columns: 1, 2, 3): ')
            if spot in TTT_graph.keys():
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
        game_plays = 1000
        for _ in range(game_plays):
            game = TicTacToe()
            result = game.start_against_random()
            if result == 1 or result == 0:
                score += 1
        summation_score_per_gameplay += score / game_plays
        print(score / game_plays)

    print('The gini agent won, or had a draw ', (summation_score_per_gameplay / samples) * 100,
          '%', 'of times on average')


test()

# game = TicTacToe()
# game.start()
