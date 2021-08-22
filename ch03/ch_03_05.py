"""S.O.L.I.D Design.

Chapter 3, LSP. Part 5.
"""
from ch02.ch_02_01 import Card

class Hand1(list):
    def append(self, card):
        assert isinstance(card, Card)
        super().append(card)

class Hand2(list):
    def append(self, card: Card):
        super().append(card)

class CardCmp:
    def __init__(self, rank, suit):
        self.rank= rank
        self.suit= suit
    def __eq__(self, other):
        if isinstance(other, CardCmp):
            return self.rank == other.rank
        elif isinstance(other, int):
            return self.rank == other
        else:
            raise TypeError

__test__ = {

    'Card Comparison': '''
>>> c1 = CardCmp(12, '♡')
>>> c2 = CardCmp(2, '♡')
>>> c3 = CardCmp(12, '♢')
>>> c1 == c2
False
>>> c1 == c3
True
>>> c1 == 12
True
>>> c1 == 13
False
'''
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
