"""S.O.L.I.D Design.

Chapter 7. Process.
"""

# 07_02

import unittest
from ch02.ch_02_isp import BlackjackFaceCard

class GIVEN_card_WHEN_repr_THEN_text(unittest.TestCase):
    def setUp(self):
        self.card = BlackjackFaceCard(11, u'\u2660')
    def runTest(self):
        text = str(self.card)
        self.assertEqual( u' J♠', text)

if __name__ == "__main__":
    unittest.main()
