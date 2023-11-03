import os
import pygame
import glob
import json
import random


pygame.init()

# #ff8800
# #00ff00
# #0000ff
# #ffff00
# #ff00e6
# 0 = nic
# 1 = zed
# 2 = bodaky
# 3 = bodaky shora
# 4 = falesna zed
# 5x = zmena
#  0 = normal
#  1 = lodicka
#  2 = sipka
#  3 = teleportovaci robutek
#  4 = ufo
# vyska = 20
# sirka = len(mapa[0])

file = '/'.join(os.path.abspath(__file__).split('/')[:-1])+'/'

zed = pygame.image.load(file+'obrazky/zed.png')
bodaky = pygame.image.load(file+'obrazky/bodaky.png')
bodaky.set_colorkey('#ffffff')
bodaky_shora = pygame.image.load(file+'obrazky/bodaky_shora.png')
bodaky_shora.set_colorkey('#ffffff')
zpet = pygame.image.load(file+'obrazky/zpet.png')
zpet.set_colorkey('#ffffff')
dal = pygame.image.load(file+'obrazky/dal.png')
dal.set_colorkey('#ffffff')
editor = pygame.image.load(file+'obrazky/editor.png')
editor.set_colorkey('#ffffff')
nic = pygame.image.load(file+'obrazky/nic.png')
nic.set_colorkey('#ffffff')
fal_zed = pygame.image.load(file+'obrazky/fales_zed.png')
fal_zed.set_colorkey('#ffffff')
zkusit = pygame.image.load(file+'obrazky/zkusit.png')
zkusit.set_colorkey('#ffffff')
ulozit = pygame.image.load(file+'obrazky/ulozit.png')
ulozit.set_colorkey('#ffffff')
editor_edit = pygame.image.load(file+'obrazky/editor_editovat.png')
editor_edit.set_colorkey('#ffffff')
hrac = []
for i in range(5):
    if i == 2:
        hrac.append(pygame.image.load(file+f'obrazky/hrac_21.png'))
        hrac[-1].set_colorkey('#ffffff')
    elif i == 3:
        hrac.append(pygame.image.load(file+f'obrazky/hrac_31.png'))
        hrac[-1].set_colorkey('#ffffff')
    else:
        hrac.append(pygame.image.load(file+f'obrazky/hrac_{i}.png'))
        hrac[-1].set_colorkey('#ffffff')
zmeny = []
for i in range(5):
    zmeny.append(pygame.image.load(file+f'obrazky/zmena_{i}.png'))
    zmeny[-1].set_colorkey('#ffffff')

veci = [nic,zed,bodaky,bodaky_shora,fal_zed]
veci += zmeny

#barvy = ['#ff8800','#00ff00','#0000ff','#ffff00','#ff00e6']
mapy = glob.glob(file+'mapy/*.json')
mapy.sort()
mapa_vybrana = 0

