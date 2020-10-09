#############################################################################################################################
#                                                                                                                           #
#   SIMPLE "REPEAT THE PATH" GAME MADE WITH PYGAME LIB                                                                      #
#                                                                                                                           #
#   do whatever you want with this, honsetly it doesn't do much of a difference to me                                       #
#                                                                                                                           #
#   IMPORTANT:                                                                                                              #
#                                                                                                                           #
#   Piano samples source: https://freesound.org/people/jobro/packs/2489/                                                    #
#   via Creative Commons 3.0 License
#                                                                                                                           #
#############################################################################################################################

import pygame
import time
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

windowResolution = (280, 320)

window = pygame.display.set_mode(windowResolution)
pygame.display.set_caption('Repeat the pattern!')

# CONSTANTS

# ---
# COLORS
# basic colors
DARK_GREY = (20, 20, 20)
BLACK = (0, 0, 0)

# other colors
COLORS = [(255, 51, 51), (255, 153, 51), (255, 255, 51), (153, 255, 51), (51, 255, 51), (55, 255, 153), (51, 255, 255), (51, 153, 255), (51, 51, 255), (153, 51, 255), (255, 51, 255), (255, 51, 153), (255, 255, 255), (255, 153, 153), (255, 204, 153), (255, 255, 153), (204, 255, 153), (153, 255, 153), (153, 255, 204), (153, 255, 255), (153, 204, 255), (153, 153, 255), (204, 153, 255), (255, 153, 255), (255, 153, 204)]
random.shuffle(COLORS)

# ---
# OBJECTS
REC_SIZE = 50

#---
# FONTS
COURIER = pygame.font.SysFont('Courier', 20)
BIGCOURIER = pygame.font.SysFont('Courier', 40)


# improvised solution to skip multi-threading while highlighting squares for specified amount of time
global hQuery
hQuery = []

def return_square_coords(mouseX, mouseY):
    for i in range(0,5):
        for j in range(0,5):
            if 5 * (i + 1) + 50 * i <= mouseX and mouseX <= 5 * (i + 1) + 50 * i + 50:
                if 40 + 5 * (j + 1) + 50 * j <= mouseY and mouseY <= 40 + 5 * (j + 1) + 50 * j + 50:
                    return (i, j)

def draw_square(x, y, color):
    pygame.draw.rect(window, color, [5 * (x + 1) + 50 * x, 40 + 5 * (y + 1) + 50 * y, REC_SIZE, REC_SIZE])

def highlight_square(i, j, color):
    play_sound(i + j * 5)
    draw_square(i, j, color)
    pygame.display.update()
    hQuery.append((i, j, time.time() + 0.5))

def draw_window():
    window.fill(DARK_GREY)

    for i in range(0, 5):
        for j in range(0, 5):
            draw_square(i, j, BLACK)

    pygame.display.update()

def render_scoreboard(level, score):
    pygame.draw.rect(window, DARK_GREY, [0, 0, 280, 40])
    return COURIER.render("LEVEL: " + str(level) + "   SCORE: " + str(score), False, (255, 255, 255))

def play_sound(name):
    pygame.mixer.music.load("sounds/" + str(name) + ".wav")
    pygame.mixer.music.play()

def win_update():
    for thread in hQuery:
        if (thread[2] < time.time()):
            draw_square(thread[0], thread[1], BLACK)
            pygame.display.update()
            hQuery.remove(thread)

def print_gameover_screen(level, score):
    window.fill(DARK_GREY)
    window.blit(render_scoreboard(level, score), (25, 150))
    window.blit(BIGCOURIER.render("GAME OVER!", False, (255, 255, 255)), (20, 15))
    window.blit(COURIER.render("Your stats:", False, (255, 255, 255)), (70, 100))
    window.blit(COURIER.render("Thanks for playing!", False, (255, 255, 255)), (30, 250))
    pygame.display.update()

    aExit = False

    while aExit != True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                aExit = True

# local level variables
inGame = True
playerTurn = False

level = 1
score = 0
patterns = []
playerPattern = []
patternNo = 0

draw_window()

pygame.time.wait(2000)

while inGame:
    window.blit(render_scoreboard(level, score), (10, 15))

    win_update()

    # GENERATING NEW LEVEL FOLLOWED BY THE DISPLAY OF ALL RECENT PATTERNS
    if playerTurn == False:

        sqX = random.randint(0, 4)
        sqY = random.randint(0, 4)
        patterns.append((sqX, sqY))

        pygame.time.wait(500)

        for pattern in patterns:
            win_update()
            pygame.time.wait(200)
            highlight_square(pattern[0], pattern[1], COLORS[(pattern[0] + 5 * pattern[1])])
            win_update()
            pygame.time.wait(500)

        playerTurn = True

    else:

        if patternNo < level:
            if playerPattern != []:
                if playerPattern[0][0] == patterns[patternNo][0] and playerPattern[0][1] == patterns[patternNo][1]:
                    patternNo += 1
                    playerPattern.pop()
                else:
                    for i in range(0, 3):
                        highlight_square(patterns[patternNo][0], patterns[patternNo][1], (155, 0, 0))
                        highlight_square(playerPattern[0][0], playerPattern[0][1], (155, 0, 0))
                        pygame.time.wait(300)
                        highlight_square(patterns[patternNo][0], patterns[patternNo][1], (0, 0, 0))
                        highlight_square(playerPattern[0][0], playerPattern[0][1], (0, 0, 0))
                        pygame.time.wait(300)

                    patterns.clear()
                    playerPattern.clear()
                    inGame = False
        else:
            win_update()
            patternNo = 0
            score += level
            level += 1
            playerTurn = False




    # KEYBOARD EVENTS
    for event in pygame.event.get():

        # KE available all time
        if event.type == pygame.QUIT:
            inGame = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inGame = False

        # KE limited
        if playerTurn == True:

            if event.type == pygame.MOUSEBUTTONDOWN and playerTurn == True:
                mousePos = pygame.mouse.get_pos()
                clickedSquare = return_square_coords(mousePos[0], mousePos[1])

                if (clickedSquare != None):
                    playerPattern.append(clickedSquare)
                    highlight_square(clickedSquare[0], clickedSquare[1], COLORS[clickedSquare[0] + 5 * clickedSquare[1]])


print_gameover_screen(level, score)

pygame.display.quit()
pygame.quit()