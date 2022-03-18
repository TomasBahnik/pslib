import random

import player


class MyPlayer(player.MyPlayer):
    def __init__(self, my_color, opponent_color, board_size=8):
        super().__init__(my_color, opponent_color, board_size)

    def move(self, board):
        moves = self.get_all_valid_moves(board)
        return random.choice(moves) if len(moves) > 0 else None
        # return moves[0] if len(moves) > 0 else None
