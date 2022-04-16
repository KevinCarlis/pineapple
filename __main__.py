print("___menu___")
print("0: Test path\n\
1: test deck \n\
2: test screen \n\
3: play game")

ch = int(input())

if ch == 0:
    from pine.constants import cwd, IMAGE_FOLDER
    print(f'Code folder: {cwd}')
    print(f'Image folder: {IMAGE_FOLDER}')

if ch == 1:
    from pine.deck import Deck
    deck = Deck()
    print(deck)
    print(f'Deal top card: {deck()}\nRest of deck:')
    print([str(card) for card in deck._cards])
    print(f'Whole deck:\n{deck._cards}')

if ch == 2:
    from pine.cardholder import CardSlot, Hand
    slot_test = CardSlot()
    hand = Hand()
    print(hand.elements)

if ch == 3:
    from pine.controller import main
    main()

