"""S.O.L.I.D Design.

Chapter 3, LSP. Part 3.
"""
import random
from ch02.ch_02_01 import Card, BlackjackAceCard, BlackjackFaceCard, BlackjackCard
from ch02.ch_02_02 import DeckX, deck_builder, blackjack_card_factory
from ch03.ch_03_01 import sort_shuffler
from ch03.ch_03_02 import DeckBuilder

class CribbageCard(Card):
    def points(self):
        return self.rank
    def heels(self):
        return False
    def nobs(self, starter_card):
        return False

class CribbageAceCard(CribbageCard):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._text = 'A'

class CribbageFaceCard(CribbageCard):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._text = {11:'J', 12:'Q', 13:'K'}[self.rank]
    def points(self):
        return 10

class CribbageHeelsCard(CribbageFaceCard):
    def heels(self):
        return True
    def nobs(self, starter_card):
        return self.suit == starter_card.suit

def cribbage_card_factory(rank, suit):
    if rank == 1: return CribbageAceCard(rank, suit)
    if 2 <= rank < 11: return CribbageCard(rank, suit)
    elif rank == 11: return CribbageHeelsCard(rank, suit)
    else: return CribbageFaceCard(rank,suit)

_suits = u'\u2660\u2661\u2662\u2663'
Spades, Hearts, Diamonds, Clubs = _suits

__test__ = {
    'card_hand_demo': '''
>>> d4 = BlackjackCard(4, Diamonds)
>>> d7 = BlackjackCard(7, Clubs)
>>> s1 = BlackjackAceCard(1, Spades)
>>> ck = BlackjackFaceCard(13, Clubs)
>>> print(d4, d7, s1, ck)
 4♢  7♣  A♠  K♣

>>> hand = [d4, d7, s1, ck]
>>> [c.hard() for c in hand]
[4, 7, 1, 10]
>>> [c.soft() for c in hand]
[4, 7, 11, 10]

>>> sum(c.hard() for c in hand)
22
''',


    'Cribbage': '''
>>> random.seed(1) # Deterministic Sequence
>>> d= DeckX(deck_builder(cribbage_card_factory))
>>> x = sort_shuffler(d)
>>> hand1= d[12:18]
>>> [str(c) for c in hand1]
[' A♣', ' 5♠', ' 6♢', ' 4♠', ' 3♡', ' 5♢']
>>> any(c.heels() for c in hand1)
False
>>> hand2 = [
...     cribbage_card_factory(11, Spades),
...     cribbage_card_factory(5, Hearts),
...     cribbage_card_factory(5, Clubs),
...     cribbage_card_factory(5, Diamonds),
... ]
>>> [str(c) for c in hand2]
[' J♠', ' 5♡', ' 5♣', ' 5♢']
>>> any(c.heels() for c in hand2)
True
>>> starter = cribbage_card_factory(5,Spades)
>>> any(c.nobs(starter) for c in hand2)
True
>>> any(c.nobs(starter) for c in hand1)
False
''',

    'DeckBuilder': '''
>>> random.seed(1) # Deterministic Sequence
>>> deck_builder1 = DeckBuilder(cribbage_card_factory)
>>> d1 = deck_builder1.build()
>>> [str(c) for c in d1[:5]]
[' K♡', ' 3♡', '10♡', ' 6♢', ' A♢']

>>> random.seed(1) # Deterministic Sequence
>>> deck_builder2 = DeckBuilder(cribbage_card_factory, n=1)
>>> d2 = deck_builder2.build()
>>> [str(c) for c in d1[:5]]
[' K♡', ' 3♡', '10♡', ' 6♢', ' A♢']

>>> all(c1.rank == c2.rank and c1.suit == c2.suit for c1, c2 in zip( d1, d2 ))
True
''',
}


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
