import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def spades_high(self,card: Card):
        rank_value = self.ranks.index(card.rank)
        # for new rank_value reserve slot of length=len(self.suit_values)
        ret = rank_value * len(self.suit_values) + self.suit_values[card.suit]
        return ret


def main():
    deck = FrenchDeck()
    print(len(deck))
    for card in sorted(deck, key=deck.spades_high):
        print(f"{card}: high={deck.spades_high(card)}")

if __name__ == "__main__":
    main()
