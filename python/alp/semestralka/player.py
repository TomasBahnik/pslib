import time

import alp.semestralka.base as base
from alp.semestralka.draw import Drawer
from draft.cv08.hw_08_light import CELL_COLUMN, \
    CELL_ROW, EMPTY_CELL_COLOR, move_cells_top_left, rotate_cells_90, rotate_cells_180, rotate_cells_270
from draft.shared.matrices import column

FIRST_FREE_STONE_SCORE = 'first_free_stone_score'


class Player(base.BasePlayer):
    def __init__(self, name, board, marks, stones, player):
        """ constructor of Player. Place you variables here with prefix 'self' -> e.g. 'self.myVariable' """

        base.BasePlayer.__init__(self, name, board, marks, stones, player)  # do not change this line!!
        self.algorithm = FIRST_FREE_STONE_SCORE  # name of your method. Will be used in tournament mode

    def moveStone(self, stone, row_col):
        # stone = [[row1, col1], ... [rown, coln]]
        # row, col = int
        # create new stone, place it to row, col
        newStone = []
        for cell in stone:
            rowCell, colCell = cell
            newRow = rowCell + row_col[0]
            newCol = colCell + row_col[1]
            newStone.append([newRow, newCol])
        return newStone

    # snaží se je co nejvíc uchránit svoje znacky a
    # naopak se snaží pokrýt soupeřovy značky
    def stone_score(self, new_stone):
        """ count the number of open pieces for player (=1 or -1)
            self.score(self.player) -> counts YOUR score (the number of your open marks)
            self.score(-self.player) -> counts OPPONENT's score (the number of his/her open marks)
        """
        opponent_marks = 0  # maximize
        my_marks = 0  # keep uncovered but put the stone in such a way that they can't be covered
        for cell in new_stone:
            r, c = cell
            if self.board[r][c] != 0:  # should not happen at this moment
                print("ERROR invalid placement")
                return -1
            if self.marks[r][c] == -self.player:
                opponent_marks += 1
            if self.marks[r][c] == self.player:
                my_marks += 1
        return [my_marks, opponent_marks, new_stone]

    def canBePlaced(self, a_stone, stone_color):
        # stone = [[row, col], ... [row, col]]
        for cell in a_stone:
            row, col = cell
            # true if all stone cells are inside the board and cells in board are free i.e. contain 0
            if self.inBoard(row, col) and self.board[row][col] == 0:
                pass
            else:
                return False
        if not self.has_correct_side(a_stone, stone_color):
            return False
        return True

    def all_stone_scores(self):
        all_scores = []  # store scores to find the best next placement
        for stone_idx in range(len(self.freeStones)):
            if self.freeStones[stone_idx] is True:
                stone_color, the_stone = self.stones[stone_idx]  # new local variables are created
                single_move = self.single_move(the_stone, stone_color)
                if len(single_move) > 0:
                    all_scores.append([stone_idx, single_move])
        return all_scores

    def first_free_stone_scores(self):
        stone_idx = self.freeStones.index(True)
        stone_color, the_stone = self.stones[stone_idx]  # new local variables are created
        single_move = self.single_move(the_stone, stone_color)
        if len(single_move) > 0:
            return [stone_idx, single_move]
        return []

    def move(self):
        """ return [ stoneIdx, [ stonePosition] ]
            stoneIdx .. integer .. index of stone to self.freeStones
            [stonePosition] = [ [row1,col1] ... [rown, coln] ] .. position into board where stone is placed

            if no stone can be placed:
            return []
        """
        t0 = time.perf_counter()
        scores = self.first_free_stone_scores() if self.algorithm == FIRST_FREE_STONE_SCORE else self.all_stone_scores()
        duration = time.perf_counter() - t0
        print("{} : scores calculation duration = {} sec".format(self.name, duration))
        if len(scores) > 0:
            if self.algorithm == FIRST_FREE_STONE_SCORE:
                return self.get_best_move(scores)
            else:
                # TODO review and optimize way for best move from all scores
                #  this must win but not
                # stone_indexes = column(scores, 0)
                stone_scores = column(scores, 1)
                x = column(stone_scores, 0)
                opp_marks = column(x, 1)
                max_opp_marks = max(opp_marks)
                max_opp_mark_idx = opp_marks.index(max_opp_marks)
                print("{} : all_free_stones : Max opponent marks = {}".format(self.name, max_opp_marks))
                return self.get_best_move(scores[max_opp_mark_idx])
        return []

    def get_best_move(self, stone_score):
        """ Structure of stone score
            [0] ... stone index
            [1] ... [my_marks, opponent_marks] covered marks , my covered marks are always 0 => might be removed
            [2] ... new stone position
        """
        idx = stone_score[0]
        score = stone_score[1]
        # opponent marks covered by move
        opp_marks = column(score, 1)
        max_opp_marks = max(opp_marks)
        print("{} : get_best_move : Max opponent marks = {}".format(self.name, max_opp_marks))
        max_opp_mark_idx = opp_marks.index(max_opp_marks)
        # simple criteria :  best move = the one which covers most of opponent marks
        best_move = score[max_opp_mark_idx][2]
        return [idx, best_move]

    def single_move(self, a_stone, stone_color):
        stone_scores = []  # store scores to find the best next placement
        a_stone = move_cells_top_left(a_stone)
        rotated_stones = [a_stone, rotate_cells_90(a_stone), rotate_cells_180(a_stone), rotate_cells_270(a_stone)]
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                for r_s in rotated_stones:  # check all rotations which is best one
                    moveStone = self.moveStone(r_s, [row, col])
                    if self.canBePlaced(moveStone, stone_color):
                        stone_score = self.stone_score(moveStone)
                        my_marks = stone_score[0]  # do not cover my own marks!
                        if my_marks == 0:
                            stone_scores.append(stone_score)
        if len(stone_scores) > 0:
            return stone_scores
        return []

    def check_surrounding(self, cell, stone):
        if cell in stone:
            return None
        else:
            return self.board[cell[0]][cell[1]] if self.inBoard(cell[0], cell[1]) else None

    def stone_surroundings(self, stone, stone_color):
        surrounding = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                for cell in stone:
                    row = cell[CELL_ROW] + r
                    col = cell[CELL_COLUMN] + c
                    cell = [row, col]
                    cell_color = self.check_surrounding(cell, stone)
                    # no cells outside board no empty cells and no duplicates
                    if cell_color is not None and cell_color != EMPTY_CELL_COLOR and cell not in column(surrounding, 0):
                        color_ratio = cell_color / stone_color
                        surrounding += [[cell, cell_color, color_ratio]]
        return surrounding

    # TODO review
    #  len < 2 dava max 1 spolecnou hranu
    #  len < 3 vybira lepsi pozice dovoli 2 spolecne hrany ale NESMI dovolit
    #  aby 2 *sousedni* bunky mely spolecne hrany na *stejne* strane <= hlavni kriretium - soucin = 0 ?
    def check_square(self, stone, stone_color):
        # tmp_board = copy.deepcopy(self.board)
        cell_has_two_neighbour = []
        # put temporarily stone on board. It is guaranteed that the cells are empty
        # creating a deep copy takes ~ 0.2 sec
        base.writeBoard(self.board, stone, stone_color)
        for cell in stone:
            r, c = cell
            x = r
            y = c - 1
            left = self.board[x][y] if self.inBoard(x, y) else 0
            x = r - 1
            y = c - 1
            left_top = self.board[x][y] if self.inBoard(x, y) else 0
            x = r - 1
            y = c
            top = self.board[x][y] if self.inBoard(x, y) else 0
            x = r - 1
            y = c + 1
            right_top = self.board[x][y] if self.inBoard(x, y) else 0
            x = r
            y = c + 1
            right = self.board[x][y] if self.inBoard(x, y) else 0
            x = r + 1
            y = c + 1
            right_bottom = self.board[x][y] if self.inBoard(x, y) else 0
            x = r + 1
            y = c
            bottom = self.board[x][y] if self.inBoard(x, y) else 0
            x = r + 1
            y = c - 1
            bottom_left = self.board[x][y] if self.inBoard(x, y) else 0
            # all must be true
            a = left * left_top * top == 0
            b = top * right_top * right == 0
            c = right * right_bottom * bottom == 0
            d = bottom * bottom_left * left == 0
            cell_has_two_neighbour += [a and b and c and d]
        square = [x for x in cell_has_two_neighbour if x is False]
        # delete stone
        base.writeBoard(self.board, stone, EMPTY_CELL_COLOR)
        return len(square) == 0  # no False => no square

    # kameny nesmí přečnívat z desky, nebo zakrývat (ani částečně) již položené kameny
    # nově položený kamen se musí dotýkat alespoň jednou hranou některého z již položených kamenů
    # kameny stejné barvy se nikdy nesmějí dotýkat hranou (kameny různých barev se mohou dotýkat)
    # nesmi vzniknout zcela pokryta bunka 2x2
    # color > 0 we can divide
    def has_correct_side(self, stone, stone_color):
        # might be used for optimizing position based on marks
        surroundings = self.stone_surroundings(stone, stone_color)
        color_ratios = column(surroundings, 2)
        # must be zero
        same_color_cnt = len([x for x in color_ratios if x == 1])
        # no limit but can used for existence of 2x2 cells
        diff_color_cnt = len([x for x in color_ratios if x != 1 and x != EMPTY_CELL_COLOR])
        # must be >= 1
        empty_color_cnt = len([x for x in color_ratios if x == EMPTY_CELL_COLOR])
        no_square = self.check_square(stone, stone_color)
        return same_color_cnt == 0 and no_square


