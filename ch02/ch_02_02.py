"""S.O.L.I.D Design.

Chapter 2, ISP. Part 2.
"""
import random
from ch02.ch_02_01 import BlackjackCard, BlackjackAceCard, BlackjackFaceCard
from ch02.ch_02_01 import CribbageCard, CribbageFaceCard, CribbageNobsCard

class DeckX(list):
    pass

class CribbageDeck(DeckX):
    def cut(self, depth):
        reveal = self.pop(depth)
        self.insert(0, reveal)

def deck_builder(card_factory, n=1):
    return  [card_factory(rank, suit)
        for rank in range(1,14)
            for suit in (u'\u2660', u'\u2661', u'\u2662', u'\u2663')
                for _ in range(n)]

def card_factory(rank,suit):
    """A metaphorical superclass for various card factory functions."""
    pass

def blackjack_card_factory(rank, suit):
    if 1 == rank: return BlackjackAceCard(rank, suit)
    elif 2 <= rank < 11: return BlackjackCard(rank, suit)
    else: return BlackjackFaceCard(rank, suit)

def cribbage_card_factory(rank, suit):
    if rank == 11: return CribbageNobsCard(rank, suit)
    elif rank in (12, 13): return CribbageFaceCard(rank, suit)
    else: return CribbageCard(rank, suit)


__test__ = {
    'DeckBuilder': '''
>>> random.seed(1) # Deterministic Sequence
>>> deck = deck_builder(blackjack_card_factory)
>>> random.shuffle(deck)
>>> dealer = iter(deck)
>>> hand = [next(dealer) for _ in range(5)]
>>> [str(c) for c in hand]
[' K♡', ' 3♡', '10♡', ' 6♢', ' A♢']
>>> sum(c.hard() for c in hand)
30
>>> sum(c.soft() for c in hand)
40
''',

    'DeckBuilder_Cribbage': '''
>>> random.seed(1) # Deterministic Sequence
>>> deck = deck_builder(cribbage_card_factory)
>>> random.shuffle(deck)
>>> dealer = iter(deck)
>>> hand = [next(dealer) for _ in range(5)]
>>> [str(c) for c in hand]
['13♡', ' 3♡', '10♡', ' 6♢', ' 1♢']
>>> sum(c.points() for c in hand)
30
>>> [c.his_heels() for c in hand]
[False, False, False, False, False]
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
