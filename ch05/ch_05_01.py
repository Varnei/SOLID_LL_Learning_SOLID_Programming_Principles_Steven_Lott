"""S.O.L.I.D Design.

Chapter 5, DIP. Part 1.
"""
from ch02.ch_02_01 import Card
from ch02.ch_02_02 import BlackjackCard, BlackjackAceCard, BlackjackFaceCard
from typing import *
from collections.abc import *
import abc
import random

class AbstractCardFactory(Callable):
    def __call__(self, rank: int, suit: str) -> Card:
        raise NotImplementedError

class AbstractCardFactory(Callable, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, rank: int, suit: str) -> Card:
        pass

class BlackjackCardFactory(AbstractCardFactory):
    def __call__(self, rank: int, suit: str) -> Card:
        if rank == 1: return BlackjackAceCard(rank, suit)
        elif 2 <= rank < 11: return BlackjackCard(rank, suit)
        else: return BlackjackFaceCard(rank, suit)

def deck_builder(factory: AbstractCardFactory) -> List[Card]:
    return [factory(rank,suit)
            for rank in range(1,14)
                for suit in _suits]

_suits = u'\u2660\u2661\u2662\u2663'
Spades, Hearts, Diamonds, Clubs = _suits

__test__ = {
    'BlackjackCardFactory': '''
>>> random.seed(1) # Deterministic Sequence
>>> blackjack_card_factory = BlackjackCardFactory()
>>> d= deck_builder(blackjack_card_factory)
>>> random.shuffle(d)
>>> [str(c) for c in d[:5]]
[' K♡', ' 3♡', '10♡', ' 6♢', ' A♢']
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
