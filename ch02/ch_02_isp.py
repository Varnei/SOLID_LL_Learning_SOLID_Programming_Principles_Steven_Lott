"""S.O.L.I.D Design.

Chapter 2. ISP.
"""
import random

# 02_01_isp

class Card:
    def __init__(self, rank, suit):
        self.rank= rank
        self.suit= suit
        self._text= "{:2d}".format(self.rank)
    def __str__(self):
        return "{_text:>2s}{suit}".format_map(vars(self))
    def __repr__(self):
        return '{class_}({rank!r}, {suit!r})'.format(
            class_= type(self).__name__,
            **vars(self)
        )

class BlackjackCard1(Card):
    """Lazy Calculation of points"""
    def hard(self):
        if self.rank <= 10: return self.rank
        return 10
    def soft(self):
        if self.rank == 1: return 11
        if self.rank <= 10: return self.rank
        return 10

class BlackjackCard2(Card):
    """Eager calculation of points"""
    def __init__(self, *args):
        super().__init__(*args)
        self._hard = self.rank if self.rank <= 10 else 10
        self._soft = 11 if self.rank == 1 else self.rank if self.rank <= 10 else 10
    def hard(self):
        return self._hard
    def soft(self):
        return self._soft

class BlackjackCard(Card):
    def hard(self):
        return self.rank
    def soft(self):
        return self.rank

class BlackjackFaceCard(BlackjackCard):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._text = {11:'J', 12:'Q', 13:'K'}[self.rank]
    def hard(self):
        return 10
    def soft(self):
        return 10

class BlackjackAceCard(BlackjackCard):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._text = 'A'
    def hard(self):
        return 1
    def soft(self):
        return 11

class CribbageCard(Card):
    def his_heels(self):
        return False
    def points(self):
        return self.rank

class CribbageFaceCard(CribbageCard):
    def his_heels(self):
        return False
    def points(self):
        return 10

class CribbageNobsCard(CribbageFaceCard):
    def his_heels(self):
        return True

def cribbage_card_factory(rank, suit):
    if rank == 11: return CribbageNobsCard(rank, suit)
    elif rank in (12, 13): return CribbageFaceCard(rank, suit)
    else: return CribbageCard(rank, suit)

## 02_02_deck_shoe

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

# 02_03_wrap_v_extend

from collections.abc import MutableSequence

class DeckW:
    def __init__(self, cards: MutableSequence):
        self.cards= cards
    def __iter__(self):
        return iter(self.cards)
    def __getitem__(self, slice_or_index):
        return self.cards[slice_or_index]
    def __setitem__(self, slice_or_index, value):
        self.cards[slice_or_index]= value
    def __len__(self):
        return len(self.cards)

class Shoe1(DeckW):
    def shuffle_burn(self):
        random.shuffle(self)
        del self[-100:]
    def __delitem__(self, slice_or_index):
        del self.cards[slice_or_index]

class Shoe2(DeckW):
    def shuffle_burn(self):
        random.shuffle(self.cards)
        del self.cards[-100:]

class Shoe3(DeckX):
    def shuffle_burn(self):
        random.shuffle(self)
        cards = int(random.uniform(.225, .275) * len(self))
        del self[-cards:]

_suits = u'\u2660\u2661\u2662\u2663'
Spades, Hearts, Diamonds, Clubs = _suits

__test__ = {
    'Card': '''
>>> c=Card(1,Spades)
>>> str(c)
' 1♠'
''',

    'BlackjackCard1': '''
>>> b1 = BlackjackCard1(1, Spades)
>>> str(b1)
' 1♠'
>>> b1.hard()
1
>>> b1.soft()
11
''',

    'BlackjackCard2': '''
>>> b2 = BlackjackCard2(1, Hearts)
>>> str(b2)
' 1♡'
>>> b2.hard()
1
>>> b2.soft()
11
''',

    'BlackjackAceCard': '''
>>> b3 = BlackjackAceCard(1, Diamonds)
>>> str(b3)
' A♢'
>>> b3.hard()
1
>>> b3.soft()
11
''',

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

    'Deck Wrapped': '''
>>> random.seed(1) # Deterministic Sequence
>>> deckw = DeckW(deck_builder(blackjack_card_factory))
>>> random.shuffle(deckw)
>>> dealer = iter(deckw)
>>> hand = [next(dealer) for _ in range(5)]
>>> hand
[BlackjackFaceCard(13, '♡'), BlackjackCard(3, '♡'), BlackjackCard(10, '♡'), BlackjackCard(6, '♢'), BlackjackAceCard(1, '♢')]
>>> deckw[:5]
[BlackjackFaceCard(13, '♡'), BlackjackCard(3, '♡'), BlackjackCard(10, '♡'), BlackjackCard(6, '♢'), BlackjackAceCard(1, '♢')]
''',

    'Shoe1': '''
>>> random.seed(1) # Deterministic Sequence
>>> shoe1 = Shoe1(deck_builder(blackjack_card_factory, 6))
>>> shoe1.shuffle_burn()
>>> dealer = iter(shoe1)
>>> hand = [next(dealer) for _ in range(5)]
>>> [str(c) for c in hand]
[' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
''',

    'Shoe2': '''
>>> random.seed(1) # Deterministic Sequence
>>> shoe2 = Shoe2(deck_builder(blackjack_card_factory, 6))
>>> shoe2.shuffle_burn()
>>> dealer = iter(shoe2)
>>> hand = [next(dealer) for _ in range(5)]
>>> [str(c) for c in hand]
[' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
''',

    'Deck Extended': '''
>>> random.seed(1) # Deterministic Sequence
>>> deckx = DeckX(deck_builder(blackjack_card_factory))
>>> random.shuffle(deckx)
>>> dealer = iter(deckx)
>>> hand = [next(dealer) for _ in range(5)]
>>> [str(c) for c in hand]
[' K♡', ' 3♡', '10♡', ' 6♢', ' A♢']
>>> [str(c) for c in deckx[:5]]
[' K♡', ' 3♡', '10♡', ' 6♢', ' A♢']
>>> cribbage = CribbageDeck(deck_builder(cribbage_card_factory))
>>> for i in range(52):
...     if cribbage[i].his_heels(): break
>>> i
40
>>> cribbage.cut(i)
>>> cribbage[0]
CribbageNobsCard(11, '♠')
>>> len(cribbage)
52
''',

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
