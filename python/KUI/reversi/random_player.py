import copy
from collections import namedtuple

import numpy as np

import player

EMPTY_MARK = -1

infinity = np.inf
GameState = namedtuple('GameState', 'to_move, utility, board, moves')


def minmax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    # player color = 0, -1
    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


class MyPlayer(player.MyPlayer):
    def __init__(self, my_color, opponent_color, board_size=8):
        super().__init__(my_color, opponent_color, board_size)
        self.name = 'RANDOM'
        self.board_size = board_size
        self.state = GameState(to_move=my_color, utility=0, board=[], moves=[])

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    # the only function with access to board
    def move(self, board):
        board_tmp = copy.deepcopy(board)
        moves = self.get_all_valid_moves(board_tmp)
        # main function to implement
        # move = random.choice(moves) if len(moves) > 0 else None
        # TODO utility is set to 0 ?? new GameState is returned from results
        self.state = GameState(to_move=self.my_color, utility=0, board=board_tmp, moves=moves)
        move = minmax_decision(self.state, self)
        utility = self.compute_utility(board_tmp, move, self.my_color)
        self.state = GameState(to_move=self.my_color, utility=utility, board=board_tmp, moves=moves)
        return move

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        ret_val = self.get_all_valid_moves(state.board)
        return ret_val

    # TODO board is updated by game controller after move
    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board
        # board[move] = state.to_move
        moves = self.get_all_valid_moves(board)
        utility = self.compute_utility(board, move, state.to_move)
        to_move = self.opponent_color if state.to_move == self.my_color else self.my_color
        return GameState(to_move=to_move, utility=utility, board=board, moves=moves)

    def utility(self, state, player_color):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player_color == self.my_color else -state.utility

    def terminal_test(self, state):
        """A state is terminal if there are no moves??."""
        actions = self.actions(state)
        ret_val = True if actions is None else False
        return ret_val

    def compute_utility(self, board, move, player_color):
        # b = copy.deepcopy(board)
        if self.__is_correct_move(move, board):
            board[move[0]][move[1]] = self.my_color
            dx = [-1, -1, -1, 0, 1, 1, 1, 0]
            dy = [-1, 0, 1, 1, 1, 0, -1, -1]
            for i in range(len(dx)):
                if self.__confirm_direction(move, dx[i], dy[i], board)[0]:
                    player.change_stones_in_direction(board, move, dx[i], dy[i], self.my_color)
            board_np = np.array(board, dtype=int)
            my_color_cnt = np.count_nonzero(board_np == self.my_color)
            opp_color_cnt = np.count_nonzero(board_np == self.opponent_color)
            cnt = my_color_cnt - opp_color_cnt
            return cnt if player_color == self.my_color else -cnt
        return 0
