"""S.O.L.I.D Design.

Chapter 5, DIP. Part 3.
"""
import unittest
import unittest.mock as mock
from ch05.ch_05_01 import deck_builder

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

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=0)
    unittest.main()
