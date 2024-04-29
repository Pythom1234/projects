#!/usr/bin/python3
import pygame
import asyncio
import sys
import os
from math import *

pygame.font.init()
pygame.display.init()

os.chdir('platformer/')

async def main():
    global selected_map, map_image, map, position, player_jump, screen_position, air_time, player_state, player_walk_cycle, run, color, screen, clock, lives, invicibility, player_hurt_timer, trampolines, coins, player_coins, stage, max_coins, checkpoints, player_checkpoint
    total_coins = 0
    win = False
    screen = pygame.display.set_mode((1600,900))
    clock = pygame.time.Clock()
    screen.fill('black')
    run = True
    play = False
    text = pygame.font.Font(size=55).render('START',True,(0,255,0,255))
    screen.blit(text,(800 - text.get_width() / 2, 500 - text.get_height() / 2))
    text = pygame.font.Font(size=20).render('Pokud je hra příliš pomalá, stiskněte a pusťte Shift.',True,(255,255,255,255))
    screen.blit(text,(800 - text.get_width() / 2, 870 - text.get_height() / 2))
    pygame.display.flip()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                run = False
                play = True
        await asyncio.sleep(0)
    if not play:
        pygame.quit()
        exit()
    def load_map(map_name):
        global map_image, map, position, player_jump, screen_position, air_time, player_state, player_walk_cycle, lives, invicibility, player_hurt_timer, trampolines, coins, player_coins, stage, max_coins, checkpoints, player_checkpoint
        map_image = [pygame.image.load(f'assets/maps/map{map_name}_image0.png'),pygame.image.load(f'assets/maps/map{map_name}_image1.png')]
        trampolines = []
        coins = []
        checkpoints = []
        map = pygame.image.load(f'assets/maps/map{map_name}.png')
        for x in range(map.get_width()):
            for y in range(map.get_height()):
                color = map.get_at((x,y))
                if color == (255,0,255,255):
                    trampolines += [[x,y,'up',0]]
                if color == (255,255,0,255):
                    coins += [[x,y]]
                if color == (0,255,0,255):
                    checkpoints += [[x,y,False]]
        map = pygame.transform.scale(map,[map.get_width() * 70,map.get_height() * 70])
        position = [1,0]
        player_jump = 0
        screen_position = [0,0]
        air_time = 0
        player_state = 'stand_r'
        player_walk_cycle = 1
        lives = 3
        invicibility = 0
        player_hurt_timer = 0
        player_coins = 0
        player_checkpoint = [1,1]
        stage = 0
        max_coins = len(coins)
    selected_map = 0
    frameskip = 1
    frames_skipped = 0
    run = True
    player_color = 'green'
    font = pygame.font.Font(size=55)
    heart_empty = pygame.image.load(f'assets/images/UI/heart_empty.png')
    heart_half = pygame.image.load(f'assets/images/UI/heart_half.png')
    heart_full = pygame.image.load(f'assets/images/UI/heart_full.png')
    p1 = pygame.image.load(f'assets/images/UI/p1.png')
    p2 = pygame.image.load(f'assets/images/UI/p2.png')
    p3 = pygame.image.load(f'assets/images/UI/p3.png')
    trampoline_up = pygame.image.load(f'assets/images/trampoline_up.png')
    trampoline_down = pygame.image.load(f'assets/images/trampoline_down.png')
    checkpoint0 = pygame.image.load(f'assets/images/checkpoint0.png')
    checkpoint1 = pygame.image.load(f'assets/images/checkpoint1.png')
    checkpoint2 = pygame.image.load(f'assets/images/checkpoint2.png')
    coin = pygame.image.load(f'assets/images/star.png')
    player = {}
    for i in ['stand_l','stand_r','hurt_l','hurt_r','jump_l','jump_r'] + [f'walk{str(j+1).zfill(2)}_l' for j in range(11)] + [f'walk{str(j+1).zfill(2)}_r' for j in range(11)]:
        player[i] = pygame.image.load(f'assets/images/player/{player_color}/{i}.png')
    load_map(selected_map)
    while run:
        stage += .08
        if stage > 1:
            stage = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    frameskip = 5
                if event.key == pygame.K_l:
                    selected_map += 1
                    try:
                        load_map(selected_map)
                    except:
                        run = False
                        win = True
                    total_coins += player_coins
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    frameskip = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 1000 < pygame.mouse.get_pos()[0] < 1050 and 5 < pygame.mouse.get_pos()[1] < 55:
                    player_color = 'green'
                if 1050 < pygame.mouse.get_pos()[0] < 1100 and 5 < pygame.mouse.get_pos()[1] < 55:
                    player_color = 'blue'
                if 1100 < pygame.mouse.get_pos()[0] < 1150 and 5 < pygame.mouse.get_pos()[1] < 55:
                    player_color = 'red'
                player = {}
                for i in ['stand_l','stand_r','hurt_l','hurt_r','jump_l','jump_r'] + [f'walk{str(j+1).zfill(2)}_l' for j in range(11)] + [f'walk{str(j+1).zfill(2)}_r' for j in range(11)]:
                    player[i] = pygame.image.load(f'assets/images/player/{player_color}/{i}.png')

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and air_time == 0:
            player_jump = 10
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            for j in range(3):
                go = True
                for i in [5,35,69]:
                    try:
                        color = map.get_at([round(position[0]*70),round(position[1]*70+i)])
                    except:
                        color = (999,999,999,999)
                    if color == (0,0,0,255):
                        go = False
                if go:
                    position[0] -= .07
            if air_time == 0:
                player_state = f'walk{str(player_walk_cycle).zfill(2)}_l'
                player_walk_cycle += 1
            else:
                player_state = 'walk04_l'
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            for j in range(3):
                go = True
                for i in [5,35,69]:
                    try:
                        color = map.get_at([round(position[0]*70+70),round(position[1]*70+i)])
                    except:
                        color = (999,999,999,999)
                    if color == (0,0,0,255):
                        go = False
                if go:
                    position[0] += .07
            if air_time == 0:
                player_state = f'walk{str(player_walk_cycle).zfill(2)}_r'
                player_walk_cycle += 1
            else:
                player_state = 'walk04_r'
        else:
            rot = player_state[-1]
            player_state = f'stand_{rot}'
        if player_walk_cycle == 12:
            player_walk_cycle = 1

        for i in [[36,48]]:
            try:
                color = map.get_at([round(position[0]*70+i[0]),round(position[1]*70+i[1])])
            except:
                color = (999,999,999,999)
            if (color == (255,0,0,255) and invicibility == 0) or color == (255,128,0,255):
                lives -= 1
                invicibility = 20
                rot = player_state[-1]
                player_hurt_timer = 10
            if color == (0,0,255,255):
                selected_map += 1
                try:
                    load_map(selected_map)
                except:
                    run = False
                    win = True
                total_coins += player_coins
            if color == (255,0,255,255):
                player_jump = 15
                air_time = 0
                for j in trampolines:
                    if j[0] == round(position[0]) and j[1] == round(position[1]+.3):
                        trampolines[trampolines.index(j)][2] = 'down'
                        trampolines[trampolines.index(j)][3] = 5
            if color == (0,255,0,255):
                for j in checkpoints:
                    checkpoints[checkpoints.index(j)][2] = False
                    if j[0] == round(position[0]) and j[1] == round(position[1]+.3):
                        checkpoints[checkpoints.index(j)][2] = True
                        player_checkpoint = [j[0],j[1]]
        for i in [[10,48]]:
            try:
                color = map.get_at([round(position[0]*70+i[0]),round(position[1]*70+i[1])])
            except:
                color = (999,999,999,999)
            if color == (255,0,255,255):
                player_jump = 15
                air_time = 0
                for j in trampolines:
                    if j[0] == round(position[0]-.5) and j[1] == round(position[1]+.3):
                        trampolines[trampolines.index(j)][2] = 'down'
                        trampolines[trampolines.index(j)][3] = 5
        for i in [[62,48]]:
            try:
                color = map.get_at([round(position[0]*70+i[0]),round(position[1]*70+i[1])])
            except:
                color = (999,999,999,999)
            if color == (255,0,255,255):
                player_jump = 15
                air_time = 0
                for j in trampolines:
                    if j[0] == round(position[0]+.5) and j[1] == round(position[1]+.3):
                        trampolines[trampolines.index(j)][2] = 'down'
                        trampolines[trampolines.index(j)][3] = 5

        if player_jump != 0:
            jump = True
            for i in [10,35,60]:
                try:
                    color = map.get_at([round(position[0]*70+i),round(position[1]*70)])
                except:
                    color = (999,999,999,999)
                if color == (0,0,0,255):
                    jump = False
            if jump:
                position[1] -= player_jump / 20
                player_jump -= 1
                air_time += 1
            else:
                player_jump = 0

        if position[0]*70-screen_position[0] > 1000:
            screen_position[0] -= 1000 - (position[0]*70-screen_position[0])
        if position[0]*70-screen_position[0] < 600:
            screen_position[0] += (position[0]*70-screen_position[0]) - 600
        if position[1]*70-screen_position[1] > 563:
            screen_position[1] -= 563 - (position[1]*70-screen_position[1])
        if position[1]*70-screen_position[1] < 337:
            screen_position[1] += (position[1]*70-screen_position[1]) - 337
        if screen_position[0] < 0:
            screen_position[0] = 0
        if screen_position[1] < -55:
            screen_position[1] = -55
        if not invicibility == 0:
            invicibility -= 1
        if lives <= 0:
            position = player_checkpoint.copy()
            lives = 3
            invicibility = 0
            player_hurt_timer = 0
            player_jump = 0
            air_time = 0

        for i in trampolines:
            if i[3] == 0:
                trampolines[trampolines.index(i)][2] = 'up'
            else:
                trampolines[trampolines.index(i)][3] -= 1

        for i in coins:
            if i[0] == round(position[0]) and i[1] == round(position[1]):
                player_coins += 1
                del coins[coins.index(i)]
                break

        if player_jump == 0:
            fall = True
            for i in [10,35,60]:
                try:
                    color = map.get_at([round(position[0]*70+i),round(position[1]*70+70)])
                except:
                    color = (999,999,999,999)
                if color == (0,0,0,255):
                    fall = False
                    air_time = 0
            if fall:
                air_time += 3
                for j in range(0,air_time,1):
                    fall = True
                    for i in [10,35,60]:
                        try:
                            color = map.get_at([round(position[0]*70+i),round(position[1]*70+70)])
                        except:
                            color = (999,999,999,999)
                        if color == (0,0,0,255):
                            fall = False
                            air_time = 0
                    if fall:
                        position[1] += .01

        if player_hurt_timer != 0:
            player_state = f'hurt_{rot}'
            player_hurt_timer -= 1

        if frames_skipped >= frameskip:
            screen.fill('#d0f4f7')
            player_tmp = player[player_state].copy()
            if invicibility != 0:
                player_tmp.set_alpha(100)
            screen.blit(player_tmp,[position[0]*70-screen_position[0],position[1]*70-screen_position[1]-25])
            screen.blit(map_image[round(stage)],[-screen_position[0],-screen_position[1]])
            for i in trampolines:
                if i[2] == 'up':
                    screen.blit(trampoline_up,[i[0]*70-screen_position[0]+1,i[1]*70-screen_position[1]+1])
                if i[2] == 'down':
                    screen.blit(trampoline_down,[i[0]*70-screen_position[0]+1,i[1]*70-screen_position[1]+1])
            for i in checkpoints:
                if i[2] == True:
                    if round(stage) == 0:
                        screen.blit(checkpoint1,[i[0]*70-screen_position[0]+1,i[1]*70-screen_position[1]+1])
                    if round(stage) == 1:
                        screen.blit(checkpoint2,[i[0]*70-screen_position[0]+1,i[1]*70-screen_position[1]+1])
                if i[2] == False:
                    screen.blit(checkpoint0,[i[0]*70-screen_position[0]+1,i[1]*70-screen_position[1]+1])
            for i in coins:
                screen.blit(coin,[i[0]*70-screen_position[0],i[1]*70-screen_position[1]])
            pygame.draw.rect(screen,(0,0,0,255),pygame.Rect(0,0,1600,55))
            screen.blit(coin,[240,-10])
            screen.blit(font.render('× '+str(player_coins)+'/'+str(max_coins),True,(255,255,255,255)),[300,10])
            for i in range(3):
                if lives > i + 0.5:
                    screen.blit(heart_full,(5+i*60,5))
                elif lives == i + 0.5:
                    screen.blit(heart_half,(5+i*60,5))
                else:
                    screen.blit(heart_empty,(5+i*60,5))
            screen.blit(p1,[1000,5])
            screen.blit(p2,[1050,5])
            screen.blit(p3,[1100,5])
            pygame.display.flip()
            clock.tick(30)
            frames_skipped = 0
        frames_skipped += 1
        await asyncio.sleep(0)
    if win:
        screen.fill('black')
        run = True
        text = pygame.font.Font(size=55).render('Vyhrál jsi!',True,(255,255,255,255))
        screen.blit(text,(800 - text.get_width() / 2, 450 - text.get_height() / 2))
        text = pygame.font.Font(size=55).render('Získaných hvězdiček: ' + str(total_coins),True,(255,255,255,255))
        screen.blit(text,(800 - text.get_width() / 2, 500 - text.get_height() / 2))
        pygame.display.flip()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            await asyncio.sleep(0)
    pygame.display.quit()
    pygame.font.quit()

asyncio.run(main())
