"""S.O.L.I.D Design.

Chapter 5. OCP.

Demo main program
"""
from ch05 import ch_05_settings as settings

def main():
    deck = settings.deck_builder(
        settings.card_factory,
        settings.shuffler).build()
    print(deck)

if __name__ == "__main__":
    main()
