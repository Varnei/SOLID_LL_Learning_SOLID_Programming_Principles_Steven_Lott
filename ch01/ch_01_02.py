"""S.O.L.I.D Design.

Chapter 1, Introduction. Part 2.
"""

import random

class Card:
    def __init__(self):
        self.cards = [ (rank, suit) for rank in range(1,14)
            for suit in '♠♡♢♣' ]
        random.shuffle(self.cards)
    def deal(self):
        return self.cards.pop()
    def points(self, card):
        rank, suit = card
        if rank == 1: return (1,11)
        elif 2 <= rank < 11: return (rank, rank)
        else: return (10,10)

class Shoe(Card):
    def __init__(self, n):
        super().__init__()
        self.shoe = []
        for _ in range(n): self.shoe.extend(self.cards)
        random.shuffle(self.shoe)
    def shuffle_burn(self, n=100):
        random.shuffle(self.shoe)
        self.shoe = self.shoe[n:]
    def deal(self):
        return self.shoe.pop()

__test__ = {
    'Card': '''
>>> random.seed(1) # Deterministic Sequence
>>> deck = Card()
>>> c1 = deck.deal()
>>> c1
(3, '♠')
>>> hand = [deck.deal() for _ in range(5)]
>>> hand
[(10, '♠'), (13, '♠'), (2, '♠'), (5, '♠'), (2, '♣')]

# Awkward totalling
>>> hand2 = [(11, '♠'), (1, '♠')]
>>> sum(deck.points(c)[0] for c in hand2)
11
>>> sum(deck.points(c)[1] for c in hand2)
21
''',

    'Shoe': '''
>>> deck = Shoe(6)
>>> random.seed(1) # Deterministic Sequence
>>> deck.shuffle_burn(100)
>>> hand = [deck.deal() for _ in range(5)]
>>> hand
[(12, '♣'), (10, '♡'), (7, '♢'), (9, '♢'), (4, '♣')]
>>> dealing= True
>>> while dealing:
...     try:
...        hand = [deck.deal() for _ in range(5)]
...        eq = any( hand[c1] == hand[c2]
...           for c1 in range(len(hand)) for c2 in range(len(hand)) if c1 != c2)
...        if eq: print(hand)
...     except IndexError:
...        dealing= False
...
[(6, '♢'), (5, '♡'), (6, '♢'), (13, '♡'), (9, '♡')]
[(3, '♢'), (9, '♠'), (6, '♡'), (2, '♢'), (9, '♠')]
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
