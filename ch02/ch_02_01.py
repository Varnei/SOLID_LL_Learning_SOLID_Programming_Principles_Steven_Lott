"""S.O.L.I.D Design.

Chapter 2, ISP. Part 1.
"""
import random

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
}


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)

