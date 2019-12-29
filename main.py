#!/usr/bin/env python
"""

Artist: Christopher Robinson, A12803368
"""

import pygame
import random as rand
from random import randint
import time
import os

BLACK = (0,0,0) #balls
PINK = (255,209,220)
WHITE = (255, 255, 255) #begin screen
BLUE = (174,198,207) #BG
RED = (255, 0, 0)
SPEED_MULT = 3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BALL_SIZE = 60
YOU_SIZE = 20
TITLE_STR = "How Long Can You Live With Yourself?"
PREMISE_STR = "The premise of this game is to not get killed by your own thoughts for 3 months until your first therapy session."
INSTRUCT_STR = "Use the arrow keys to navigate."
BEGIN_STR = "Press the SPACEBAR to begin"
WIN_STR = "Congratulations! You survived until your first therapy session."
LOSS_STR = "You are dead."
ENDGAME_STR = 'Did you know the current wait for a first time therapy appointment at the UCSD Department of Psychiatry is 3 months?'
REPLAY_STR = "Press the SPACEBAR to play again"
TIMER = 0.8

start = False
newBall = True
win = False
end = False
totalday = 1
day = 1
month = 1
stage = 0

date_string = "Day 1 Month 1"
ball_list = []
clock = pygame.time.Clock()
stage1 = open("stage1.txt","r")
stage2 = open("stage2.txt","r")
stage3 = open("stage3.txt","r")
stage4 = open("stage4.txt","r")
words1 = stage1.read().split()
words2 = stage2.read().split()
words3 = stage3.read().split()
words4 = stage4.read().split()
wordsList = [words1, words2, words3, words4]

pygame.init()
font = pygame.font.Font("./times-new-roman.ttf", 32)
endgamefont = pygame.font.Font("./times-new-roman.ttf", 16)
timer = time.time()
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption(TITLE_STR)
topscreen = pygame.surface.Surface((800,100))

#define moving character
class You:
    def __init__(self):
        self.x = rand.randrange(YOU_SIZE, SCREEN_WIDTH - YOU_SIZE)
        self.y = rand.randrange(YOU_SIZE + 100, SCREEN_WIDTH - YOU_SIZE)
        self.speed = 16
       
#moving character, bounded by walls
def down(you):
    you.y = you.y + you.speed
    if(you.y > SCREEN_HEIGHT-YOU_SIZE): 
        you.y = SCREEN_HEIGHT-YOU_SIZE

#moving character, bounded by walls
def up(you):
    you.y = you.y - you.speed
    if(you.y < 100):
        you.y = 100

#moving character, bounded by walls
def left(you):
    you.x = you.x - you.speed
    if(you.x < 0):
        you.x = 0

#moving character, bounded by walls
def right(you):
    you.x = you.x + you.speed
    if(you.x > SCREEN_WIDTH-YOU_SIZE): 
        you.x = SCREEN_WIDTH-YOU_SIZE

#show black square on the screen
def show_you(you):
    pygame.draw.rect(screen, BLACK, [you.x, you.y, YOU_SIZE, YOU_SIZE])

#create ball
class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.word = ""
        self.stage = 0

#creates ball object and returns
def make_ball(stage):
    ball = Ball()
    ball.stage = stage
    ball.x = rand.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
    ball.y = rand.randrange(BALL_SIZE + 100, SCREEN_HEIGHT - BALL_SIZE)
    ball.change_x = randint(SPEED_MULT*stage, SPEED_MULT*(stage+1))
    ball.change_y = randint(SPEED_MULT*stage, SPEED_MULT*(stage+1))

    return ball
        
#shows ball on screen
def show_ball(ball):
    rBall = 255
    gBall = (-1.0 * (totalday/100 - 1.0)) * 209.0
    bBall = (-1.0 * (totalday/100 - 1.0)) * 220.0
    pygame.draw.circle(screen, (rBall, gBall, bBall), [ball.x, ball.y], BALL_SIZE)
    ballfont = pygame.font.Font("./times-new-roman.ttf", 24)
    text = ballfont.render(ball.word, True, (0,0,0), (rBall, gBall, bBall))
    screen.blit(text, [ball.x - BALL_SIZE/2, ball.y])

#gets color of background
def get_bg_color():
    rBG = (-1.0 * (totalday/100 - 1.0)) * 174.0
    gBG = (-1.0 * (totalday/100 - 1.0)) * 198.0
    bBG = (-1.0 * (totalday/100 - 1.0)) * 207.0
    return (rBG, gBG, bBG)
    
