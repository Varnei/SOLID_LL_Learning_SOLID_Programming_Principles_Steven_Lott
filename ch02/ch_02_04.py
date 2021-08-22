"""S.O.L.I.D Design.

Chapter 2, ISP. Part 4.
"""
from ch02.ch_02_02 import DeckX, deck_builder, blackjack_card_factory
from ch02.ch_02_02 import CribbageDeck, cribbage_card_factory
import random
from collections.abc import MutableSequence

class Shoe3(DeckX):
    def shuffle_burn(self):
        random.shuffle(self)
        cards = int(random.uniform(.225, .275) * len(self))
        del self[-cards:]

__test__ = {

    'Shoe3': '''
>>> random.seed(1) # Deterministic Sequence
>>> shoe3 = Shoe3(deck_builder(blackjack_card_factory, 6))
>>> shoe3.shuffle_burn()
>>> dealer = iter(shoe3)
>>> hand = [next(dealer) for _ in range(5)]
>>> [str(c) for c in hand]
[' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
