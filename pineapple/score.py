try:
    from constants import *
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.freetype
    from pygame.locals import *
    import random
    from enum import Enum
    from collections import Counter
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


def score_boards(boards):
    for board in boards:
        del board.hand
        print(board.player.name)
        for row in board:
            row.result()
            print(row.name.capitalize() + ':')
            print(row.result)
            print(row)
            print()
        if (
            board['top'].score > board['middle'].score
            or board['top'].score > board['bottom'].score
            or board['middle'].score > board['bottom'].score
        ):
            for row in board:
                row.score = 0
            print("FOUL")
        print()
        print()


def winner(boards):
    if len(boards) > 1:
        for row_count in range(3):
            row_name = boards[0][row_count].name
            row_scores = {}
            for board in boards:
                row_scores[board.player.name] = board[row_count].score
            print('Rankings ' + row_name.capitalize() + ':')
            row_scores = {
                k: v for k, v in sorted(row_scores.items(), key=lambda item: item[1], reverse=True)
            }
            comparators = []
            result = ""
            for count, score in enumerate(list(row_scores.values())[:-1]):
                if score == list(row_scores.values())[count + 1]:
                    comparators.append('= ')
                else:
                    comparators.append('> ')
            for count, name in enumerate(row_scores.keys()):
                result += name + ' '
                if count < len(comparators):
                    result += comparators[count]
            print(result)
            print()
                
    else:
        if boards[0]['top'].score == 0:
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

