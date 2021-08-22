"""S.O.L.I.D Design.

Chapter 3. LSP.
"""

# 03_01_lsp

import random
from ch02.ch_02_isp import DeckX, deck_builder, blackjack_card_factory
from ch02.ch_02_isp import Card, BlackjackAceCard, BlackjackFaceCard, BlackjackCard
from ch02.ch_02_isp import Spades, Hearts, Diamonds, Clubs

class Shuffler:
    @staticmethod
    def shuffle(deck):
       pass

class RandomShuffler(Shuffler):
    @staticmethod
    def shuffle(deck):
        random.shuffle(deck)

class SortShuffler(Shuffler):
    @staticmethod
    def shuffle(deck):
        pairs = [(random.random(), index) for index in range(len(deck))]
        pairs.sort()
        for destination, pair in enumerate(pairs):
            r, source = pair
            deck[destination], deck[source]= deck[source], deck[destination]

def null_shuffler(deck, rng=None):
    pass

random_shuffler = random.shuffle

def sort_shuffler(deck, rng=random.random):
    pairs = [(random.random(), index) for index in range(len(deck))]
    pairs.sort()
    for destination, pair in enumerate(pairs):
        r, source = pair
        deck[destination], deck[source]= deck[source], deck[destination]

# 03_02_interface_variations

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

# 03_03_cards

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

card_hand_demo = '''
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
'''

# 03_04_defaults

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

# 03_05_isinstance

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
    'Shuffler': '''
>>> random.seed(1) # Deterministic Sequence
>>> d= DeckX(deck_builder(blackjack_card_factory, 6))
>>> s = Shuffler()
>>> s.shuffle(d)
>>> [str(c) for c in d[:5]]
[' A♠', ' A♠', ' A♠', ' A♠', ' A♠']
''',

    'RandomShuffler': '''
>>> random.seed(1) # Deterministic Sequence
>>> d= DeckX(deck_builder(blackjack_card_factory, 6))
>>> s = RandomShuffler()
>>> s.shuffle(d)
>>> [str(c) for c in d[:5]]
[' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
''',

    'SortShuffler': '''
>>> random.seed(1) # Deterministic Sequence
>>> d= DeckX(deck_builder(blackjack_card_factory, 6))
>>> s = SortShuffler()
>>> s.shuffle(d)
>>> [str(c) for c in d[:5]]
[' 2♣', ' J♣', ' 2♣', ' 4♢', ' 7♢']
''',

    'null_shuffler': '''
>>> random.seed(1) # Deterministic Sequence
>>> d= DeckX(deck_builder(blackjack_card_factory, 6))
>>> null_shuffler(d)
>>> [str(c) for c in d[:5]]
[' A♠', ' A♠', ' A♠', ' A♠', ' A♠']
''',

    'random_shuffler': '''
>>> random.seed(1) # Deterministic Sequence
>>> d= DeckX(deck_builder(blackjack_card_factory, 6))
>>> random_shuffler(d)
>>> [str(c) for c in d[:5]]
[' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
''',

    'sort_shuffler': '''
>>> random.seed(1) # Deterministic Sequence
>>> d= DeckX(deck_builder(blackjack_card_factory, 6))
>>> sort_shuffler(d)
>>> [str(c) for c in d[:5]]
[' 2♣', ' J♣', ' 2♣', ' 4♢', ' 7♢']
''',

    'cards': card_hand_demo,

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

    'ShoeBuilder': '''
>>> random.seed(1) # Deterministic Sequence
>>> cards = ShoeBuilder(blackjack_card_factory, n=6).build()
>>> [str(c) for c in cards[:5]]
[' 3♡', ' J♡', ' Q♠', '10♢', ' 8♡']
>>> len(cards)
312
''',

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
