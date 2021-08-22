"""S.O.L.I.D Design.

Chapter 2, ISP. Part 3.
"""
from ch02.ch_02_02 import DeckX, deck_builder, blackjack_card_factory
from ch02.ch_02_02 import CribbageDeck, cribbage_card_factory
import random
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

__test__ = {

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

}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
