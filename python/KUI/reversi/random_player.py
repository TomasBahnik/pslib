import random
from collections import namedtuple

import numpy as np

import player

EMPTY_MARK = -1

infinity = np.inf
GameState = namedtuple('GameState', 'utility, board, moves')


# TODO  must use only game board
# player move function is called in headless_reversi_creator.py as
# move = self.current_player.move(self.board.get_board_copy())
# i.e with deep copy of current board initialized as
# self.board = GameBoard(board_size, player1_color, player2_color)
# def utility(self, state, player): is defined as
# def utility(self, board, player):
#     """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
#     return board.utility if player == 'X' else -board.utility

def minimax_search(game, state):
    """
    Search game tree to determine best move; return (value, move) pair.
    Where `value` is the utility that the algorithm computes for the player whose turn it is to move
    and `move` is the move itself
    """

    player = state.to_move

    def max_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)


class MyPlayer(player.MyPlayer):
    def __init__(self, my_color, opponent_color, board_size=8):
        super().__init__(my_color, opponent_color, board_size)
        self.name = 'RANDOM'
        self.board_size = board_size
        self.state = GameState(utility=0, board=[], moves=[])

    # the only function with access to board
    def move(self, board):
        game = np.array(board, dtype=int)
        stones_cnt = np.count_nonzero(game != EMPTY_MARK)
        empty_cnt = np.count_nonzero(game == EMPTY_MARK) # can be counted as size of board - stones_cnt
        my_color_cnt = np.count_nonzero(game == self.my_color)
        opp_color_cnt = np.count_nonzero(game == self.opponent_color)
        moves = self.get_all_valid_moves(board)
        # main function to implement
        move = random.choice(moves) if len(moves) > 0 else None
        utility = self.compute_utility(board, move)
        self.state = GameState(utility=utility, board=board, moves=moves)
        return move

    def actions(self):
        """Legal moves are any square not yet taken."""
        return self.state.moves

    # TODO board is updated by game controller after move
    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        utility = self.compute_utility(board, move)
        return GameState(utility=utility, board=board, moves=moves)

    def utility(self, state, player_color):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player_color == self.my_color else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def compute_utility(self, board, move):
        return len(self.state.moves)
