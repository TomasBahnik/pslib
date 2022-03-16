import random

import math

import player

infinity = math.inf


# TODO  must use only game board
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

    def move(self, board):
        moves = self.get_all_valid_moves(board)
        return random.choice(moves) if len(moves) > 0 else None
