print("___-menu___")
print("1: test deck \n\
2: test screen \n\
3: play game")

ch = int(input())

if ch == 1:
    from pine.deck import Deck
    deck = Deck()
    for card in deck:
        print(card)
    print(deck._cards)
