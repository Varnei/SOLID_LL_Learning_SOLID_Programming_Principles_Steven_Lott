"""S.O.L.I.D Design.

Chapter 5. DIP.
"""
from typing import *
from collections.abc import *
import random
import unittest.mock as mock
import unittest
import abc

from ch02.ch_02_isp import Card, BlackjackAceCard, BlackjackCard, BlackjackFaceCard

# 05_01

class AbstractCardFactory(Callable):
    def __call__(self, rank: int, suit: str) -> Card:
        raise NotImplementedError

class AbstractCardFactory(Callable, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, rank: int, suit: str) -> Card:
        pass

class BlackjackCardFactory(AbstractCardFactory):
    def __call__(self, rank: int, suit: str) -> Card:
        if rank == 1: return BlackjackAceCard(rank, suit)
        elif 2 <= rank < 11: return BlackjackCard(rank, suit)
        else: return BlackjackFaceCard(rank, suit)

def deck_builder(factory: AbstractCardFactory) -> List[Card]:
    return [factory(rank,suit)
            for rank in range(1,14)
                for suit in _suits]

# 05_02

class SomeHouse:
    pass

class Blackjack_3_2:
    pass

class SimplePlayer:
    pass

class Rules1Player:
    pass

class Rules2Player:
    pass

class Configurer:
    """Abstract superclass of configuration objects."""

class SimpleBuilder:
    HOUSE_CLASS_MAP = {
        'default': SomeHouse,
        'typical': SomeHouse,
        'pays32': Blackjack_3_2,
    }
    PLAYER_CLASS_MAP = {
        'default': SimplePlayer,
        'rules1': Rules1Player,
        'rules2': Rules2Player,
    }
    def __init__(self, options):
        self.house= self.HOUSE_CLASS_MAP[options.house]()
        self.player= self.PLAYER_CLASS_MAP[options.player]()

class Configure_Simulator_V3_1(Configurer):
    HOUSE_CLASS_MAP = {
        'default': SomeHouse,
        'typical': SomeHouse,
        'pays32': Blackjack_3_2,
    }
    PLAYER_CLASS_MAP = {
        'default': SimplePlayer,
        'rules1': Rules1Player,
        'rules2': Rules2Player,
    }
    def __init__(self, options, environment, config_file):
        if options.house:
            self.house_name= options.house
        elif 'house' in config_file:
            self.house_name= config_file['house']
        else:
            self.house_name= environment.get('MYAPP_HOUSE', 'default')
        if options.player:
            self.player_name= options.player
        elif 'player' in config_file:
            self.player_name= config_file['player']
        else:
            self.player_name = environment.get('MYAPP_PLAYER', 'default')
    @property
    def house(self):
        return self.HOUSE_CLASS_MAP[self.house_name]()
    @property
    def player(self):
        return self.PLAYER_CLASS_MAP[self.player_name]()

import pathlib
import os.path
import argparse

config_places = [pathlib.Path(os.curdir),
    pathlib.Path(os.path.expanduser('~')),
    pathlib.Path(os.path.expanduser('~simulator')),
    pathlib.Path('/etc/simulator')]

class Simulator:
    def __init__(self, house, player):
        pass

def main(args, env, config_class=Configure_Simulator_V3_1, sim_class=Simulator):
    """Typical use: main(sys.argv, os.environ)"""
    parser= argparse.ArgumentParser()
    parser.add_argument('--house')
    parser.add_argument('--player')
    options = parser.parse_args(args)
    file_configuration = {}
    for directory in config_places:
        candidate_path = directory / 'simulator.yaml'
        if candidate_path.exists():
            file_configuration= yaml.load(candidate_path.open())
            break
    config_builder = config_class(options, env, file_configuration)
    house = config_builder.house
    player = config_builder.player
    simulation = sim_class( house, player )
    simulation.run()

# 05_03

class TestDeckBuilder(unittest.TestCase):
    def setUp(self):
        self.mock_cards = [mock.Mock(return_value=i) for i in range(52)]
        self.mock_card_factory = mock.Mock(
            side_effect = self.mock_cards
        )
    def runTest(self):
        deck = deck_builder(self.mock_card_factory)
        self.assertEqual(deck, self.mock_cards)
        self.assertEqual(52, len(self.mock_card_factory.mock_calls))
        # Check 13 ranks × 4 suits

import ch05.ch_05_main

class TestMain(unittest.TestCase):
    def setUp(self):
        self.mock_card_factory = mock.Mock()
        self.mock_deck_builder = mock.Mock( return_value = mock.Mock() )
        self.mock_shuffler = mock.Mock()
        self.mock_settings = mock.Mock(
            card_factory = self.mock_card_factory,
            deck_builder = self.mock_deck_builder,
            shuffler = self.mock_shuffler
        )
    def runTest(self):
        with mock.patch('ch05.ch_05_main.settings', self.mock_settings):
            ch05.ch_05_main.main()
        self.mock_deck_builder.assert_called_once_with(
            self.mock_card_factory, self.mock_shuffler
        )


_suits = u'\u2660\u2661\u2662\u2663'
Spades, Hearts, Diamonds, Clubs = _suits

__test__ = {
    'BlackjackCardFactory': '''
>>> random.seed(1) # Deterministic Sequence
>>> blackjack_card_factory = BlackjackCardFactory()
>>> d= deck_builder(blackjack_card_factory)
>>> random.shuffle(d)
>>> [str(c) for c in d[:5]]
[' K♡', ' 3♡', '10♡', ' 6♢', ' A♢']
''',

    'SimpleBuilder': '''
>>> from argparse import Namespace
>>> options= Namespace(player='rules1', house='typical')
>>> config= SimpleBuilder(options)
>>> config.player #doctest: +ELLIPSIS
<....Rules1Player object at ...>
>>> config.house #doctest: +ELLIPSIS
<....SomeHouse object at ...>

''',

    'Configure': '''
>>> from argparse import Namespace
>>> options= Namespace(player='rules1', house=None)
>>> environment= {'MYAPP_HOUSE': 'default'}
>>> config_file= {}
>>> config= Configure_Simulator_V3_1(options, environment, config_file)
>>> config.house #doctest: +ELLIPSIS
<....SomeHouse object at ...>
>>> config.player #doctest: +ELLIPSIS
<....Rules1Player object at ...>
''',

    'Main': '''
>>> args = ['--player', 'rules2']
>>> environment= {'MYAPP_HOUSE': 'default'}
>>> mock_class = mock.MagicMock( return_value= mock.Mock() )
>>> main(args, environment, sim_class=mock_class)
>>> mock_class.mock_calls #doctest: +ELLIPSIS
[call(<....SomeHouse object at ...>, <....Rules2Player object at ...>)]
>>> mock_class.return_value.mock_calls
[call.run()]
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=0)
    unittest.main()
