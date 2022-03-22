import copy
import random
from collections import namedtuple

import numpy as np

EMPTY_MARK = -1

infinity = np.inf
GameState = namedtuple('GameState', 'to_move, utility, board, moves')


def random_player(state, game):
    moves = game.actions(state)
    return random.choice(moves) if len(moves) > 0 else None


def max_utility(state, game):
    return max(game.actions(state), key=lambda move: game.result(state, move).utility)


def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """
    Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    """

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
    eval_fn = eval_fn or (lambda state: game.utility(state))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)


def monte_carlo_tree_search(state, game, N=10, d=4, cutoff_test=None, eval_fn=None):
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not game.terminal_test(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state, depth):
        """simulate the utility of current state by random picking a step"""
        player = game.to_move(state)
        while not cutoff_test(state, depth):
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
            depth += 1
        v = eval_fn(state)
        return -v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)

    root = MCT_Node(state=state)
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state))

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state, 1)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    return root.children.get(max_state)


def change_stones_in_direction(board, move, dx, dy, player_color):
    posx = move[0] + dx
    posy = move[1] + dy
    while not (board[posx][posy] == player_color):
        board[posx][posy] = player_color
        posx += dx
        posy += dy


class MyPlayer:
    """Player for reversi game based on model used in AIMA book"""

    def __init__(self, my_color, opponent_color, board_size=8):
        self.name = 'bahnitom'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    # the only function with access to board
    def move(self, board):
        game_state = GameState(to_move=self.my_color, utility=-infinity, board=board, moves=[])
        move = monte_carlo_tree_search(game_state, self, 200, 10)
        # move = alpha_beta_cutoff_search(game_state, self, d=3)
        # move = random_player(game_state, self)
        # move = max_utility(game_state, self)
        return move

    def actions(self, state):
        ret_val = self.get_all_valid_moves(state.board, state.to_move)
        return ret_val

    def result(self, state, move):
        board = state.board
        board_tmp = copy.deepcopy(board)
        self.play_move(board_tmp, move, state.to_move)
        # utility for ME
        utility = self.compute_utility(board_tmp)
        # exchange players
        to_move = self.opponent_color if state.to_move == self.my_color else self.my_color
        # moves of the changed player
        moves = self.get_all_valid_moves(board_tmp, to_move)
        return GameState(to_move=to_move, utility=utility, board=board_tmp, moves=moves)

    def utility(self, state):
        return state.utility

    def terminal_test(self, state):
        """
        A state is terminal if there are no moves.
        self.get_all_valid_moves return always array not None
        """
        actions = self.actions(state)
        ret_val = len(actions) == 0
        return ret_val

    def compute_utility(self, board_tmp):
        board_np = np.array(board_tmp, dtype=int)
        my_color_cnt = np.count_nonzero(board_np == self.my_color)
        opp_color_cnt = np.count_nonzero(board_np == self.opponent_color)
        # utility from MY POV
        cnt = my_color_cnt - opp_color_cnt
        return cnt

    def play_move(self, board, move, player_color):
        board[move[0]][move[1]] = player_color
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.confirm_direction(board, move, dx[i], dy[i], player_color):
                change_stones_in_direction(board, move, dx[i], dy[i], player_color)

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

    def __is_correct_move(self, move, board, player):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.confirm_direction(board, move, dx[i], dy[i], player):
                return True
        return False

    def get_all_valid_moves(self, board, player):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board, player):
                    valid_moves.append((x, y))

        if len(valid_moves) <= 0:
            print('No possible move!')
            return []
        return valid_moves
