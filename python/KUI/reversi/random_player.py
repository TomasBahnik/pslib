import copy
from collections import namedtuple

import numpy as np

import player

EMPTY_MARK = -1

infinity = np.inf
GameState = namedtuple('GameState', 'to_move, utility, board, moves')


def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


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
        self.state = GameState(to_move=self.my_color, utility=0, board=board_tmp, moves=moves)
        move = alpha_beta_cutoff_search(self.state, self, d=2)
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
        if self.__is_correct_move(move, board):
            self.play_move(board, move, player_color)
            board_np = np.array(board, dtype=int)
            my_color_cnt = np.count_nonzero(board_np == self.my_color)
            opp_color_cnt = np.count_nonzero(board_np == self.opponent_color)
            cnt = my_color_cnt - opp_color_cnt
            return cnt if player_color == self.my_color else -cnt
        return 0

    def play_move(self, board, move, player_color):
        board[move[0]][move[1]] = player_color
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.confirm_direction(board, move, dx[i], dy[i], player_color):
                player.change_stones_in_direction(board, move, dx[i], dy[i], player_color)

    def confirm_direction(self, board, move, dx, dy, player_color):
        if player_color == self.my_color:
            opponents_color = self.opponent_color
        else:
            opponents_color = self.my_color
        posx = move[0] + dx
        posy = move[1] + dy
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] == opponents_color:
                while (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == EMPTY_MARK:
                            return False
                        if board[posx][posy] == player_color:
                            return True
        return False
