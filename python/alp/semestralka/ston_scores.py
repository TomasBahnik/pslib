from draft.shared.matrices import column


class StoneScore:
    def __init__(self, stone_scores):
        self.stone_scores = stone_scores

    def idx(self):
        return self.stone_scores[0]

    def score(self):
        return self.stone_scores[1]

    def opp_marks(self):
        return column(self.score(), 1)

    def max_opp_marks(self):
        return max(self.opp_marks())

    def max_opp_mark_idx(self):
        return self.opp_marks().index(self.max_opp_marks())

    def best_move(self):
        return self.score()[self.max_opp_mark_idx()][2]

    def result(self):
        return [self.idx(), self.best_move()]
