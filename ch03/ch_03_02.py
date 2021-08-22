"""S.O.L.I.D Design.

Chapter 3, LSP. Part 2.
"""

import random
from ch02.ch_02_02 import blackjack_card_factory

class Deck(list):
    pass

class Shoe(Deck):
    def shuffle_burn(self, penetration=.25):
        random.shuffle(self)
        cards = int(penetration * len(self))
        del self[-cards:]

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

class DeckR1(list):
    pass

class ShoeR1(DeckR1):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        burn = int(random.uniform(.225, .275)*len(self))
        del self[-burn:]

class DeckR2(list):
    def shuffle(self):
        random.shuffle(self)

class ShoeR2(DeckR2):
    def shuffle(self):
        super().shuffle()
        burn = int(random.uniform(.225, .275)*len(self))
        del self[-burn:]

__test__ = {
        'Shoe Rethink & ShoeBuilder': '''
>>> random.seed(1) # Deterministic Sequence
>>> shoe = ShoeR1(ShoeBuilder(blackjack_card_factory, n=6).build())
>>> [str(c) for c in shoe[:5]]
[' 3♡', ' J♡', ' Q♠', '10♢', ' 8♡']
>>> len(shoe)
229
''',

    'Shoe Refactor & ShoeBuilder': '''
>>> random.seed(1) # Deterministic Sequence
>>> shoe = ShoeR2(ShoeBuilder(blackjack_card_factory, n=6).build())
>>> shoe.shuffle()
>>> [str(c) for c in shoe[:5]]
[' 7♠', ' 4♢', ' 5♣', ' K♡', ' A♢']
>>> len(shoe)
233
''',

}


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
