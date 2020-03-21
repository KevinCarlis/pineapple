try:
    import pygame
    import os
    import random
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CARD_WIDTH = 70
CARD_HEIGHT = 105
SPACE = 15
BLACK = (0, 0, 0)
GREEN = (0, 50, 0)
LIME = (50, 205, 50)
WHITE = (255, 255, 255)
FPS = 30

class Card():
    def __init__ (self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__ (self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

    def __eq__(self, other):
        return self.rank == other

    def __ne__(self, other):
        return self.rank != other

    def __lt__(self, other):
        return self.rank < other

    def __le__(self, other):
        return self.rank <= other

    def __gt__(self, other):
        return self.rank > other

    def __ge__(self, other):
        return self.rank >= other
    
    def __mul__(self, other):
        return other * self.rank
    
    def __rmul__(self, other):
        return self.rank * other

    def __add__(self, other):
        return other + self.rank

    def __radd__(self, other):
        return self.rank + other


class Deck:
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    SUITS = ('S', 'D', 'H', 'C')

    def __init__ (self):
        self.shuffle()

    def shuffle(self):
        self.deck = [Card(rank, suit) for rank in self.RANKS for suit in self.SUITS]
        random.shuffle(self.deck)

    def __len__ (self):
        return len(self.deck)

    def deal (self, *args):
        if len(self) == 0:
            return None
        elif args:
            return [self.deck.pop() for _ in range(args[0])]
        else:
            return [self.deck.pop()]


class Score:
    def __init__ (self, hand):
        # create a list to store total_point
        self.hand = hand
        self.score = 0
        self.result = None
        self.isRoyal(self.hand)

    def point(self, hand):
        return (hand[0] * 13 ** 4 
               + hand[1] * 13 ** 3 
               + hand[2] * 13 ** 2 
               + hand[3] * 13
               + hand[4])

    def isRoyal(self, hand):
        """returns the total_point and prints out 'Royal Flush' if true, 
        if false, pass down to isStraightFlush(hand)"""
        sortedHand = sorted(hand, reverse=True)
        flag = True
        Cursuit = sortedHand[0].suit
        Currank = 14
        for card in sortedHand:
            if card.suit != Cursuit or card.rank != Currank:
                flag = False
                break
            else:
                Currank -= 1
        if flag:
            self.result = 'Royal Flush'
            self.score = 10 * 13 ** 5 + self.point(sortedHand) 
        else:
            self.isStraightFlush(sortedHand)

    def isStraightFlush(self, hand):       
        """returns the total_point and prints out 'Straight Flush' if true, 
        if false, pass down to isFour(hand)"""
        sortedHand = sorted(hand,reverse=True)
        if sortedHand[0] == 14:
            sortedHand[0].rank = 1
            sortedHand = sorted(sortedHand, reverse=True)
        flag = True
        Cursuit = sortedHand[0].suit
        Currank = sortedHand[0].rank
        for card in sortedHand:
            if card.suit != Cursuit or card.rank != Currank:
                flag = False
                break
            else:
                Currank -= 1
        if flag:
            self.result = 'Straight Flush'
            self.score = 9 * 13 ** 5 + self.point(sortedHand)
        else:
            for card in sortedHand:
                if card == 1:
                    card.rank = 14
            self.isFour(sortedHand)

    def isFour(self, hand):
        """returns the total_point and prints out 'Four of a Kind' if true, 
        if false, pass down to isFull()"""
        sortedHand = sorted(hand, reverse=True)
        # since it has 4 identical ranks,the 2nd one in the sorted listmust be the identical rank
        Currank = sortedHand[1].rank
        count = 0
        for card in sortedHand:
            if card == Currank:
                count += 1
        if count == 4:
            self.result = 'Four of a Kind'
            if sortedHand[0] != sortedHand[1]:
                sortedHand = sorted(sortedHand)
            self.score = 8 * 13 ** 5 + self.point(sortedHand)    
        else:
            self.isFull(sortedHand)

    def isFull(self, hand):
        """returns the total_point and prints out 'Full House' if true, 
        if false, pass down to isFlush()"""
        sortedHand = sorted(hand, reverse=True)
        #create a list to store ranks
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        # The 1st rank and the last rank should be different in a sorted list
        rank1 = sortedHand[0].rank                  
        rank2 = sortedHand[-1].rank
        num_rank1 = mylist.count(rank1)
        num_rank2 = mylist.count(rank2)
        if num_rank1 == 3 and num_rank2 == 2:
            self.result = 'Full House'
            self.score = 7 * 13 ** 5 + self.point(sortedHand)
        elif num_rank1 == 2 and num_rank2 == 3:
            self.result = 'Full House'
            self.score = 7 * 13 ** 5 + self.point(sorted(sortedHand))
        else:
            self.isFlush(sortedHand)

    def isFlush(self, hand):
        """returns the total_point and prints out 'Flush' if true, 
        if false, pass down to isStraight()"""
        sortedHand = sorted(hand, reverse=True)
        flag = True
        Cursuit = sortedHand[0].suit
        for card in sortedHand:
            if not(card.suit == Cursuit):
                flag = False
                break
        if flag:
            self.result = 'Flush'
            self.score = 6 * 13 ** 5 + self.point(sortedHand)
        else:
            self.isStraight(sortedHand)

    def isStraight(self, hand):
        sortedHand = sorted(hand, reverse=True)
        if sortedHand[0] == 14 and sortedHand[1] == 5:
            sortedHand[0].rank = 1
            sortedHand = sorted(sortedHand, reverse=True)
        flag = True
        # this should be the highest rank
        Currank = sortedHand[0].rank
        for card in sortedHand:
            if card != Currank:
                flag = False
                break
            else:
                Currank-=1
        if flag:
            self.result = 'Straight'
            self.score = 5 * 13 ** 5 + self.point(sortedHand)
        else:
            for card in sortedHand:
                if card == 1:
                    card.rank = 14
            self.isThree(sortedHand)

    def isThree(self, hand):
        sortedHand = sorted(hand, reverse=True)
        curRank = sortedHand[2].rank
        #In a sorted rank, the middle one should have 3 counts
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(curRank) == 3:
            pointHand = [sortedHand[2]] * 3
            for card in sortedHand:
                if card.rank != curRank:
                    pointHand.append(card)
            self.result = 'Three of a Kind'
            self.score = 4 * 13 ** 5 + self.point(pointHand)
        else:
            self.isTwo(sortedHand)

    def isTwo(self, hand):
        """returns the total_point and prints out 'Two Pair' if true, 
        if false, pass down to isOne()"""
        sortedHand = sorted(hand, reverse=True)
        # in a five cards sorted group, the 2nd and 4th card should have another identical rank
        rank1 = sortedHand[1].rank                        
        rank2 = sortedHand[3].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(rank1) == 2 and mylist.count(rank2) == 2:
            pointHand = [sortedHand[1]] * 2 + [sortedHand[3]] * 2
            for card in sortedHand:
                if card != rank1 and card != rank2:
                    pointHand.append(card)
            self.result = 'Two Pair'
            self.score = 3 * 13 ** 5 + self.point(pointHand)
        else:
            self.isOne(sortedHand)

    def isOne (self, hand):                            
        """returns the total_point and prints out 'One Pair' if true, 
        if false, pass down to isHigh()"""
        sortedHand = sorted(hand, reverse=True)
        # create an empty list to store ranks
        ranks=[]
        for card in sortedHand:
            ranks.append(card.rank)
        for index, rank in enumerate(ranks):
            if ranks.count(rank) == 2:
                self.result = 'One Pair'
                pointHand = [sortedHand[index]] * 2
                for card in sortedHand:
                    if card != rank:
                        pointHand.append(card)
                self.score = 2 * 13 ** 5 + self.point(sortedHand)
                break
        else:
            self.isHigh(sortedHand)

    def isHigh (self, hand):
        """returns the total_point and prints out 'High Card'""" 
        sortedHand = sorted(hand, reverse=True)
        self.result = 'High Card'
        self.score = 1 * 13 ** 5 + self.point(sortedHand)


class TopScore:
    def __init__ (self, hand):
        # create a list to store total_point
        self.hand = hand
        self.score = 0
        self.result = None
        self.isThree(self.hand)

    def point(self, hand):
        # point()function to calculate partial score
        return (hand[0] * 13 ** 4 
               + hand[1] * 13 ** 3 
               + hand[2] * 13 ** 2 
               + 1 * 13
               + 1)

    def isThree(self, hand):
        sortedHand = sorted(hand, reverse=True)
        if sortedHand[0] == sortedHand[1] == sortedHand[2]:
            self.result = 'Three of a Kind'
            self.score = 4 * 13 ** 5 + self.point(sortedHand)
        else:
            self.isOne(sortedHand)

    def isOne (self, hand):                            
        """returns the total_point and prints out 'One Pair' if true, 
        if false, pass down to isHigh()"""
        sortedHand = sorted(hand,reverse=True)
        if sortedHand[0] == sortedHand[1]:
            self.result = 'One Pair'
            self.score = 2 * 13 ** 5 + self.point(sortedHand)
        elif sortedHand[1] == sortedHand[2]:
            self.result = 'One Pair'
            self.score = 2 * 13 ** 5 + self.point(sorted(sortedHand))
        else:
            self.isHigh(sortedHand)

    def isHigh (self, hand):
        """returns the total_point and prints out 'High Card'""" 
        sortedHand = sorted(hand, reverse=True)
        self.result = 'High Card'
        self.score = 1 * 13 ** 5 + self.point(sortedHand)

class CardSprite(pygame.sprite.Sprite):
    def __init__ (self, card):
        self.card = card
        self.draggable = True
        self.dragging = False
        self.image, self.rect = load_png(str(card) + '.png', dimensions=(CARD_WIDTH, CARD_HEIGHT))
        pygame.sprite.Sprite.__init__(self)

class CardSlot:
    def __init__(self, left, top):
        self.drawbox = pygame.Rect((left, top), (CARD_WIDTH, CARD_HEIGHT))
        self.hitbox = self.drawbox.inflate(SPACE * 4, SPACE * 4)
        self.card = None


class SlotHolder:
    def __init__(self, rowName, card_num, top):
        self.rowName = rowName
        self.score = 0
        self.card_num = card_num
        self.top = top
        self.width = int((CARD_WIDTH + SPACE) * self.card_num - SPACE)
        self.left = (SCREEN_WIDTH - self.width)/2
        self.height = CARD_HEIGHT
        self.rect = pygame.Rect(
            (self.left, self.top), 
            (self.width, self.height)
        )
        self.cardslots = self._card_spaces()

    def __str__(self):
        return self.rowName

    def __len__(self):
        return len(self.cardslots)

    def __getitem__(self, key):
        return self.cardslots[key]

    def _card_spaces(self):
        return[
            CardSlot(self.left + (CARD_WIDTH + SPACE) * slot, self.top) for slot in range(self.card_num)
        ]

    @property
    def cards(self):
        count = 0
        for slot in self:
            if slot.card:
                count += 1
        return count


class Board:
    def __init__(self, playerName):
        self.playerName = playerName
        self.fouled = False
        self.starting_hand = True
        self.full = False
        self.deck = Deck()
        self.top = SlotHolder("Top", 3, SPACE)
        self.middle = SlotHolder("Middle", 5, CARD_HEIGHT + SPACE * 2)
        self.bottom = SlotHolder("Bottom", 5, CARD_HEIGHT * 2 + SPACE * 3)
        self.hand = SlotHolder("Hand", 5, SCREEN_HEIGHT - CARD_HEIGHT - SPACE)
        self.deal()

    def __len__(self):
        return len(self.board)

    def __getitem__(self, key):
        return self.board[key]

    @property
    def board(self):
        return [self.top, self.middle, self.bottom, self.hand]

    def update(self):
        for row in self:
            for slot in row:
                if slot.card:
                    slot.card.rect = slot.drawbox.copy()

    def deal(self):
        cards = self.deck.deal(5)
        starting_hand = []
        for card in cards:
            starting_hand.append(CardSprite(card))
        self.cardsprites = pygame.sprite.Group(starting_hand)
        for slot, card in zip(self.hand, starting_hand):
            slot.card = card
        self.update()

    def draw(self):
        self.hand = SlotHolder("Hand", 3, SCREEN_HEIGHT - CARD_HEIGHT - SPACE)
        cards = self.deck.deal(3)
        new_hand = []
        for card in cards:
            new_hand.append(CardSprite(card))
        self.cardsprites.add(new_hand)
        for slot, card in zip(self.hand, new_hand):
            slot.card = card
        self.update()


def load_png(name, dimensions=None):
    """ Load image and return image object"""
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        if dimensions:
            image = pygame.transform.scale(image, dimensions)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()


def score(*boards):
    for board in boards:
        top = []
        for slot in board.top:
            top.append(slot.card.card)
        middle = []
        for slot in board.middle:
            middle.append(slot.card.card)
        bottom = []
        for slot in board.bottom:
            bottom.append(slot.card.card)
        top = TopScore(top)
        board.top.score = top.score
        print(board.playerName)
        print("Top:", top.result)
        mid = Score(middle)
        board.middle.score = mid.score
        print("Middle:", mid.result)
        bot = Score(bottom)
        board.bottom.score = bot.score
        print("Bottom:", bot.result)
        if mid.score > bot.score or top.score > mid.score or top.score > bot.score:
            board.fouled = True
            print("FOUL")
        print()


def winner(*boards):
    score(*boards)
    if len(boards) > 1:
        topScores = []
        midScores = []
        botScores = []
        playerNames = []
        for board in boards:
            playerNames.append(board.playerName)
            if board.fouled:
                topScores.append(0)
                midScores.append(0)
                botScores.append(0)
            else:
                topScores.append(board.top.score)
                midScores.append(board.middle.score)
                botScores.append(board.bottom.score)

        scoreList = [topScores, midScores, botScores]
        scoreText = ['Rank Top:   ', 'Rank Middle:', 'Rank Bottom:']
        for row in range(3):
            zipped = zip(scoreList[row], playerNames)
            zipped = sorted(zipped, reverse=True)
            print(scoreText[row], ", ".join([player for (score, player) in zipped]))
    else:
        if boards[0].fouled:
            lose_message = [
                "You fucking suck", 
                "Eat a dick you bad", 
                "Why you even try?", 
                "It's okay you'll get em next time",
                "Sorry you fouled out"
            ]
            print(random.choice(lose_message))
        else:
            win_message=[
                "You did okay I guess",
                "Nice",
                "Bravisimo, fantastico, alrightasaur",
                "Get it",
                "I've seen better"
            ]
            print(random.choice(win_message))

def play(screen, boards):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)
    clock = pygame.time.Clock()

    for board in boards:
        running = True
        while running:
            if not board.hand.cards and board.starting_hand:
                for row in board:
                    for slot in row:
                        if slot.card:
                            slot.card.draggable = False
                board.draw()
                board.starting_hand = False
                running = False
            if 0 < board.hand.cards < 2 and not board.starting_hand:
                for row in board:
                    for slot in row:
                        if slot.card:
                            slot.card.draggable = False
                for slot in board.hand:
                    if slot.card:
                        board.cardsprites.remove(slot.card)
                        slot.card = None
                board.draw()
                running = False
            if board.top.cards == 3 and board.middle.cards == 5 and board.bottom.cards == 5:
                for slot in board.hand:
                    if slot.card:
                        board.cardsprites.remove(slot.card)
                        slot.card = None
                board.full = True
                for board_check in boards:
                    if not board_check.full:
                        running = False
                        break
                else:
                    winner(*boards)
                    return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for row in board:
                            for slot in row:
                                if slot.card and slot.card.draggable:
                                    if slot.card.rect.collidepoint(event.pos):
                                        slot.card.dragging = True
                                        mouse_x, mouse_y = event.pos
                                        offset_x = slot.card.rect.x - mouse_x
                                        offset_y = slot.card.rect.y - mouse_y
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for row in board:
                            for old_slot in row:
                                if old_slot.card and old_slot.card.dragging:
                                    card = old_slot.card
                                    for row in board:
                                        for new_slot in row:
                                            if new_slot.hitbox.contains(card.rect):
                                                if not new_slot.card:
                                                    new_slot.card = card
                                                    old_slot.card = None
                                    board.update()
                                    card.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    for row in board:
                        for slot in row:
                            if slot.card and slot.card.dragging:
                                mouse_x, mouse_y = event.pos
                                slot.card.rect.x = mouse_x + offset_x
                                slot.card.rect.y = mouse_y + offset_y
            for row in board:
                if row.rowName != 'Hand':
                    for slot in row:
                        pygame.draw.rect(background, LIME, slot.drawbox)
            screen.blit(background, (0, 0))
            board.cardsprites.draw(screen)
            pygame.display.update()
            clock.tick(FPS)
    play(screen, boards)


def homeScreen(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)
    TEXT_SPACE = 7

    titlefont = pygame.font.Font(None, 124)
    title = titlefont.render("Pineapple", 1, LIME)
    titlepos = title.get_rect()
    titlepos.top = SPACE * 3
    titlepos.centerx = background.get_rect().centerx
    
    textfont = pygame.font.Font(None, 36)
    playButton1 = textfont.render("One Player", 1, (10, 10, 10))
    playButton1pos = playButton1.get_rect()
    playButton1pos.centerx = background.get_rect().centerx
    playButton1pos.centery = background.get_rect().centery
    
    playButton2 = textfont.render("Two Players", 1, (10, 10, 10))
    playButton2pos = playButton2.get_rect()
    playButton2pos.centerx = background.get_rect().centerx
    playButton2pos.centery = background.get_rect().centery + playButton1pos.height + SPACE * 2
    
    playButton3 = textfont.render("Three Players", 1, (10, 10, 10))
    playButton3pos = playButton3.get_rect()
    playButton3pos.centerx = background.get_rect().centerx
    playButton3pos.centery = background.get_rect().centery + (playButton2pos.height + SPACE * 2) * 2

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if playButton1pos.collidepoint(event.pos):
                        return [Board('Player1')]
                    if playButton2pos.collidepoint(event.pos):
                        return Board('Player1'), Board('Player2')
                    if playButton3pos.collidepoint(event.pos):
                        return Board('Player1'), Board('Player2'), Board('Player3')
        # pygame.draw.rect(background, LIME, titlepos.inflate(0, 5))
        pygame.draw.rect(background, LIME, playButton1pos.inflate(TEXT_SPACE, 			TEXT_SPACE))
        pygame.draw.rect(background, LIME, playButton2pos.inflate(TEXT_SPACE, 		TEXT_SPACE))
        pygame.draw.rect(background, LIME, playButton3pos.inflate(TEXT_SPACE, 		TEXT_SPACE))
        background.blit(title, titlepos)
        background.blit(playButton1, playButton1pos)
        background.blit(playButton2, playButton2pos)
        background.blit(playButton3, playButton3pos)
        screen.blit(background, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

def main():
    pygame.init()
    logo = pygame.image.load(os.path.join('images', 'PineLogo.png'))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Pineapple")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    players = homeScreen(screen)
    if players:
        play(screen, players)
    pygame.display.quit()


if __name__=="__main__":
    main()