# the following if/else is simplified. On Brute, we will check if return value
# from move() is valid ...
def is_move_valid(player, move):
    # use player board to check
    # player_sign = player.player
    # player_board = player.board
    # any(player_sign in x for x in player_board)
    return len(move) != 0


if __name__ == "__main__":

    # load stones from file
    stones = base.loadStones("stones.txt")
    print("stones are", stones)

    # prepare board and marks
    board, marks = base.makeBoard10()

    # create both players
    p1 = Player("pepa", board, marks, stones, 1)
    p1.algorithm = 'none'
    p2 = Player("franta", board, marks, stones, -1)
    p2.algorithm = FIRST_FREE_STONE_SCORE

    # not necessary, only if you want to draw board to png files
    d = Drawer()
    d.draw(p1.board, p1.marks, "init.png")

    moveidx = 0
    while True:
        p1play = True
        p2play = True

        move = p1.move()  # first player, we assume that a corrent output is returned

        # the following if/else is simplified. On Brute, we will check if return value
        # from move() is valid ...
        if not is_move_valid(p1, move):
            p1play = False
        else:
            stoneIdx, stone = move
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)  # write stone to player1's board
            base.writeBoard(p2.board, stone, stoneColor)  # write stone to player2's board
            p1.freeStones[stoneIdx] = False  # tell player1 which stone is used
            p2.freeStones[stoneIdx] = False  # tell player2 which stone is used
        if p1play:  # draw only if played
            d.draw(p2.board, p2.marks, "move-{:02d}a.png".format(moveidx))  # draw to png

        # now we call player2 and update boards/freeStones of both players
        move = p2.move()
        if not is_move_valid(p2, move):
            p2play = False
        else:
            stoneIdx, stone = move
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)
            base.writeBoard(p2.board, stone, stoneColor)
            p1.freeStones[stoneIdx] = False
            p2.freeStones[stoneIdx] = False

        if p2play:
            d.draw(p1.board, p1.marks, "move-{:02d}b.png".format(moveidx))

        # if both players return [] from move, the game ends
        if p1play is False and p2play is False:
            print("end of game")
            break

        moveidx += 1
        print(" -- end of move ", moveidx, " score is ", p1.score(p1.player), p1.score(-p1.player))
