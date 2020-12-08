import pytest
import sys
sys.path.insert(0, '..')
from pineapple.deck import Deck, DeckTest



def test_defaults():
    deck = Deck()
    assert len(deck._deck) == 52
    assert len(deck) == 52


def test_deck_access():
    deck = Deck()
    assert next(deck) == deck._cards[0]
    assert deck(3) == tuple(deck._cards[1:4])
    flag = True
    for card in deck:
        if flag:
            assert card == deck._cards[4]
            flag = False
    assert len(deck) == 52
    
    
    

# class TestDeck():

    # def test_deck_starts_full(self):
        # deck = card.Deck()
        # self.assertIsNone(deck.dealt)
        # self.assert
            # self.assertIsNotNone(client.pool)
            # pool_ref = weakref.ref(client._pool)
            # self.assertIsNotNone(pool_ref())
        # self.assertIsNone(pool_ref())

    # def test_atexit_closes_threadpool(self):
        # client = kubernetes.client.ApiClient()
        # self.assertIsNotNone(client.pool)
        # self.assertIsNotNone(client._pool)
        # atexit._run_exitfuncs()
        # self.assertIsNone(client._pool)