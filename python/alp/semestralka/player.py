import alp.semestralka.base as base

from alp.semestralka.draw import Drawer

from draft.cv08.hw_08_light import CELL_COLUMN, \
    CELL_ROW, EMPTY_CELL_COLOR, move_cells_top_left, rotate_cells_90, rotate_cells_180, rotate_cells_270

from draft.shared.matrices import column


class Player(base.BasePlayer):
    def __init__(self, name, board, marks, stones, player):
        """ constructor of Player. Place you variables here with prefix 'self' -> e.g. 'self.myVariable' """

        base.BasePlayer.__init__(self, name, board, marks, stones, player)  # do not change this line!!
        self.algorithm = "my great method"  # name of your method. Will be used in tournament mode

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

    # TODO maximize player.score function
    def canBePlaced(self, stone, stoneColor):
        # stone = [[row, col], ... [row, col]]
        for cell in stone:
            row, col = cell
            # true if all stone cells are inside the board and cells in board are free i.e. contain 0
            if self.inBoard(row, col) and self.board[row][col] == 0:
                pass
            else:
                return False
        if not self.has_correct_side(stone, stoneColor):
            return False
        return True

    def move(self):
        """ return [ stoneIdx, [ stonePosition] ]
            stoneIdx .. integer .. index of stone to self.freeStones
            [stonePosition] = [ [row1,col1] ... [rown, coln] ] .. position into board where stone is placed

            if no stone can be placed:
            return []
        """
        try:
            stoneIdx = self.freeStones.index(True)
            stoneColor, stone = self.stones[stoneIdx]  # new local variables are created
        except ValueError as ve:  # in case when there is no stone left i.e. index returns None
            return []

        # here new local variable stone is used and might be assigned
        # do not use in/out variables anyway
        new_scores = []  # store scores to find the best next placement
        stone = move_cells_top_left(stone)
        rotated_stones = [stone, rotate_cells_90(stone), rotate_cells_180(stone), rotate_cells_270(stone)]
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                for r_s in rotated_stones:  # check all rotations which is best one
                    moveStone = self.moveStone(r_s, [row, col])
                    if self.canBePlaced(moveStone, stoneColor):
                        new_scores.append(self.stone_score(moveStone))
        if len(new_scores) > 0:
            opp_marks = column(new_scores, 1)
            max_opp_mark_idx = opp_marks.index(max(opp_marks))
            best_move = new_scores[max_opp_mark_idx][2]
            return [stoneIdx, best_move]

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
                    # TODO filter in list comprehension
                    if cell_color is not None and cell_color != EMPTY_CELL_COLOR and cell not in column(surrounding, 0):
                        color_ratio = cell_color / stone_color
                        surrounding += [[cell, cell_color, color_ratio]]
        return surrounding

    def check_square(self, surround, stone):
        f_c = column(surround, 0)
        next_cell_filled = []
        for cell in stone:
            r, c = cell
            n = [r + 1, c] in f_c or [r, c + 1] in f_c or [r - 1, c] in f_c or [r, c - 1] in f_c
            next_cell_filled += [n]
        return [x for x in next_cell_filled if x is True]

    # kameny nesmí přečnívat z desky, nebo zakrývat (ani částečně) již položené kameny
    # nově položený kamen se musí dotýkat alespoň jednou hranou některého z již položených kamenů
    # kameny stejné barvy se nikdy nesmějí dotýkat hranou (kameny různých barev se mohou dotýkat)
    # nesmi vzniknout zcela pokryta bunka 2x2
    # color > 0 we can divide
    def has_correct_side(self, stone, stone_color):
        surroundings = self.stone_surroundings(stone, stone_color)
        colors = column(surroundings, 1)
        color_ratios = column(surroundings, 2)
        # must be zero
        same_color_cnt = len([x for x in color_ratios if x == 1])
        # no limit but can used for existence of 2x2 cells
        diff_color_cnt = len([x for x in color_ratios if x != 1 and x != EMPTY_CELL_COLOR])
        # must be >= 1
        empty_color_cnt = len([x for x in color_ratios if x == EMPTY_CELL_COLOR])
        m = self.check_square(surroundings, stone)
        return same_color_cnt == 0 and len(m) < 2


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
    p2 = Player("franta", board, marks, stones, -1)

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
