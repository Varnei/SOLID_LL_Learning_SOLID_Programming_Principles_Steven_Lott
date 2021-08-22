"""S.O.L.I.D Design.

Chapter 4. OCP.
"""
import random
import logging
import unittest.mock as mock
import unittest

from ch02.ch_02_isp import DeckX, Shoe3, deck_builder, blackjack_card_factory
from ch02.ch_02_isp import Spades, Hearts, Diamonds, Clubs
from ch02.ch_02_isp import Card, BlackjackCard, BlackjackAceCard, BlackjackFaceCard

# 04_01

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

# 04_03

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

# 04_04

import functools

def logged(class_):
    class_.logger = logging.getLogger(class_.__qualname__)
    return class_

def trace(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kw):
        result= method(self, *args, **kw)
        self.logger.debug("{0}(*{1!r}, **{2!r}) = {3!r}".format(
            method.__name__, args, kw, result) )
        return result
    return wrapped

@logged
class LCard(Card):
    @trace
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

@logged
class BlackjackHand(list):
    @trace
    def __init__(self, cards):
        super().__init__(cards)
    @trace
    def hard(self):
        return sum(c.hard() for c in self)

class NumberPoints:
    def hard(self):
        return self.rank
    def soft(self):
        return self.rank

class FacePoints:
    def hard(self):
        return 10
    def soft(self):
        return 10

class AcePoints:
    def hard(self):
        return 1
    def soft(self):
        return 11

class MixBlackjackCard(Card, NumberPoints):
    pass
class MixBlackjackFaceCard(Card, FacePoints):
    pass
class MixBlackjackAceCard(Card, AcePoints):
    pass

def mix_blackjack_card_factory(rank, suit):
    if 1 == rank: return MixBlackjackAceCard(rank, suit)
    elif 2 <= rank < 11: return MixBlackjackCard(rank, suit)
    else: return MixBlackjackFaceCard(rank, suit)

__test__ = {
    'Shoe Builder Functional': '''
>>> random.seed(1) # Deterministic Sequence
>>> shuffler= Shuffler().shuffle
>>> s1 = ShoeWithBurn(shuffler(deck_builder(blackjack_card_factory, 6)), burn=0.25)
>>> [str(c) for c in s1[:5]]
[' Q♢', ' 6♠', ' 5♠', ' 8♠', ' 3♡']
''',

    'Shoe Builder Composite': '''
>>> random.seed(1) # Deterministic Sequence
>>> shuffler= Shuffler().shuffle
>>> s2 = ShoeBuilder2(blackjack_card_factory, shuffler, n=6, burn=100).build()
>>> [str(c) for c in s2[:5]]
[' 5♠', ' 5♢', ' Q♠', ' 5♡', ' 2♠']
''',

    'Simple LCard': '''
>>> c = LCard(11, Spades)
>>> print(c)
11♠
>>> c
LCard(11, '♠')
>>> with mock.patch.object(LCard, 'logger') as mock_logging:
...    c2= LCard(1, Spades)
...    mock_logging.debug.mock_calls
[call("__init__(*(1, '♠'), **{}) = None")]
''',

    'BlackjackHand': '''
>>> cards = [
...      blackjack_card_factory(1, Spades),
...      blackjack_card_factory(10, Clubs)
... ]
>>> with mock.patch.object(BlackjackHand, 'logger') as mock_logging:
...     h = BlackjackHand( cards )
...     h.hard()
...     mock_logging.debug.mock_calls
11
[call("__init__(*([BlackjackAceCard(1, '♠'), BlackjackCard(10, '♣')],), **{}) = None"),
 call('hard(*(), **{}) = 11')]
''',

    'Mixin Blackjack': '''
>>> c1 = mix_blackjack_card_factory(1, Spades)
>>> c2 = mix_blackjack_card_factory(7, Spades)
>>> c3 = mix_blackjack_card_factory(12, Spades)
>>> hand = [c1, c2, c3]
>>> [str(c) for c in hand]
[' 1♠', ' 7♠', '12♠']
>>> sum(c.hard() for c in hand)
18
>>> sum(c.soft() for c in hand)
28
''',
}

class GIVEN_LCard_WHEN_create_THEN_log(unittest.TestCase):
    """This is an alternate form of the 'Simple LCard' doctest shown above.
    It's slightly easiser to debug in this form.
    """
    def runTest(self, ):
        with mock.patch.object( LCard, 'logger' ) as mock_logging:
            c = LCard(11, Spades)
            #print( mock_logging.debug.mock_calls )
            mock_logging.debug.assert_called_once_with("__init__(*(11, '♠'), **{}) = None")

class GIVEN_Hand_WHEN_create_THEN_log(unittest.TestCase):
    """This is an alternate form of the 'Simple LCard' doctest shown above.
    It's slightly easiser to debug in this form.
    """
    def runTest(self, ):
        with mock.patch.object(BlackjackHand, 'logger') as mock_logging:
            cards = [
                blackjack_card_factory(1, Spades),
                blackjack_card_factory(10, Clubs)
            ]
            h = BlackjackHand( cards )
            self.assertEqual( 11, h.hard() )
            #print( mock_logging.debug.mock_calls )
            mock_logging.debug.assert_has_calls(
                [mock.call("__init__(*([BlackjackAceCard(1, '♠'), BlackjackCard(10, '♣')],), **{}) = None"),
                 mock.call('hard(*(), **{}) = 11')]
            )


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
    unittest.main()
