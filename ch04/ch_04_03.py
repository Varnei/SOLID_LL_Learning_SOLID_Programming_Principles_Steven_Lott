"""S.O.L.I.D Design.

Chapter 4, OCP. Part 3.
"""
import random
from ch02.ch_02_02 import DeckX, blackjack_card_factory, deck_builder

class Shuffler:
    def __init__(self, rng=None):
        self.rng= rng
    def shuffle(self, deck):
        random.shuffle(deck, self.rng)
        return deck

class MultipassShuffler(Shuffler):
    def __init__(self, passes=1, *args, **kw):
        self.passes= passes
        super().__init__(*args, **kw)
    def shuffle(self, deck):
        for _ in range(self.passes):
            random.shuffle(deck, self.rng)
        return deck

class DeckBuilder2:
    SUITS = u'\u2660\u2661\u2662\u2663'
    def __init__(self, card_factory, shuffler, **kw):
        self.factory= card_factory
        self.shuffler= shuffler
        assert 'n' not in kw or 'n' in kw and kw['n'] == 1, 'if present, n must be 1'
    def deck(self):
        return [self.factory(r,s) for r in range(1,14) for s in self.SUITS]
    def build(self):
        cards= self.deck()
        self.shuffler(cards)
        return cards

class ShoeBuilder2(DeckBuilder2):
    def __init__(self, *args, n, burn, **kw):
        self.n= n
        self.burn= burn
        super().__init__(*args, **kw)
    def build(self):
        cards = []
        for _ in range(self.n):
            cards.extend(super().deck())
        shuffle= self.shuffler
        shuffle(cards)
        del cards[-self.burn:]
        return cards

__test__ = {

    'Shoe Builder Composite': '''
>>> random.seed(1) # Deterministic Sequence
>>> shuffler= Shuffler().shuffle
>>> s2 = ShoeBuilder2(blackjack_card_factory, shuffler, n=6, burn=100).build()
>>> [str(c) for c in s2[:5]]
[' 5♠', ' 5♢', ' Q♠', ' 5♡', ' 2♠']
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
