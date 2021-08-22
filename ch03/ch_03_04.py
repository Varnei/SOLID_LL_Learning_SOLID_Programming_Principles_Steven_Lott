"""S.O.L.I.D Design.

Chapter 3, LSP. Part 4.
"""
import random
from ch02.ch_02_02 import blackjack_card_factory
from ch03.ch_03_03 import cribbage_card_factory

class DeckBuilder:
    SUITS = u'\u2660\u2661\u2662\u2663'
    def __init__(self, card_factory, **kw):
        self.factory= card_factory
        assert 'n' not in kw or 'n' in kw and kw['n'] == 1, 'if present, n must be 1'
    def build(self):
        cards= [self.factory(r,s) for r in range(1,14) for s in self.SUITS]
        random.shuffle(cards)
        return cards

class ShoeBuilder(DeckBuilder):
    def __init__(self, card_factory, *, n):
        super().__init__(card_factory)
        self.n= n
    def build(self):
        cards = []
        for _ in range(self.n):
            cards.extend(super().build())
        random.shuffle(cards)
        return cards

__test__ = {

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

    'ShoeBuilder': '''
>>> random.seed(1) # Deterministic Sequence
>>> cards = ShoeBuilder(blackjack_card_factory, n=6).build()
>>> [str(c) for c in cards[:5]]
[' 3♡', ' J♡', ' Q♠', '10♢', ' 8♡']
>>> len(cards)
312
''',

}


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
