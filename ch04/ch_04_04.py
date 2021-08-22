"""S.O.L.I.D Design.

Chapter 4, OCP. Part 4.
"""
from ch02.ch_02_01 import Card, BlackjackCard, BlackjackAceCard, BlackjackFaceCard
from ch02.ch_02_02 import blackjack_card_factory

import logging
import functools
import unittest
from unittest import mock

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

_suits = u'\u2660\u2661\u2662\u2663'
Spades, Hearts, Diamonds, Clubs = _suits

__test__ = {

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

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
    unittest.main()
