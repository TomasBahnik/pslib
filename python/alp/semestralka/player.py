import sys
import random
import copy
import alp.semestralka.base as base

from alp.semestralka.draw import Drawer


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

    def canBePlaced(self, stone):
        # stone = [[row, col], ... [row, col]]
        # true if all [row, cal] inside board and all row, col are free
        for cell in stone:
            row, col = cell
            if not (self.inBoard(row, col) and self.board[row][col] == 0):
                pass
            else:
                return False
        return True

    def move(self):
        """ return [ stoneIdx, [ stonePosition] ]
            stoneIdx .. integer .. index of stone to self.freeStones
            [stonePosition] = [ [row1,col1] ... [rown, coln] ] .. position into board where stone is placed

            if no stone can be placed:
            return []
        """
        stoneIdx = 4
        stoneColor, stone = self.stones[stoneIdx]

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                moveStone = self.moveStone(stone, [row, col])
                if self.canBePlaced(moveStone):
                    return [stoneIdx, moveStone]

        return []


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
    d.draw(p1.board, p1.marks, "init.png");

    moveidx = 0
    while True:
        p1play = True
        p2play = True

        move_ret_val = p1.move()  # first player, we assume that a corrent output is returned

        # the following if/else is simplified. On Brute, we will check if return value
        # from move() is valid ...
        if len(move_ret_val) == 0:
            p1play = False
        else:
            stoneIdx, stone = move_ret_val
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)  # write stone to player1's board
            base.writeBoard(p2.board, stone, stoneColor)  # write stone to player2's board
            p1.freeStones[stoneIdx] = False  # tell player1 which stone is used
            p2.freeStones[stoneIdx] = False  # tell player2 which stone is used

        d.draw(p2.board, p2.marks, "move-{:02d}a.png".format(moveidx))  # draw to png

        # now we call player2 and update boards/freeStones of both players
        move_ret_val = p2.move()
        if len(move_ret_val) == 0:
            p2play = False
        else:
            stoneIdx, stone = move_ret_val
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)
            base.writeBoard(p2.board, stone, stoneColor)
            p1.freeStones[stoneIdx] = False
            p2.freeStones[stoneIdx] = False

        d.draw(p1.board, p1.marks, "move-{:02d}b.png".format(moveidx))

        # if both players return [] from move, the game ends
        if p1play == False and p2play == False:
            print("end of game")
            break

        moveidx += 1
        print(" -- end of move ", moveidx, " score is ", p1.score(p1.player), p1.score(-p1.player))
