import numpy as np

import player


class MyPlayer(player.MyPlayer):
    def __init__(self, my_color, opponent_color, board_size=8):
        super().__init__(my_color, opponent_color, board_size)

    def move(self, board):
        game_state = player.GameState(to_move=self.my_color, utility=-np.inf, board=board, moves=[])
        return player.max_utility(game_state, self)