screen = pygame.display.set_mode((800,500))
run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
            run = False
        if (i.type == pygame.MOUSEBUTTONUP and i.button == 1) or (i.type == pygame.KEYUP and i.key == pygame.K_SPACE):
            if pygame.Rect(5,270,50,60).collidepoint(pygame.mouse.get_pos()):
                mapa_vybrana -= 1
            elif pygame.Rect(745,270,50,60).collidepoint(pygame.mouse.get_pos()):
                mapa_vybrana += 1
            elif pygame.Rect(10,10,60,60).collidepoint(pygame.mouse.get_pos()):
                pos = [100,0]
                running = True
                clock = pygame.time.Clock()
                mapa = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                vybrano = 1
                while running:
                    screen.fill('#ffff00')
                    for i in pygame.event.get():
                        if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                            running = False
                        if i.type == pygame.KEYDOWN and i.key == pygame.K_s:
                            vybrano += 1
                        if i.type == pygame.MOUSEBUTTONUP and pygame.Rect(380,430,60,60).collidepoint(pygame.mouse.get_pos()):
                            runx = True
                            napsano = ''
                            name_used = False
                            while runx:
                                screen.fill('#ffff00')
                                for i in pygame.event.get():
                                    if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                                        runx = False
                                    if i.type == pygame.KEYDOWN:
                                        if i.unicode in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-+':
                                            napsano += i.unicode
                                        elif i.key == pygame.K_RETURN:
                                            try:
                                                s = open('mapy/'+napsano+'.json','r')
                                                s.close()
                                                name_used = 200
                                            except:
                                                with open('mapy/'+napsano+'.json','w') as s:
                                                    mapa.reverse()
                                                    s.write(json.dumps({'mapa':mapa}))
                                                    mapa.reverse()
                                                    mapy = glob.glob('mapy/*.json')
                                                    runx = False
                                        elif i.key == pygame.K_BACKSPACE:
                                            napsano = napsano[:-1]
                                if name_used != False:
                                    font = pygame.font.SysFont('Arial',20)
                                    screen.blit(font.render('This name is used',True,(255,0,0)),(10,30))
                                    name_used -= 1
                                if name_used == 0:
                                    name_used = False
                                font = pygame.font.SysFont('Arial',20)
                                screen.blit(font.render('Map name: '+napsano,True,(0,0,0)),(10,10))
                                pygame.display.flip()
                        if i.type == pygame.MOUSEBUTTONUP and pygame.Rect(300,430,60,60).collidepoint(pygame.mouse.get_pos()):
                            try:
                                pos = [100,0]
                                runx = True
                                skoc = 0
                                smer = 1
                                typ = 0
                                cekej = 0
                                updown = 1
                                clock = pygame.time.Clock()
                                while runx:
                                    screen.fill('#ffff00')
                                    for i in pygame.event.get():
                                        if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                                            runx = False
                                    if typ == 0:
                                        if pos[1] % 20 == 0 and (mapa[pos[1]//20-1][pos[0]//20-1] == 1 or mapa[pos[1]//20-1][pos[0]//20] == 1 or pos[1] == 0) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            skoc = 14
                                        if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                            pos[1] -= 4
                                        if skoc > 0:
                                            pos[1] += skoc
                                            skoc -= 1
                                        if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                            pos[1] = round(pos[1]/20)*20
                                    if typ == 1:
                                        if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            pos[1] += 4
                                        if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                            pos[1] -= 2
                                        if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                            pos[1] = round(pos[1]/20)*20
                                    if typ == 2:
                                        if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            if smer == 1:
                                                smer = -1
                                            elif smer == -1:
                                                smer = 1
                                            cekej = 15
                                        if cekej != 0:
                                            cekej -= 1
                                        if smer == 1:
                                            pos[1] += 2
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_21.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                        elif smer == -1:
                                            pos[1] -= 2
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_2-1.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                    if typ == 3:
                                        if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            if updown == 1:
                                                updown = -1
                                            elif updown == -1:
                                                updown = 1
                                            cekej = 15
                                        if cekej != 0:
                                            cekej -= 1
                                        if updown == 1:
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_31.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 9
                                            if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                pos[1] = round(pos[1]/20)*20
                                        elif updown == -1:
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_3-1.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                            if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1):
                                                pos[1] += 9
                                            if mapa[pos[1]//20][pos[0]//20+1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20+1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                pos[1] = round(pos[1]/20)*20
                                    if typ == 4:
                                        if skoc < 1 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            skoc = 10
                                        if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                            pos[1] -= 3
                                        if skoc > 0:
                                            pos[1] += skoc
                                            skoc -= 1
                                        if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                            pos[1] = round(pos[1]/20)*20
                                    if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20-1] == 2 or mapa[pos[1]//20][pos[0]//20-1] == 3 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20][pos[0]//20] == 2 or mapa[pos[1]//20][pos[0]//20] == 3:
                                        pos = [100,0]
                                        typ = 0
                                    if pos[1] >= 380:
                                        pos[1] = 380
                                    if pos[1] <= 0:
                                        pos[1] = 0
                                    pos[0] += 2
                                    if str(mapa[pos[1]//20][pos[0]//20-1])[0] == '5':
                                        skoc = 0
                                        smer = 1
                                        cekej = 0
                                        updown = 1
                                        typ = int(str(mapa[pos[1]//20][pos[0]//20-1])[1])
                                    if str(mapa[pos[1]//20][pos[0]//20])[0] == '5':
                                        skoc = 0
                                        smer = 1
                                        cekej = 0
                                        updown = 1
                                        typ = int(str(mapa[pos[1]//20][pos[0]//20])[1])
                                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                                        if typ == 0:
                                            if pos[1] % 20 == 0 and (mapa[pos[1]//20-1][pos[0]//20-1] == 1 or mapa[pos[1]//20-1][pos[0]//20] == 1 or pos[1] == 0) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                skoc = 14
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 4
                                            if skoc > 0:
                                                pos[1] += skoc
                                                skoc -= 1
                                            if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                                pos[1] = round(pos[1]/20)*20
                                        if typ == 1:
                                            if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                pos[1] += 4
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 2
                                            if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                pos[1] = round(pos[1]/20)*20
                                        if typ == 2:
                                            if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                if smer == 1:
                                                    smer = -1
                                                elif smer == -1:
                                                    smer = 1
                                                cekej = 15
                                            if cekej != 0:
                                                cekej -= 1
                                            if smer == 1:
                                                pos[1] += 2
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_21.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                            elif smer == -1:
                                                pos[1] -= 2
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_2-1.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                        if typ == 3:
                                            if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                if updown == 1:
                                                    updown = -1
                                                elif updown == -1:
                                                    updown = 1
                                                cekej = 15
                                            if cekej != 0:
                                                cekej -= 1
                                            if updown == 1:
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_31.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                                if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                    pos[1] -= 9
                                                if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                    pos[1] = round(pos[1]/20)*20
                                            elif updown == -1:
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_3-1.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                                if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1):
                                                    pos[1] += 9
                                                if mapa[pos[1]//20][pos[0]//20+1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20+1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                    pos[1] = round(pos[1]/20)*20
                                        if typ == 4:
                                            if skoc < 1 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                skoc = 10
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 3
                                            if skoc > 0:
                                                pos[1] += skoc
                                                skoc -= 1
                                            if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                                pos[1] = round(pos[1]/20)*20
                                        if (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20-1] == 2 or mapa[pos[1]//20][pos[0]//20-1] == 3 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20][pos[0]//20] == 2 or mapa[pos[1]//20][pos[0]//20] == 3) and not pygame.key.get_pressed[pygame.K_LCTRL]:
                                            pos = [100,0]
                                            typ = 0
                                        if pos[1] >= 380:
                                            pos[1] = 380
                                        if pos[1] <= 0:
                                            pos[1] = 0
                                        pos[0] += 2
                                        if str(mapa[pos[1]//20][pos[0]//20-1])[0] == '5':
                                            skoc = 0
                                            smer = 1
                                            cekej = 0
                                            updown = 1
                                            typ = int(str(mapa[pos[1]//20][pos[0]//20-1])[1])
                                        if str(mapa[pos[1]//20][pos[0]//20])[0] == '5':
                                            skoc = 0
                                            smer = 1
                                            cekej = 0
                                            updown = 1
                                            typ = int(str(mapa[pos[1]//20][pos[0]//20])[1])
                                    for y,ym in zip(range(0,500,20),range(20)):
                                        for x,xm in zip(range(-(pos[0]%20),800+pos[0]%20,20),range(pos[0]//20-3,pos[0]//20+38)):
                                            try:
                                                if xm >= 0:
                                                    if mapa[ym][xm] == 1 or mapa[ym][xm] == 4:
                                                        screen.blit(zed,(x,380-y))
                                                    if mapa[ym][xm] == 2:
                                                        screen.blit(bodaky,(x,380-y))
                                                    if mapa[ym][xm] == 3:
                                                        screen.blit(bodaky_shora,(x,380-y))
                                                    if str(mapa[ym][xm])[0] == '5':
                                                        screen.blit(zmeny[int(str(mapa[ym][xm])[1])],(x,380-y))
                                            except:
                                                pygame.draw.rect(screen,'#00ffff',pygame.Rect(x,0,10,400))
                                                break
                                    # hrac[typ] = pygame.transform.rotate(hrac[typ],smer)
                                    # hrac[typ].set_colorkey('#ffffff')
                                    screen.blit(hrac[typ],(40,(380-pos[1])))
                                    pygame.draw.rect(screen,'#f0f000',pygame.Rect(0,400,800,200))
                                    pygame.display.flip()
                                    clock.tick(60)
                            except:
                                pos = [100,0]
                    if vybrano == 10:
                        vybrano = 0
                    if pygame.key.get_pressed()[pygame.K_a]:
                        if pos[0] > 100:
                            pos[0] -= 5
                        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            if pos[0] > 100:
                                pos[0] -= 10
                    if pygame.key.get_pressed()[pygame.K_d]:
                        pos[0] += 5
                        while True:
                            try:
                                mapa[0][pos[0]//20+40]
                                break
                            except:
                                for i in mapa:
                                    i += [0]
                        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            pos[0] += 10
                            while True:
                                try:
                                    mapa[0][pos[0]//20+40]
                                    break
                                except:
                                    for i in mapa:
                                        i += [0]
                    if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1] < 400:
                        if vybrano == 0 or vybrano == 1 or vybrano == 2 or vybrano == 3 or vybrano == 4:
                            mapa[(400-pygame.mouse.get_pos()[1])//20][(pos[0]+pygame.mouse.get_pos()[0])//20-3] = vybrano
                        else:
                            mapa[(400-pygame.mouse.get_pos()[1])//20][(pos[0]+pygame.mouse.get_pos()[0])//20-3] = int('5'+str(vybrano-5))
                    if pygame.mouse.get_pressed()[2] and pygame.mouse.get_pos()[1] < 400:
                        mapa[(400-pygame.mouse.get_pos()[1])//20][(pos[0]+pygame.mouse.get_pos()[0])//20-3] = 0
                    if pygame.mouse.get_pressed()[0]:
                        for x in range(len(veci)):
                            if pygame.Rect(10+x*25,450,20,20).collidepoint(pygame.mouse.get_pos()):
                                vybrano = x
                    for y,ym in zip(range(0,500,20),range(20)):
                        for x,xm in zip(range(-(pos[0]%20),800+pos[0]%20,20),range(pos[0]//20-3,pos[0]//20+38)):
                            try:
                                if xm >= 0:
                                    if mapa[ym][xm] == 1:
                                        screen.blit(zed,(x,380-y))
                                    if mapa[ym][xm] == 4:
                                        screen.blit(fal_zed,(x,380-y))
                                    if mapa[ym][xm] == 2:
                                        screen.blit(bodaky,(x,380-y))
                                    if mapa[ym][xm] == 3:
                                        screen.blit(bodaky_shora,(x,380-y))
                                    if str(mapa[ym][xm])[0] == '5':
                                        screen.blit(zmeny[int(str(mapa[ym][xm])[1])],(x,380-y))
                            except:
                                pass
                    pygame.draw.rect(screen,'#f0f000',pygame.Rect(0,400,800,200))
                    pygame.draw.circle(screen,'#f66151',(10+vybrano*25+10,460),15)
                    for x in range(len(veci)):
                        screen.blit(veci[x],(10+(x*25),450))
                    screen.blit(zkusit,(300,430))
                    screen.blit(ulozit,(380,430))
                    pygame.display.flip()
                    clock.tick(60)
            elif pygame.Rect(80,10,60,60).collidepoint(pygame.mouse.get_pos()):
                pos = [100,0]
                with open(mapy[mapa_vybrana]) as s:
                    mapa = json.loads(s.read())['mapa']
                    mapa.reverse()
                running = True
                clock = pygame.time.Clock()
                vybrano = 1
                while running:
                    screen.fill('#ffff00')
                    for i in pygame.event.get():
                        if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                            running = False
                        if i.type == pygame.KEYDOWN and i.key == pygame.K_s:
                            vybrano += 1
                        if i.type == pygame.MOUSEBUTTONUP and pygame.Rect(380,430,60,60).collidepoint(pygame.mouse.get_pos()):
                            runx = True
                            napsano = ''
                            name_used = False
                            while runx:
                                screen.fill('#ffff00')
                                for i in pygame.event.get():
                                    if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                                        runx = False
                                    if i.type == pygame.KEYDOWN:
                                        if i.unicode in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-+':
                                            napsano += i.unicode
                                        elif i.key == pygame.K_RETURN:
                                            try:
                                                s = open('mapy/'+napsano+'.json','r')
                                                s.close()
                                                name_used = 200
                                            except:
                                                with open('mapy/'+napsano+'.json','w') as s:
                                                    mapa.reverse()
                                                    s.write(json.dumps({'mapa':mapa}))
                                                    mapa.reverse()
                                                    mapy = glob.glob('mapy/*.json')
                                                    runx = False
                                        elif i.key == pygame.K_BACKSPACE:
                                            napsano = napsano[:-1]
                                if name_used != False:
                                    font = pygame.font.SysFont('Arial',20)
                                    screen.blit(font.render('This name is used',True,(255,0,0)),(10,30))
                                    name_used -= 1
                                if name_used == 0:
                                    name_used = False
                                font = pygame.font.SysFont('Arial',20)
                                screen.blit(font.render('Map name: '+napsano,True,(0,0,0)),(10,10))
                                pygame.display.flip()
                        if i.type == pygame.MOUSEBUTTONUP and pygame.Rect(300,430,60,60).collidepoint(pygame.mouse.get_pos()):
                            try:
                                pos = [100,0]
                                runx = True
                                skoc = 0
                                smer = 1
                                typ = 0
                                cekej = 0
                                updown = 1
                                clock = pygame.time.Clock()
                                while runx:
                                    screen.fill('#ffff00')
                                    for i in pygame.event.get():
                                        if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                                            runx = False
                                    if typ == 0:
                                        if pos[1] % 20 == 0 and (mapa[pos[1]//20-1][pos[0]//20-1] == 1 or mapa[pos[1]//20-1][pos[0]//20] == 1 or pos[1] == 0) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            skoc = 14
                                        if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                            pos[1] -= 4
                                        if skoc > 0:
                                            pos[1] += skoc
                                            skoc -= 1
                                        if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                            pos[1] = round(pos[1]/20)*20
                                    if typ == 1:
                                        if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            pos[1] += 4
                                        if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                            pos[1] -= 2
                                        if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                            pos[1] = round(pos[1]/20)*20
                                    if typ == 2:
                                        if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            if smer == 1:
                                                smer = -1
                                            elif smer == -1:
                                                smer = 1
                                            cekej = 15
                                        if cekej != 0:
                                            cekej -= 1
                                        if smer == 1:
                                            pos[1] += 2
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_21.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                        elif smer == -1:
                                            pos[1] -= 2
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_2-1.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                    if typ == 3:
                                        if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            if updown == 1:
                                                updown = -1
                                            elif updown == -1:
                                                updown = 1
                                            cekej = 15
                                        if cekej != 0:
                                            cekej -= 1
                                        if updown == 1:
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_31.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 9
                                            if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                pos[1] = round(pos[1]/20)*20
                                        elif updown == -1:
                                            hrac[typ] = pygame.image.load(file+'obrazky/hrac_3-1.png')
                                            hrac[typ].set_colorkey('#ffffff')
                                            if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1):
                                                pos[1] += 9
                                            if mapa[pos[1]//20][pos[0]//20+1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20+1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                pos[1] = round(pos[1]/20)*20
                                    if typ == 4:
                                        if skoc < 1 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                            skoc = 10
                                        if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                            pos[1] -= 3
                                        if skoc > 0:
                                            pos[1] += skoc
                                            skoc -= 1
                                        if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                            pos[1] = round(pos[1]/20)*20
                                    if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20-1] == 2 or mapa[pos[1]//20][pos[0]//20-1] == 3 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20][pos[0]//20] == 2 or mapa[pos[1]//20][pos[0]//20] == 3:
                                        pos = [100,0]
                                        typ = 0
                                    if pos[1] >= 380:
                                        pos[1] = 380
                                    if pos[1] <= 0:
                                        pos[1] = 0
                                    pos[0] += 2
                                    if str(mapa[pos[1]//20][pos[0]//20-1])[0] == '5':
                                        skoc = 0
                                        smer = 1
                                        cekej = 0
                                        updown = 1
                                        typ = int(str(mapa[pos[1]//20][pos[0]//20-1])[1])
                                    if str(mapa[pos[1]//20][pos[0]//20])[0] == '5':
                                        skoc = 0
                                        smer = 1
                                        cekej = 0
                                        updown = 1
                                        typ = int(str(mapa[pos[1]//20][pos[0]//20])[1])
                                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                                        if typ == 0:
                                            if pos[1] % 20 == 0 and (mapa[pos[1]//20-1][pos[0]//20-1] == 1 or mapa[pos[1]//20-1][pos[0]//20] == 1 or pos[1] == 0) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                skoc = 14
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 4
                                            if skoc > 0:
                                                pos[1] += skoc
                                                skoc -= 1
                                            if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                                pos[1] = round(pos[1]/20)*20
                                        if typ == 1:
                                            if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                pos[1] += 4
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 2
                                            if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                pos[1] = round(pos[1]/20)*20
                                        if typ == 2:
                                            if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                if smer == 1:
                                                    smer = -1
                                                elif smer == -1:
                                                    smer = 1
                                                cekej = 15
                                            if cekej != 0:
                                                cekej -= 1
                                            if smer == 1:
                                                pos[1] += 2
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_21.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                            elif smer == -1:
                                                pos[1] -= 2
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_2-1.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                        if typ == 3:
                                            if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                if updown == 1:
                                                    updown = -1
                                                elif updown == -1:
                                                    updown = 1
                                                cekej = 15
                                            if cekej != 0:
                                                cekej -= 1
                                            if updown == 1:
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_31.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                                if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                    pos[1] -= 9
                                                if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                    pos[1] = round(pos[1]/20)*20
                                            elif updown == -1:
                                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_3-1.png')
                                                hrac[typ].set_colorkey('#ffffff')
                                                if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1):
                                                    pos[1] += 9
                                                if mapa[pos[1]//20][pos[0]//20+1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20+1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                                    pos[1] = round(pos[1]/20)*20
                                        if typ == 4:
                                            if skoc < 1 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                                skoc = 10
                                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                                pos[1] -= 3
                                            if skoc > 0:
                                                pos[1] += skoc
                                                skoc -= 1
                                            if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                                pos[1] = round(pos[1]/20)*20
                                        if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20-1] == 2 or mapa[pos[1]//20][pos[0]//20-1] == 3 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20][pos[0]//20] == 2 or mapa[pos[1]//20][pos[0]//20] == 3:
                                            pos = [100,0]
                                            typ = 0
                                        if pos[1] >= 380:
                                            pos[1] = 380
                                        if pos[1] <= 0:
                                            pos[1] = 0
                                        pos[0] += 2
                                        if str(mapa[pos[1]//20][pos[0]//20-1])[0] == '5':
                                            skoc = 0
                                            smer = 1
                                            cekej = 0
                                            updown = 1
                                            typ = int(str(mapa[pos[1]//20][pos[0]//20-1])[1])
                                        if str(mapa[pos[1]//20][pos[0]//20])[0] == '5':
                                            skoc = 0
                                            smer = 1
                                            cekej = 0
                                            updown = 1
                                            typ = int(str(mapa[pos[1]//20][pos[0]//20])[1])
                                    for y,ym in zip(range(0,500,20),range(20)):
                                        for x,xm in zip(range(-(pos[0]%20),800+pos[0]%20,20),range(pos[0]//20-3,pos[0]//20+38)):
                                            try:
                                                if xm >= 0:
                                                    if mapa[ym][xm] == 1 or mapa[ym][xm] == 4:
                                                        screen.blit(zed,(x,380-y))
                                                    if mapa[ym][xm] == 2:
                                                        screen.blit(bodaky,(x,380-y))
                                                    if mapa[ym][xm] == 3:
                                                        screen.blit(bodaky_shora,(x,380-y))
                                                    if str(mapa[ym][xm])[0] == '5':
                                                        screen.blit(zmeny[int(str(mapa[ym][xm])[1])],(x,380-y))
                                            except:
                                                pygame.draw.rect(screen,'#00ffff',pygame.Rect(x,0,10,400))
                                                break
                                    # hrac[typ] = pygame.transform.rotate(hrac[typ],smer)
                                    # hrac[typ].set_colorkey('#ffffff')
                                    screen.blit(hrac[typ],(40,(380-pos[1])))
                                    pygame.draw.rect(screen,'#f0f000',pygame.Rect(0,400,800,200))
                                    pygame.display.flip()
                                    clock.tick(60)
                            except:
                                pos = [100,0]
                    if vybrano == 10:
                        vybrano = 0
                    if pygame.key.get_pressed()[pygame.K_a]:
                        if pos[0] > 100:
                            pos[0] -= 5
                        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            if pos[0] > 100:
                                pos[0] -= 10
                    if pygame.key.get_pressed()[pygame.K_d]:
                        pos[0] += 5
                        while True:
                            try:
                                mapa[0][pos[0]//20+40]
                                break
                            except:
                                for i in mapa:
                                    i += [0]
                        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            pos[0] += 10
                            while True:
                                try:
                                    mapa[0][pos[0]//20+40]
                                    break
                                except:
                                    for i in mapa:
                                        i += [0]
                    if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1] < 400:
                        if vybrano == 0 or vybrano == 1 or vybrano == 2 or vybrano == 3 or vybrano == 4:
                            mapa[(400-pygame.mouse.get_pos()[1])//20][(pos[0]+pygame.mouse.get_pos()[0])//20-3] = vybrano
                        else:
                            mapa[(400-pygame.mouse.get_pos()[1])//20][(pos[0]+pygame.mouse.get_pos()[0])//20-3] = int('5'+str(vybrano-5))
                    if pygame.mouse.get_pressed()[2] and pygame.mouse.get_pos()[1] < 400:
                        mapa[(400-pygame.mouse.get_pos()[1])//20][(pos[0]+pygame.mouse.get_pos()[0])//20-3] = 0
                    if pygame.mouse.get_pressed()[0]:
                        for x in range(len(veci)):
                            if pygame.Rect(10+x*25,450,20,20).collidepoint(pygame.mouse.get_pos()):
                                vybrano = x
                    for y,ym in zip(range(0,500,20),range(20)):
                        for x,xm in zip(range(-(pos[0]%20),800+pos[0]%20,20),range(pos[0]//20-3,pos[0]//20+38)):
                            try:
                                if xm >= 0:
                                    if mapa[ym][xm] == 1:
                                        screen.blit(zed,(x,380-y))
                                    if mapa[ym][xm] == 4:
                                        screen.blit(fal_zed,(x,380-y))
                                    if mapa[ym][xm] == 2:
                                        screen.blit(bodaky,(x,380-y))
                                    if mapa[ym][xm] == 3:
                                        screen.blit(bodaky_shora,(x,380-y))
                                    if str(mapa[ym][xm])[0] == '5':
                                        screen.blit(zmeny[int(str(mapa[ym][xm])[1])],(x,380-y))
                            except:
                                pass
                    pygame.draw.rect(screen,'#f0f000',pygame.Rect(0,400,800,200))
                    pygame.draw.circle(screen,'#f66151',(10+vybrano*25+10,460),15)
                    for x in range(len(veci)):
                        screen.blit(veci[x],(10+(x*25),450))
                    screen.blit(zkusit,(300,430))
                    screen.blit(ulozit,(380,430))
                    pygame.display.flip()
                    clock.tick(60)
            else:
                try:
                    pos = [100,0]
                    with open(mapy[mapa_vybrana]) as s:
                        mapa = json.loads(s.read())['mapa']
                        mapa.reverse()
                    running = True
                    skoc = 0
                    smer = 1
                    typ = 0
                    cekej = 0
                    updown = 1
                    clock = pygame.time.Clock()
                    while running:
                        screen.fill('#ffff00')
                        for i in pygame.event.get():
                            if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                                running = False
                        if typ == 0:
                            if pos[1] % 20 == 0 and (mapa[pos[1]//20-1][pos[0]//20-1] == 1 or mapa[pos[1]//20-1][pos[0]//20] == 1 or pos[1] == 0) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                skoc = 14
                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                pos[1] -= 4
                            if skoc > 0:
                                pos[1] += skoc
                                skoc -= 1
                            if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                pos[1] = round(pos[1]/20)*20
                        if typ == 1:
                            if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                pos[1] += 4
                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                pos[1] -= 2
                            if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                pos[1] = round(pos[1]/20)*20
                        if typ == 2:
                            if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                if smer == 1:
                                    smer = -1
                                elif smer == -1:
                                    smer = 1
                                cekej = 15
                            if cekej != 0:
                                cekej -= 1
                            if smer == 1:
                                pos[1] += 2
                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_21.png')
                                hrac[typ].set_colorkey('#ffffff')
                            elif smer == -1:
                                pos[1] -= 2
                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_2-1.png')
                                hrac[typ].set_colorkey('#ffffff')
                        if typ == 3:
                            if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                if updown == 1:
                                    updown = -1
                                elif updown == -1:
                                    updown = 1
                                cekej = 15
                            if cekej != 0:
                                cekej -= 1
                            if updown == 1:
                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_31.png')
                                hrac[typ].set_colorkey('#ffffff')
                                if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                    pos[1] -= 9
                                if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                    pos[1] = round(pos[1]/20)*20
                            elif updown == -1:
                                hrac[typ] = pygame.image.load(file+'obrazky/hrac_3-1.png')
                                hrac[typ].set_colorkey('#ffffff')
                                if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1):
                                    pos[1] += 9
                                if mapa[pos[1]//20][pos[0]//20+1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20+1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                    pos[1] = round(pos[1]/20)*20
                        if typ == 4:
                            if skoc < 1 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                skoc = 10
                            if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                pos[1] -= 3
                            if skoc > 0:
                                pos[1] += skoc
                                skoc -= 1
                            if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                pos[1] = round(pos[1]/20)*20
                        if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20-1] == 2 or mapa[pos[1]//20][pos[0]//20-1] == 3 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20][pos[0]//20] == 2 or mapa[pos[1]//20][pos[0]//20] == 3:
                            pos = [100,0]
                            typ = 0
                        if pos[1] >= 380:
                            pos[1] = 380
                        if pos[1] <= 0:
                            pos[1] = 0
                        pos[0] += 2
                        if str(mapa[pos[1]//20][pos[0]//20-1])[0] == '5':
                            skoc = 0
                            smer = 1
                            cekej = 0
                            updown = 1
                            typ = int(str(mapa[pos[1]//20][pos[0]//20-1])[1])
                        if str(mapa[pos[1]//20][pos[0]//20])[0] == '5':
                            skoc = 0
                            smer = 1
                            cekej = 0
                            updown = 1
                            typ = int(str(mapa[pos[1]//20][pos[0]//20])[1])
                        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            if typ == 0:
                                if pos[1] % 20 == 0 and (mapa[pos[1]//20-1][pos[0]//20-1] == 1 or mapa[pos[1]//20-1][pos[0]//20] == 1 or pos[1] == 0) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                    skoc = 14
                                if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                    pos[1] -= 4
                                if skoc > 0:
                                    pos[1] += skoc
                                    skoc -= 1
                                if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                    pos[1] = round(pos[1]/20)*20
                            if typ == 1:
                                if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1) and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                    pos[1] += 4
                                if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                    pos[1] -= 2
                                if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                    pos[1] = round(pos[1]/20)*20
                            if typ == 2:
                                if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                    if smer == 1:
                                        smer = -1
                                    elif smer == -1:
                                        smer = 1
                                    cekej = 15
                                if cekej != 0:
                                    cekej -= 1
                                if smer == 1:
                                    pos[1] += 2
                                    hrac[typ] = pygame.image.load(file+'obrazky/hrac_21.png')
                                    hrac[typ].set_colorkey('#ffffff')
                                elif smer == -1:
                                    pos[1] -= 2
                                    hrac[typ] = pygame.image.load(file+'obrazky/hrac_2-1.png')
                                    hrac[typ].set_colorkey('#ffffff')
                            if typ == 3:
                                if cekej == 0 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                    if updown == 1:
                                        updown = -1
                                    elif updown == -1:
                                        updown = 1
                                    cekej = 15
                                if cekej != 0:
                                    cekej -= 1
                                if updown == 1:
                                    hrac[typ] = pygame.image.load(file+'obrazky/hrac_31.png')
                                    hrac[typ].set_colorkey('#ffffff')
                                    if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                        pos[1] -= 9
                                    if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                        pos[1] = round(pos[1]/20)*20
                                elif updown == -1:
                                    hrac[typ] = pygame.image.load(file+'obrazky/hrac_3-1.png')
                                    hrac[typ].set_colorkey('#ffffff')
                                    if not (mapa[pos[1]//20+1][pos[0]//20-1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1):
                                        pos[1] += 9
                                    if mapa[pos[1]//20][pos[0]//20+1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20+1][pos[0]//20+1] == 1 or mapa[pos[1]//20+1][pos[0]//20] == 1:
                                        pos[1] = round(pos[1]/20)*20
                            if typ == 4:
                                if skoc < 1 and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
                                    skoc = 10
                                if not (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1) and not pos[1] == 0:
                                    pos[1] -= 3
                                if skoc > 0:
                                    pos[1] += skoc
                                    skoc -= 1
                                if (not skoc > 0) and (mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20] == 1):
                                    pos[1] = round(pos[1]/20)*20
                            if mapa[pos[1]//20][pos[0]//20-1] == 1 or mapa[pos[1]//20][pos[0]//20-1] == 2 or mapa[pos[1]//20][pos[0]//20-1] == 3 or mapa[pos[1]//20][pos[0]//20] == 1 or mapa[pos[1]//20][pos[0]//20] == 2 or mapa[pos[1]//20][pos[0]//20] == 3:
                                pos = [100,0]
                                typ = 0
                            if pos[1] >= 380:
                                pos[1] = 380
                            if pos[1] <= 0:
                                pos[1] = 0
                            pos[0] += 2
                            if str(mapa[pos[1]//20][pos[0]//20-1])[0] == '5':
                                skoc = 0
                                smer = 1
                                cekej = 0
                                updown = 1
                                typ = int(str(mapa[pos[1]//20][pos[0]//20-1])[1])
                            if str(mapa[pos[1]//20][pos[0]//20])[0] == '5':
                                skoc = 0
                                smer = 1
                                cekej = 0
                                updown = 1
                                typ = int(str(mapa[pos[1]//20][pos[0]//20])[1])
                        for y,ym in zip(range(0,500,20),range(20)):
                            for x,xm in zip(range(-(pos[0]%20),800+pos[0]%20,20),range(pos[0]//20-3,pos[0]//20+38)):
                                try:
                                    if xm >= 0:
                                        if mapa[ym][xm] == 1 or mapa[ym][xm] == 4:
                                            screen.blit(zed,(x,380-y))
                                        if mapa[ym][xm] == 2:
                                            screen.blit(bodaky,(x,380-y))
                                        if mapa[ym][xm] == 3:
                                            screen.blit(bodaky_shora,(x,380-y))
                                        if str(mapa[ym][xm])[0] == '5':
                                            screen.blit(zmeny[int(str(mapa[ym][xm])[1])],(x,380-y))
                                except:
                                    pygame.draw.rect(screen,'#00ffff',pygame.Rect(x,0,10,400))
                                    break
                        # hrac[typ] = pygame.transform.rotate(hrac[typ],smer)
                        # hrac[typ].set_colorkey('#ffffff')
                        screen.blit(hrac[typ],(40,(380-pos[1])))
                        pygame.draw.rect(screen,'#f0f000',pygame.Rect(0,400,800,200))
                        pygame.display.flip()
                        clock.tick(60)
                except:
                    pass
        if i.type == pygame.MOUSEWHEEL:
            if i.y == 1:
                mapa_vybrana += 1
            if i.y == -1:
                mapa_vybrana -= 1
    if mapa_vybrana >= len(mapy):
        mapa_vybrana = 0
    if mapa_vybrana <= -1:
        mapa_vybrana = len(mapy)-1
    screen.fill('#ffff00')
    screen.blit(zpet,(5,270))
    screen.blit(dal,(745,270))
    screen.blit(editor,(10,10))
    screen.blit(editor_edit,(80,10))
    font = pygame.font.SysFont('Arial',20)
    try:
        screen.blit(font.render(mapy[mapa_vybrana].split('/')[-1][0:-5],True,(0,0,0)),(300,290))
    except:
        pass
    pygame.display.update()
    pygame.display.flip()