#create character
you = You()

#game logic
while True:

    #game is not running
    if not start:
        screen.fill(WHITE)
        
        #game just ended
        if end:
            #if you win, show win screen
            if win:
                text = font.render(WIN_STR, True, (0,0,0), WHITE)
                textRect = text.get_rect()
                textRect.center = (400,100)
                text2 = endgamefont.render(ENDGAME_STR, True, (0,0,0), WHITE)
                text3 = font.render(REPLAY_STR, True, (0,0,0), WHITE)
                textRect2 = text.get_rect()
                textRect3 = text.get_rect()
                textRect2.center = (420,300)
                textRect3.center = (550,700)
            #if you lost, show loss screen
            else:
                text = font.render(LOSS_STR, True, (0,0,0), WHITE)
                textRect = text.get_rect()
                textRect.center = (400,100)
                text2 = endgamefont.render(ENDGAME_STR, True, (0,0,0), WHITE)
                text3 = font.render(REPLAY_STR, True, (0,0,0), WHITE)
                textRect2 = text.get_rect()
                textRect3 = text.get_rect()
                textRect2.center = (110,300)
                textRect3.center = (250,700)
            screen.blit(text3, textRect3)
            if timer + 30 < time.time():
                end = False
                win = False

        #title screen
        else:
            text = font.render(TITLE_STR, True, (0,0,0), WHITE)
            text2 = endgamefont.render(PREMISE_STR, True, (0,0,0), WHITE)
            text3 = endgamefont.render(INSTRUCT_STR, True, (0,0,0), WHITE)
            text4 = font.render(BEGIN_STR, True, (0,0,0), WHITE)
            textRect = text.get_rect()
            textRect2 = text2.get_rect()
            textRect3 = text3.get_rect()
            textRect4 = text4.get_rect()
            textRect.center = (400,100)
            textRect2.center = (400,250)
            textRect3.center = (380,350)
            textRect4.center = (380,600)
            screen.blit(text3, textRect3)
            screen.blit(text4, textRect4)
        screen.blit(text, textRect)
        screen.blit(text2, textRect2)

        #if a SPACEBAR pressed, start game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    timer = time.time()
                    end = False
                    win = False
                    start = True
                    day = 1
                    totalday = 1
                    newBall = True
                    month = 1
                    stage = 0
                    rBG, gBG, bBG = BLUE
                    rBall, gBall, bBall = PINK
                    date_string = "Day 1 Month 1"
                    ball_list = []

    #game play
    else:
        if totalday >= 90:
           win = True
           start = False
           end = True
           timer = time.time()

        screen.fill(get_bg_color())
        topscreen.fill(WHITE)
        screen.blit(topscreen,(0,0))
        text = font.render(date_string, True, (0,0,0), WHITE)
        textRect = text.get_rect(center=(400,50))
        screen.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            down(you)
        elif keys[pygame.K_UP]:
            up(you)
        elif keys[pygame.K_RIGHT]:
            right(you)
        elif keys[pygame.K_LEFT]:
            left(you)

        #keep track of gameplay
        if timer + TIMER < time.time():
            timer = time.time()
            day = day + 1
            totalday = totalday + 1
            if day >= 31:
                day = 1
                month = month + 1
            date_string = "Day %d Month %d" % (day, month)
            if totalday == 23 or totalday == 45 or totalday == 67:
                newBall = True
        if newBall:
            stage = stage + 1 
            ball = make_ball(stage)
            ball_list.append(ball)
            newBall = False
        for ball in ball_list:
            ball.x += ball.change_x
            ball.y += ball.change_y
            if ball.y > SCREEN_HEIGHT - BALL_SIZE or ball.y < BALL_SIZE + 100:
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - BALL_SIZE or ball.x < BALL_SIZE:
                ball.change_x *= -1
            #set word displayed on ball to cooresponding word from txt file
            ball.word = wordsList[ball.stage-1][totalday-(22*(ball.stage-1))-1]
            show_ball(ball)
            if you.x + YOU_SIZE > ball.x - BALL_SIZE + 8 and you.x < ball.x + BALL_SIZE - 8:
                if you.y + YOU_SIZE > ball.y - BALL_SIZE + 8 and you.y< ball.y + BALL_SIZE - 8:
                    win = False
                    end = True
                    start = False
        show_you(you)
            
        clock.tick(30)
    pygame.display.update()
