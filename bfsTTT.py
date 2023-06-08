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

    def get_visited(self, computer_player):
        visited = []
        computer_visited = []
        board = self.board
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

    def get_states(self, board, plays, player):
        temp_plays = plays
        results = [0, 0, 0]
        check_win_board_list = []
        temp_board = [row[:] for row in board]
        while temp_plays:
            play = temp_plays.pop(0)
            index = self.transform_to_index(play)
            if temp_board[index[0]][index[1]] == '-':
                temp_board[index[0]][index[1]] = player
                if self.is_player_win(temp_board, player):
                    results[0] += 1
                if self.is_board_filled(temp_board):
                    results[1] += 1
                # then check all spots other player can make a move at, count number of L/W/D
                player = 'X' if player == 'O' else 'O'
                if len(check_win_board_list) == 0:
                    check_win_board = [row[:] for row in temp_board]
                    for row in range(3):
                        for col in range(3):
                            if temp_board[row][col] == '-':
                                check_win_board[row][col] = player
                                check_win_board_list.append(check_win_board)
                                if self.is_player_win(check_win_board, player):
                                    results[2] += 1
                                if self.is_board_filled(check_win_board):
                                    results[1] += 1
                                check_win_board[row][col] = '-'
                else:
                    for check_win_board in check_win_board_list:
                        for row in range(3):
                            for col in range(3):
                                if check_win_board[row][col] == '-':
                                    check_win_board[row][col] = player
                                    if self.is_player_win(check_win_board, player):
                                        results[2] += 1
                                    if self.is_board_filled(check_win_board):
                                        results[1] += 1
                                    temp_board[row][col] = '-'
                player = 'X' if player == 'O' else 'O'
        return results

    def map_game(self, board, player):
        visited, computer_visited = self.get_visited(player)
        temp_board = board
        queue = computer_visited  # all spots where the computer has made a mark
        temp_visited = visited  # all spots that can't be moved to
        win_dict = {}
        # check first move to be made, must be BFS too, try implementing winning_state for this too
        # use map_game to get winning estimates for each spot
        if len(computer_visited) == 0:
            for key in list(TTT_graph.keys()):
                if key not in visited:
                    win_dict[key] = self.get_states(temp_board, [key], player)
            return win_dict
        while queue:
            first_node = queue[0]
            current_node = queue.pop(0)
            for neighbor in TTT_graph[current_node]:
                if neighbor not in temp_visited:
                    win_dict[neighbor] = [0, 0, 0]
                    # check all the parent nodes if a second layer, see if playing one of those plus this is a win
                    queue.append(neighbor)
                    temp_visited.append(neighbor)
                    if current_node != first_node:
                        states = self.get_states(
                            board, [current_node, neighbor], player)
                        for i in range(2):
                            win_dict[neighbor][i] += states[i]
                            win_dict[current_node][i] += states[i]
                    else:
                        win_dict[neighbor] = self.get_states(
                            board, [neighbor], player)

        return win_dict

    def bfs_player(self, board, player):
        # call map_game and based on its results make move
        moves = self.map_game(board, player)
        # check all possible moves with equivalent win scenarios, choose one with lowest loses
        equivalent_max_win = []
        spot = list(moves.keys())[0]
        max_sum_draw_win = (moves[spot][0] + moves[spot][1])
        for key, value in moves.items():
            if (value[0]+value[1]) > max_sum_draw_win:
                max_sum_draw_win = (value[0]+value[1])
                spot = key
            elif (value[0]+value[1]) == max_sum_draw_win:
                equivalent_max_win.append([key, value])
        if len(equivalent_max_win) > 0 and (equivalent_max_win[0][1][0]+equivalent_max_win[0][1][1]) >= max_sum_draw_win:
            lowest_loses = equivalent_max_win[0][1][2]
            spot = equivalent_max_win[0][0]
            for key, value in equivalent_max_win:
                if value[2] < lowest_loses:
                    lowest_loses = value[2]
                    spot = key

        self.fix_position(spot, player)
        return True

    def random_player(self, player):
        temp_player = 'X' if player == 'O' else 'O'
        possible_spots = [spot for spot in TTT_graph.keys()
                          if spot not in self.get_visited(temp_player)[0]]
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
                self.bfs_player(self.board, player)

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
                self.bfs_player(self.board, player)
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
        game_plays = 1000
        for _ in range(game_plays):
            game = TicTacToe()
            result = game.start_against_random()
            if result == 1 or result == 0:
                score += 1
        summation_score_per_gameplay += score/game_plays
        print(score/game_plays)

    print('The BFS agent won, or had a draw ', (summation_score_per_gameplay/samples)
          * 100, '%', 'of times on average')

# runs 5 different samples each of 1000 games, and returns average win rates of the computer against a random
test()

# use below code if you want to play against computer
game = TicTacToe()
game.start()
