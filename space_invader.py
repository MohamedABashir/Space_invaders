#!/usr/bin/python

import pygame
import random
from pygame.locals import *
import os
import sys
import time
from subprocess import Popen

pygame.init()



SCREEN_WIDTH = 700
SCREEN_HEIGHT = 550
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255,223,0)
gameDisplay = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()


# images
how_many_lives = 3
background = pygame.image.load('./img/background.jpg')
enemy_ship = (pygame.image.load('./img/enemy.png'))
ufo_ship = (pygame.image.load('./img/ufo.png'))
player_ship = pygame.image.load('./img/space-ship.png') 
blocker = pygame.image.load('./img/blocker.jpg')
# tiny_ship = pygame.image.load('./img/tiny_ship.png')
# tiny_ships = [tiny_ship]*how_many_lives


u_x = 1000
u_y = 1000
ufo_rect = Rect(u_x, u_y,30, 30)
ufo_show = 25000
ufo_bullet = []

#player initial position
player_x = SCREEN_WIDTH//2
player_y = SCREEN_HEIGHT-100
player_rect = Rect(player_x, player_y, 64, 64) # for collision detection
player_lives = [player_ship] * how_many_lives


# sounds 
bullet_sound = pygame.mixer.Sound('./music/shoot.wav')
enemy_bullet_sound = pygame.mixer.Sound('./music/shoot2.wav')
enemy_killed = pygame.mixer.Sound('./music/invaderkilled.wav')
player_killed = pygame.mixer.Sound('./music/playerkilled.wav')

# score
font = pygame.font.Font('./font/font.ttf', 20)
def display_text(score, x, y, text):
    sc = font.render(text +':' +str(score), True, (0, 255, 0))
    gameDisplay.blit(sc, (x,y))

# bullets
bullet_y = 450
playerBullets = []
shots = 1
enemy_bullets = []

def player_update(event):
    '''update player movement'''
    player_move = 0
    if event.key == pygame.K_LEFT:
        player_move = -7
    elif event.key ==pygame.K_RIGHT:
        player_move =7
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT: 
            player_move = 0
    return player_move
def player_bullet_collision(playerBullets,ufo_rect,invaders, score):
    ''' checks if the player bullet has collided with the invader '''
    for bullet in playerBullets:
        pygame.draw.rect(gameDisplay,GOLD, bullet)
        if bullet.colliderect(ufo_rect):
            try:
                del playerBullets[0]
                score += 20
            except:
                pass

        for index, invader in enumerate(invaders):
            if invader.colliderect(bullet):
                try:
                    del playerBullets[0]
                    enemy_killed.play()
                    del invaders[index]
                    score += 5
                except:
                    pass
    return score


def make_invaders():
    '''creates mulitple invader '''
    y = 50
    invaders = []
    how_many_row = 3
    how_many_col = 5
    while y <= 64 * how_many_row:
        x = 20
        while x <= 64 *5:
            invaders.append(Rect(x, y, 64, 64))
            x += 64
        y += 70
    return invaders

# moves the alien and checks if it touches player's ship
def move_invaders(invaders, direction, player_rect, player_lives, player_live):
    '''move the invader side and down'''
    # moves each alien
    for inv in invaders:
        if inv.right >= SCREEN_WIDTH or inv.left <= 0:
            direction *= -1
            for i in invaders:
                i.move_ip(0, 15)
            break

    # checks for collision
    for inv in invaders:
        inv.move_ip(direction, 0)
        if inv.colliderect(player_rect):
                try:
                    del player_lives[0]
                    player_killed.play()
                    player_live -=1
                except:
                    pass
    return direction


def enemy(array):
    '''load aliens ship'''
    for i in array:
        gameDisplay.blit(enemy_ship, i)


def ufo():
    '''load ufo ship'''
    gameDisplay.blit(ufo_ship, ufo_rect)


def blockers(x, y):
    '''create blockers that protects player from enemy bullets'''
    blocks = []
    for i in range(60):
        row = []
        for j in range(30):
            row.append(Rect(i+x, j+y, 6, 6))
        blocks.append(row)
    return blocks


def block_collition(block, invaders,playerBullets, enemy_bullets, ufo_bullet):
    '''checks for collition against the blocks '''
    for i in block:
        for j in i:
            gameDisplay.blit(blocker, j)
    for i in block:
        for j in i:
            # checks if the player' bullet has touched the blockers
            for bullet in playerBullets:
                if j.colliderect(bullet):
                    try:
                        del i[:20]
                        del playerBullets[0]
                        
                    except:
                        pass
            # checks if the invader's bullet has touched the blockers        
            for e_bullets in enemy_bullets:
                if j.colliderect(e_bullets):
                    if len(i) >= 3:
                        try:
                            del i[:40]
                            del enemy_bullets[0]
                            enemy_bullets.remove(e_bullets)
                        except:
                            pass
            # checks if the invader has touched the blockers
            for inv in invaders:
                if j.colliderect(inv):
                    try:
                        del i[:20]
                    except:
                        pass
            #checks if the invader's bullet has touched the blockers        
            for u_b in ufo_bullet:
                if j.colliderect(u_b):
                    try:
                        del i[:40]
                        ufo_bullet.pop()
                    except:
                        pass


