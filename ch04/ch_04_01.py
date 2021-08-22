"""S.O.L.I.D Design.

Chapter 4, OCP. Part 1.
"""
import random
from ch02.ch_02_02 import DeckX, blackjack_card_factory, deck_builder
from ch04.ch_04_03 import Shuffler

class ShoeWithBurn(DeckX):
    def __init__(self, cards, burn=0.33):
        super().__init__(cards)
        penetration= int(random.gauss(burn,burn/10)*len(cards))
        del self[-penetration:]

class FluentBuilder:
    """
    >>> random.seed(1) # Deterministic Sequence
    >>> fb = FluentBuilder()
    >>> shoe = fb.build(fb.factory, 6).shuffle().shoe()
    >>> [str(c) for c in shoe[:5]]
    [' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
    """
    def __init__(self):
        self.shuffler= Shuffler()
    def factory(self, *args):
        return blackjack_card_factory(*args)
    def build(self, factory, decks):
        self.deck= deck_builder(factory, decks)
        return self
    def shuffle(self, *args, **kw):
        self.deck= self.shuffler.shuffle(self.deck)
        return self
    def shoe(self, *args, **kw):
        return ShoeWithBurn(self.deck)

__test__ = {
    'Shoe Builder Functional': '''
>>> random.seed(1) # Deterministic Sequence
>>> shuffler= Shuffler().shuffle
>>> s1 = ShoeWithBurn(shuffler(deck_builder(blackjack_card_factory, 6)), burn=0.25)
>>> [str(c) for c in s1[:5]]
[' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
''',
}



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
