#! python2

import pygame
from pygame.locals import *
import pygbutton
import colors
from random import choice
pygame.init()

def writeOnScreen(text, color, surface, font, x="center", y="center"):
    def text_objects(text, color, font):
        textSurf = font.render(text, 0, color)
        return textSurf, textSurf.get_rect()
    textSurf, textRect = text_objects(text, color, font)
    surfSize = surface.get_size()
    if x == "center":
        if y == "center":
            textRect.center = surfSize[0]/2, surfSize[1]/2
            surface.blit(textSurf, textRect)
        else:
            textRect.center = surfSize[0]/2, y
            surface.blit(textSurf, textRect)
    elif y == "center":
        textRect.center = x, surfSize[1]/2
        surface.blit(textSurf, textRect)
    else:
        surface.blit(textSurf, (x, y))

def draw_table(surface, color, width):
    #-------
    pygame.draw.line(surface, color, (75, 185), (325, 185), width)
    pygame.draw.line(surface, color, (75, 270), (325, 270), width)
    #|||||||
    pygame.draw.line(surface, color, (155, 110), (155, 355), width)
    pygame.draw.line(surface, color, (240, 110), (240, 355), width)

def get_free_boxes(table):
    empty = []
    r = 0
    b = 0
    for row in table:
        b = 0
        for box in row:
            if box == None:
                empty.append((r, b))
            b += 1
        r += 1

    return empty

def computer_turn(table, turn):
    if turn == -1:
        empty = get_free_boxes(table)
        if len(empty) > 0:
            selected = choice(empty)
            table[selected[0]][selected[1]] = "o"
            turn *= -1
            
    return table, turn

def get_board_dup(table):
    dup = []
    r = 0
    for row in table:
        dup.append([])
        for b in row:
            dup[r].append(b)
        r += 1
    return dup
            
def computer_turn_with_AI(table, turn):
    # The algorithm is:
    # Step 1: Check if you can win, if so, do it.
    # Step 2: Check if the player can win, if so, block him.
    # Step 3: Check if one of the corners are free, if so, choose one and put there "o".
    # Step 4: Check if the center is free, if so, put there "o".
    # Step 5: Check if one of tne sides are free, if so, choose one and put there "o".

    def canWin(table, letter):
        free = get_free_boxes(table)
        for box in free:
            dup = get_board_dup(table)
            dup[box[0]][box[1]] = letter
            if check_win(dup) == letter:
                return box
        return False

    def areFree(table, boxes):
        free = []
        for box in boxes:
            if table[box[0]][box[1]] == None:
                free.append(box)

        if len(free) == 0:
            return False
        else:
            return free

    if turn == -1:
        if canWin(table, "o") != False:
            to_win = canWin(table, "o")
            table[to_win[0]][to_win[1]] = "o"
            turn *= -1
        elif canWin(table, "x") != False:
            to_block = canWin(table, "x")
            table[to_block[0]][to_block[1]] = "o"
            turn *= -1
        elif areFree(table, [(0, 0), (0, 2), (2, 0), (2, 2)]) != False:
            free_corners = areFree(table, [(0, 0), (0, 2), (2, 0), (2, 2)])
            choosen = choice(free_corners)
            table[choosen[0]][choosen[1]] = "o"
            turn *= -1
        elif table[1][1] == None:
            table[1][1] = "o"
            turn *= -1
        elif areFree(table, [(0, 1), (1, 0), (1, 2), (2, 1)]) != False:
            free_sides = areFree(table, [(0, 1), (1, 0), (1, 2), (2, 1)])
            choosen = choice(free_sides)
            table[choosen[0]][choosen[1]] = "o"
            turn *= -1
        
    return table, turn

def check_win(table):
    for sign in ["x", "o"]:
        if table[0][0] == sign and table[0][1] == sign and table[0][2] == sign:
            return sign
        elif table[1][0] == sign and table[1][1] == sign and table[1][2] == sign:
            return sign
        elif table[2][0] == sign and table[2][1] == sign and table[2][2] == sign:
            return sign
        elif table[0][0] == sign and table[1][0] == sign and table[2][0] == sign:
            return sign
        elif table[0][1] == sign and table[1][1] == sign and table[2][1] == sign:
            return sign
        elif table[0][2] == sign and table[1][2] == sign and table[2][2] == sign:
            return sign
        elif table[0][0] == sign and table[1][1] == sign and table[2][2] == sign:
            return sign
        elif table[0][2] == sign and table[1][1] == sign and table[2][0] == sign:
            return sign
    for row in table:
        if None in row:
            return None
    return "tie"

def reset_table():
    return [[None, None, None], [None, None, None], [None, None, None]]

def table_update(table, rects, turn, mode, event_list):
    for event in event_list:
        if event.type == MOUSEBUTTONDOWN:
            mousePOS = pygame.mouse.get_pos()
            r = 0
            b = 0
            for row in rects:
                b = 0
                for box in row:
                    if table[r][b] == None:
                        if box.collidepoint(mousePOS):
                            if mode == "twoplayers":
                                if turn == 1:
                                    table[r][b] = "x"
                                elif turn == -1:
                                    table[r][b] = "o"
                                turn *= -1
                            elif mode == "oneplayer":
                                if turn == 1:
                                    table[r][b] ="x"
                                    turn *= -1
                    b += 1
                r += 1
    return table, turn