def crash():
    '''opens this exact program when player dies '''
    filename = 'run_game_forever.py'
    try:
        p = Popen([sys.executable, filename])
        p.communicate()
    except:
        pass


def gameLoop():
    block = blockers(30, 400)
    block2 = blockers(300, 400)
    block3 = blockers(550, 400)
    probability_to_fire = 0.001
    direction = 3 
    invaders = make_invaders()
    move = 0
    score = 0
    shot = 0
    player_live = 3
    timer = pygame.time.get_ticks()

    # game loop
    game_over = False
    while not game_over:
        gameDisplay.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # change the player and bullet pos
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:  
                # update players movement based on K_RIGHT or K_Left  
                move = player_update(event)
                if event.key == pygame.K_SPACE:
                    # sets player's bullet
                    if len(playerBullets) < shots and len(player_lives)>= 1:
                        bullet_sound.play()
                        bullet_x = player_rect.x
                        playerBullets.append(Rect(bullet_x+23, bullet_y-26, 2, 5))
                        if len(playerBullets) < shots:
                            playerBullets.append(Rect(bullet_x, bullet_y+2, 2, 5))
                            playerBullets.append(Rect(bullet_x+48, bullet_y+4, 2, 5))
        
        # checks player ship for bounderies
        if player_rect.x > SCREEN_WIDTH-50:
            player_rect.x -= 10
        elif player_rect.x < 0:
            player_rect.x += 10 
  
        #fire player bullets
        for b in playerBullets:
            b.move_ip(0,-5)
            if b.y < 0:
                playerBullets.remove(b)
        
        # check if player bullet collided with the invader
        score = player_bullet_collision(playerBullets,ufo_rect,invaders, score)

        # move the invader side and down
        direction =move_invaders(invaders, direction,
                                player_rect, player_lives, player_live)
        
        # create new wave
        if len(invaders) < 1:
            invaders = make_invaders()
        
        
        # create enemy bullet
        for i in invaders:
            ans = random.random()
            if ans <= probability_to_fire:
                enemy_bullets.append(Rect(i.x+25, i.y+50, 2, 4))

        # moves enemy bullets
        for b in enemy_bullets:
            b.move_ip(0,3)

        # detect if player has been hit
        for bullet in enemy_bullets:
            pygame.draw.rect(gameDisplay,RED, bullet)
            if bullet.colliderect(player_rect):
                enemy_bullets.remove(bullet)
                if len(player_lives) >= 1 and player_live >= 1:
                    player_killed.play()
                    del player_lives[0]
                    player_live -=1
        ufo()
        # updates the ufo's location after some time
        current_time = pygame.time.get_ticks()
        passed = current_time - timer
        if 2400 < passed < 2500:
            ufo_rect.x = random.randrange(20, SCREEN_WIDTH-100)
            ufo_rect.y = random.randrange(20, 200)
            while len(ufo_bullet) < 1:
                ufo_bullet.append(Rect(ufo_rect.x, ufo_rect.y, 2, 5))
        ufo_rect.move_ip(2, 0)
        
        # reset the timer
        if passed > 12000:
            timer = current_time
        
        # moves ufo bullets
        for b in ufo_bullet:
            b.move_ip(0,3)
            if b.y - ufo_rect.y < 10 and 0 <b.x< SCREEN_WIDTH:
                enemy_bullet_sound.play()
            if b.y > SCREEN_HEIGHT:
                ufo_bullet.remove(b)

        # detect if player has been hit by ufo bullet
        for bullet in ufo_bullet:
            pygame.draw.rect(gameDisplay,(0, 0, 0), bullet)
            if bullet.colliderect(player_rect):
                ufo_bullet.remove(bullet)
                if len(player_lives) >= 1:
                    player_killed.play()
                    del player_lives[0]
                    player_live -= 1
                    
        #make blockers and check for blocker collition
        block_collition(block, invaders, playerBullets, enemy_bullets, 
                        ufo_bullet)
        block_collition(block2, invaders, playerBullets, enemy_bullets,
                         ufo_bullet)
        block_collition(block3, invaders, playerBullets, enemy_bullets,
                         ufo_bullet)

        #update player position
        player_rect.x += move

        if len(player_lives) >= 1:
            gameDisplay.blit(player_lives[0], player_rect)

        # when game over
        if len(player_lives)<1:
            pygame.quit()
            crash()
            sys.exit()

        enemy(invaders)
        display_text(score, 10, 10, 'Score')
        display_text(player_live, SCREEN_WIDTH-100, 10, 'Lives')
        clock.tick(100)
        pygame.display.flip()
    pygame.quit()


def main():
    newgame = gameLoop
    start = True
    text =  'Press any Key to Play'
    font = pygame.font.Font('./font/font.ttf', 50)
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                newgame()
                sys.exit()
        gameDisplay.blit(background, (0, 0))
        sc = font.render(text, True, (0, 255, 0))
        gameDisplay.blit(sc, (10,SCREEN_HEIGHT//2))
        pygame.display.flip()

main()
