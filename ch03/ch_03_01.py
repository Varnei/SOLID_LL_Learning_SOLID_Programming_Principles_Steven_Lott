"""S.O.L.I.D Design.

Chapter 3, LSP. Part 1.
"""

import random
from ch02.ch_02_02 import DeckX, deck_builder, blackjack_card_factory

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
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