def draw_XnO(surface, table, rects, font):
    r = 0
    b = 0
    for row in table:
        b = 0
        for box in row:
            surface.blit(font.render(box, 0, colors.black), rects[r][b])
            b += 1
        r += 1

_clock = pygame.time.Clock()
FPS = 30
size = width, height = 400, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic Tac Toe")
icon = pygame.image.load("tttIcon.png")
pygame.display.set_icon(icon)
font = pygame.font.Font(pygame.font.match_font("comicsansms"), 24)
title_font = _font = pygame.font.Font(pygame.font.match_font("comicsansms"), 38)
title_font.set_underline(True)
small_font = pygame.font.Font(pygame.font.match_font("comicsansms"), 18)
big_font = pygame.font.Font(pygame.font.match_font("comicsansms"), 60)

wins = 0
ties = 0
loses = 0
table = [[None, None, None],
         [None, None, None],
         [None, None, None]]

table_rects = [[pygame.Rect(75, 110, 77, 72), pygame.Rect(159, 110, 78, 72), pygame.Rect(244, 110, 82, 72)],
              [pygame.Rect(75, 188, 77, 79), pygame.Rect(159, 189, 78, 78), pygame.Rect(244, 189, 82, 78)],
              [pygame.Rect(75, 274, 77, 82), pygame.Rect(159, 274, 78, 82), pygame.Rect(244, 274, 82, 82)]]

displaying = "menu"

#Menu:
onePlayBut = pygbutton.PygButton(rect=(115, 150, 170, 50), caption="One Player", bgcolor=(0, 220, 0), fgcolor=colors.white, font=font)
twoPlayBut = pygbutton.PygButton(rect=(115, 201, 170, 50), caption="Two Players", bgcolor=(0, 220, 0), fgcolor=colors.white, font=font)
menuBut = pygbutton.PygButton(rect=(130, 65, 70, 35), caption="Menu", bgcolor=(0, 220, 0), fgcolor=colors.control, font=small_font)
resetBut = pygbutton.PygButton(rect=(200, 65, 70, 35), caption="Reset", bgcolor=(0, 220, 0), fgcolor=colors.control, font=small_font) 

status = None
turn = 1 #1 means X turn, -1 means O turn.
win_checked = False

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif "click" in onePlayBut.handleEvent(event) and displaying == "menu":
            displaying = "oneplayer"
            table = reset_table()
            wins, ties, loses = 0, 0, 0
            win_checked = False
            turn = 1
        elif "click" in twoPlayBut.handleEvent(event) and displaying == "menu":
            displaying = "twoplayers"
            table = reset_table()
            wins, ties, loses = 0, 0, 0
            win_checked = False
            turn = 1
        elif "click" in menuBut.handleEvent(event) and displaying != "menu":
            displaying = "menu"
        elif "click" in resetBut.handleEvent(event) and displaying != "menu":
            table = reset_table()
            win_checked = False

    screen.fill(colors.white)
    writeOnScreen("Tic Tac Toe", colors.black, screen, title_font, "center", 20)
    if displaying == "menu":
        onePlayBut.draw(screen)
        twoPlayBut.draw(screen)
    elif displaying == "oneplayer":
        menuBut.draw(screen)
        resetBut.draw(screen)
        writeOnScreen("Wins: {0}, Ties: {1}, Loses: {2}".format(wins,ties,loses), colors.black, screen, font, y=375)
        status = check_win(table)
        if status == None:
            draw_table(screen, colors.black, 7)
            draw_XnO(screen, table, table_rects, big_font)
            table, turn = table_update(table, table_rects, turn, "oneplayer", events)
            table, turn = computer_turn_with_AI(table, turn)
        elif status == "x":
            writeOnScreen("You win!!!", colors.black, screen, big_font)
            if not win_checked:
                wins += 1
            win_checked = True
            turn = 1
        elif status == "o":
            writeOnScreen("You lose!!", colors.black, screen, big_font)
            if not win_checked:
                loses += 1
            win_checked = True
            turn = -1
        elif status == "tie":
            writeOnScreen("It's a tie", colors.black, screen, big_font)
            if not win_checked:
                ties += 1
            win_checked = True
    elif displaying == "twoplayers":
        menuBut.draw(screen)
        resetBut.draw(screen)
        writeOnScreen("X Wins: {0}, Ties: {1}, O Wins: {2}".format(wins,ties,loses), colors.black, screen, font, y=375)
        if turn == 1:
            writeOnScreen("X turn", colors.black, screen, small_font, x=20, y=50)
        elif turn == -1:
            writeOnScreen("O turn", colors.black, screen, small_font, x=20, y=50)
        status = check_win(table)
        if status == None:
            draw_table(screen, colors.black, 7)
            draw_XnO(screen, table, table_rects, big_font)
            table, turn = table_update(table, table_rects, turn, "twoplayers", events)
        elif status == "x":
            writeOnScreen("X wins!!!", colors.black, screen, big_font)
            if not win_checked:
                wins += 1
            win_checked = True
            turn = 1
        elif status == "o":
            writeOnScreen("O wins!!!", colors.black, screen, big_font)
            if not win_checked:
                loses += 1
            win_checked = True
            turn = -1
        elif status == "tie":
            writeOnScreen("It's a tie!!", colors.black, screen, big_font)
            if not win_checked:
                ties += 1
            win_checked = True
            
    pygame.display.update()
