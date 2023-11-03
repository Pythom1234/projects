

import pygame
import random
import time

#             [1]
#pruchod = [0] X [2]
#             [3]
#
# jmeno: krysa pavouk mumie klicnik sermir sekernik duch drak
# sila:    5     6      7      8      9       10     12   15
# dava:  zbran kouzlo kouzlo klic   zbran    zbran truhla truhla
# dava:  dyky uzdra- magicky         mec    sekera
#              veni    mec

pygame.init()


class Dilek_I:
    def __init__(self,x,y,rot=0):
        self.rot = rot
        self.y = y
        self.x = x
        self.obr = pygame.transform.rotate(pygame.image.load('obrazky/I.png'),self.rot)
        if self.rot == 0 or self.rot == 180:
            self.pruchod = [0,1,0,1]
        elif self.rot == 90 or self.rot == -90:
            self.pruchod = [1,0,1,0]
    def nakresli(self):
        mapa.blit(self.obr,(self.x*40,self.y*40))
class Dilek_L:
    def __init__(self,x,y,rot=0):
        self.rot = rot
        self.y = y
        self.x = x
        self.obr = pygame.transform.rotate(pygame.image.load('obrazky/L.png'),self.rot)
        if self.rot == 0:
            self.pruchod = [0,1,1,0]
        elif self.rot == 90:
            self.pruchod = [1,1,0,0]
        elif self.rot == 180:
            self.pruchod = [1,0,0,1]
        elif self.rot == -90:
            self.pruchod = [0,0,1,1]
    def nakresli(self):
        mapa.blit(self.obr,(self.x*40,self.y*40))
class Dilek_T:
    def __init__(self,x,y,rot=0):
        self.rot = rot
        self.y = y
        self.x = x
        self.obr = pygame.transform.rotate(pygame.image.load('obrazky/T.png'),self.rot)
        if self.rot == 0:
            self.pruchod = [1,0,1,1]
        elif self.rot == 90:
            self.pruchod = [0,1,1,1]
        elif self.rot == 180:
            self.pruchod = [1,1,1,0]
        elif self.rot == -90:
            self.pruchod = [1,1,0,1]
    def nakresli(self):
        mapa.blit(self.obr,(self.x*40,self.y*40))
class Dilek_X:
    def __init__(self,x,y,rot=0):
        self.rot = rot
        self.y = y
        self.x = x
        self.obr = pygame.transform.rotate(pygame.image.load('obrazky/X.png'),self.rot)
        self.pruchod = [1,1,1,1]
    def nakresli(self):
        mapa.blit(self.obr,(self.x*40,self.y*40))

class Potvora:
    def __init__(self,x,y):
        self.pos = [x,y]
    def nakresli(self):
        screen.blit(self.obr,(self.pos[0]*40+12,self.pos[1]*40+12))

class Krysa(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'krysa'
        self.sila = 5
        self.obr = pygame.image.load('obrazky/zmensene14/krysa.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'dyky'
        super().__init__(x,y)
class Pavouk(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'pavouk'
        self.sila = 6
        self.obr = pygame.image.load('obrazky/zmensene14/pavouk.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'uzdraveni'
        super().__init__(x,y)
class Mumie(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'mumie'
        self.sila = 7
        self.obr = pygame.image.load('obrazky/zmensene14/mumie.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'magicky_mec'
        super().__init__(x,y)
class Klicnik(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'klíčník'
        self.sila = 8
        self.obr = pygame.image.load('obrazky/zmensene14/klicnik.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'klic'
        super().__init__(x,y)
class Sermir(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'šermíř'
        self.sila = 9
        self.obr = pygame.image.load('obrazky/zmensene14/sermir.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'mec'
        super().__init__(x,y)
class Sekernik(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'sekerník'
        self.sila = 10
        self.obr = pygame.image.load('obrazky/zmensene14/sekernik.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'sekera'
        super().__init__(x,y)
class Duch(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'duch'
        self.sila = 12
        self.obr = pygame.image.load('obrazky/zmensene14/duch.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'truhla'
        super().__init__(x,y)
class Drak(Potvora):
    def __init__(self,x,y):
        self.jmeno = 'drak'
        self.sila = 15
        self.obr = pygame.image.load('obrazky/zmensene14/drak.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'truhla+'
        super().__init__(x,y)
class Truhla():
    def __init__(self,x,y):
        self.pos = [x,y]
        self.jmeno = 'truhla'
        self.sila = '0'
        self.obr = pygame.image.load('obrazky/zmensene30/truhla_zamcena.png')
        self.obr.set_colorkey('#ffffff')
        self.dava = 'truhla'
    def nakresli(self):
        screen.blit(self.obr,(self.pos[0]*40+12,self.pos[1]*40+12))

class Hrdina:
    def __init__(self):
        self.pos = [12,12]
        self.predchozi = [12,12]
        self.zdravi = 10
        self.predmety = {'zbrane':[],'klic':False,'kouzla':[],'truhly':0,'kletba':False}
    def nakresli(self):
        if self.zdravi == 0:
            pygame.draw.circle(screen,'#ff0000',(self.pos[0]*40+20,self.pos[1]*40+20),8)
        else:
            pygame.draw.circle(screen,'#33ff00',(self.pos[0]*40+20,self.pos[1]*40+20),8)
    def odemkni(self):
        self.predmety['klic'] = False
    def pouzij_kouzlo(self,jake):
        del self.predmety['kouzla'][jake]
    def uzdrav_se(self):
        self.zdravi = 10
    def nakresli_stav(self):
        if self.predmety['klic']:
            img = pygame.image.load('obrazky/klic.png')
            img.set_colorkey('#ffffff')
            screen.blit(img,(1060,154))
        for zbran in range(len(self.predmety['zbrane'])):
            if self.predmety['zbrane'][zbran] == 1:
                img = pygame.image.load('obrazky/dyky.png')
                img.set_colorkey('#ffffff')
                screen.blit(img,(1060,10+(zbran*70)))
            if self.predmety['zbrane'][zbran] == 2:
                img = pygame.image.load('obrazky/mec.png')
                img.set_colorkey('#ffffff')
                screen.blit(img,(1060,10+(zbran*70)))
            if self.predmety['zbrane'][zbran] == 3:
                img = pygame.image.load('obrazky/sekera.png')
                img.set_colorkey('#ffffff')
                screen.blit(img,(1060,10+(zbran*70)))
        for kouzlo in range(len(self.predmety['kouzla'])):
            vec = self.predmety['kouzla'][kouzlo]
            img = pygame.image.load(f'obrazky/{vec}.png')
            img.set_colorkey('#ffffff')
            screen.blit(img,(1150,10+(kouzlo*70)))
        font = pygame.font.SysFont('Arial',30)
        screen.blit(font.render('truhel: '+str(self.predmety['truhly']),True,'#000000'),(1060,230))
    def dostan(self,co):
        global run
        if co == 'dyky':
            self.predmety['zbrane'].append(1)
        if co == 'mec':
            self.predmety['zbrane'].append(2)
        if co == 'sekera':
            self.predmety['zbrane'].append(3)
        if len(self.predmety['zbrane']) >= 3:
            if 1 in self.predmety['zbrane']:
                del self.predmety['zbrane'][self.predmety['zbrane'].index(1)]
                mapa_veci[self.pos[1]][self.pos[0]] = 'dyky'
                raise Exception
            elif 2 in self.predmety['zbrane']:
                del self.predmety['zbrane'][self.predmety['zbrane'].index(2)]
                mapa_veci[self.pos[1]][self.pos[0]] = 'mec'
                raise Exception
            elif 3 in self.predmety['zbrane']:
                del self.predmety['zbrane'][self.predmety['zbrane'].index(3)]
                mapa_veci[self.pos[1]][self.pos[0]] = 'sekera'
                raise Exception
        if co == 'klic' and not self.predmety['klic']:
            self.predmety['klic'] = True
        elif co == 'klic' and self.predmety['klic']:
            raise Exception
        if co in 'uzdraveni magicky_mec':
            if co == 'uzdraveni':
                self.predmety['kouzla'].append('uzdraveni')
            if co == 'magicky_mec':
                self.predmety['kouzla'].append('magicky_mec')
            if len(self.predmety['kouzla']) >= 4:
                mapa_veci[self.pos[1]][self.pos[0]] = self.predmety['kouzla'][0]
                del self.predmety['kouzla'][0]
                raise Exception
        if co == 'truhla':
            self.predmety['truhly'] += 1
        if co == 'truhla+':
            img = pygame.image.load('obrazky/truhla+.png')
            img.set_colorkey('#ffffff')
            nakresli_vse()
            screen.blit(img,(1100,600))
            pygame.display.flip()
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        exit()
    def uskoc(self):
        self.pos = self.predchozi.copy()
    def pohyb(self,smer):
        if not self.zdravi == 0:
            if (smer == pygame.K_LEFT or smer == pygame.K_a) and self.pos[0] != 0 and mapa_sezn[self.pos[1]][self.pos[0]].pruchod[0] == 1:
                self.predchozi = self.pos.copy()
                if mapa_sezn[self.pos[1]][self.pos[0]-1] != None and mapa_sezn[self.pos[1]][self.pos[0]-1].pruchod[2] == 1:
                    self.pos[0] -= 1
                elif mapa_sezn[self.pos[1]][self.pos[0]-1] == None:
                    ran = random.choice(list('xilt'))
                    if ran == 'x':
                        dilky.append(Dilek_X(self.pos[0]-1,self.pos[1],0))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]][self.pos[0]-1] = Dilek_X(self.pos[0]-1,self.pos[1],0)
                        self.pos[0] -= 1
                    if ran == 'i':
                        dilky.append(Dilek_I(self.pos[0]-1,self.pos[1],90))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]][self.pos[0]-1] = Dilek_I(self.pos[0]-1,self.pos[1],90)
                        self.pos[0] -= 1
                    if ran == 'l':
                        if random.randrange(0,2) == 0:
                            dilky.append(Dilek_L(self.pos[0]-1,self.pos[1],0))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]-1] = Dilek_L(self.pos[0]-1,self.pos[1],0)
                            self.pos[0] -= 1
                        else:
                            dilky.append(Dilek_L(self.pos[0]-1,self.pos[1],-90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]-1] = Dilek_L(self.pos[0]-1,self.pos[1],-90)
                            self.pos[0] -= 1
                    if ran == 't':
                        r = random.randrange(0,3)
                        if r == 0:
                            dilky.append(Dilek_T(self.pos[0]-1,self.pos[1],0))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]-1] = Dilek_T(self.pos[0]-1,self.pos[1],0)
                            self.pos[0] -= 1
                        elif r == 1:
                            dilky.append(Dilek_T(self.pos[0]-1,self.pos[1],90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]-1] = Dilek_T(self.pos[0]-1,self.pos[1],90)
                            self.pos[0] -= 1
                        else:
                            dilky.append(Dilek_T(self.pos[0]-1,self.pos[1],180))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]-1] = Dilek_T(self.pos[0]-1,self.pos[1],180)
                            self.pos[0] -= 1
                    nova_potvora(self.pos[0],self.pos[1])

            if (smer == pygame.K_RIGHT or smer == pygame.K_d) and self.pos[0] != 24 and mapa_sezn[self.pos[1]][self.pos[0]].pruchod[2] == 1:
                self.predchozi = self.pos.copy()
                if mapa_sezn[self.pos[1]][self.pos[0]+1] != None and mapa_sezn[self.pos[1]][self.pos[0]+1].pruchod[0] == 1:
                    self.pos[0] += 1
                elif mapa_sezn[self.pos[1]][self.pos[0]+1] == None:
                    ran = random.choice(list('xilt'))
                    if ran == 'x':
                        dilky.append(Dilek_X(self.pos[0]+1,self.pos[1],0))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]][self.pos[0]+1] = Dilek_X(self.pos[0]+1,self.pos[1],0)
                        self.pos[0] += 1
                    if ran == 'i':
                        dilky.append(Dilek_I(self.pos[0]+1,self.pos[1],90))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]][self.pos[0]+1] = Dilek_I(self.pos[0]+1,self.pos[1],90)
                        self.pos[0] += 1
                    if ran == 'l':
                        if random.randrange(0,2) == 0:
                            dilky.append(Dilek_L(self.pos[0]+1,self.pos[1],90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]+1] = Dilek_L(self.pos[0]+1,self.pos[1],90)
                            self.pos[0] += 1
                        else:
                            dilky.append(Dilek_L(self.pos[0]+1,self.pos[1],180))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]+1] = Dilek_L(self.pos[0]+1,self.pos[1],180)
                            self.pos[0] += 1
                    if ran == 't':
                        r = random.randrange(0,3)
                        if r == 0:
                            dilky.append(Dilek_T(self.pos[0]+1,self.pos[1],0))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]+1] = Dilek_T(self.pos[0]+1,self.pos[1],0)
                            self.pos[0] += 1
                        elif r == 1:
                            dilky.append(Dilek_T(self.pos[0]+1,self.pos[1],-90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]+1] = Dilek_T(self.pos[0]+1,self.pos[1],-90)
                            self.pos[0] += 1
                        else:
                            dilky.append(Dilek_T(self.pos[0]+1,self.pos[1],180))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]][self.pos[0]+1] = Dilek_T(self.pos[0]+1,self.pos[1],180)
                            self.pos[0] += 1
                    nova_potvora(self.pos[0],self.pos[1])

            if (smer == pygame.K_UP or smer == pygame.K_w) and self.pos[1] != 0 and mapa_sezn[self.pos[1]][self.pos[0]].pruchod[1] == 1:
                self.predchozi = self.pos.copy()
                if mapa_sezn[self.pos[1]-1][self.pos[0]] != None and mapa_sezn[self.pos[1]-1][self.pos[0]].pruchod[3] == 1:
                    self.pos[1] -= 1
                elif mapa_sezn[self.pos[1]-1][self.pos[0]] == None:
                    ran = random.choice(list('xilt'))
                    if ran == 'x':
                        dilky.append(Dilek_X(self.pos[0],self.pos[1]-1,0))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]-1][self.pos[0]] = Dilek_X(self.pos[0],self.pos[1]-1,0)
                        self.pos[1] -= 1
                    if ran == 'i':
                        dilky.append(Dilek_I(self.pos[0],self.pos[1]-1,0))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]-1][self.pos[0]] = Dilek_I(self.pos[0],self.pos[1]-1,0)
                        self.pos[1] -= 1
                    if ran == 'l':
                        if random.randrange(0,2) == 0:
                            dilky.append(Dilek_L(self.pos[0],self.pos[1]-1,180))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]-1][self.pos[0]] = Dilek_L(self.pos[0],self.pos[1]-1,180)
                            self.pos[1] -= 1
                        else:
                            dilky.append(Dilek_L(self.pos[0],self.pos[1]-1,-90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]-1][self.pos[0]] = Dilek_L(self.pos[0],self.pos[1]-1,-90)
                            self.pos[1] -= 1
                    if ran == 't':
                        r = random.randrange(0,3)
                        if r == 0:
                            dilky.append(Dilek_T(self.pos[0],self.pos[1]-1,0))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]-1][self.pos[0]] = Dilek_T(self.pos[0],self.pos[1]-1,0)
                            self.pos[1] -= 1
                        elif r == 1:
                            dilky.append(Dilek_T(self.pos[0],self.pos[1]-1,90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]-1][self.pos[0]] = Dilek_T(self.pos[0],self.pos[1]-1,90)
                            self.pos[1] -= 1
                        else:
                            dilky.append(Dilek_T(self.pos[0],self.pos[1]-1,-90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]-1][self.pos[0]] = Dilek_T(self.pos[0],self.pos[1]-1,-90)
                            self.pos[1] -= 1
                    nova_potvora(self.pos[0],self.pos[1])

            if (smer == pygame.K_DOWN or smer == pygame.K_s) and self.pos[1] != 24 and mapa_sezn[self.pos[1]][self.pos[0]].pruchod[3] == 1:
                self.predchozi = self.pos.copy()
                if mapa_sezn[self.pos[1]+1][self.pos[0]] != None and mapa_sezn[self.pos[1]+1][self.pos[0]].pruchod[1] == 1:
                    self.pos[1] += 1
                elif mapa_sezn[self.pos[1]+1][self.pos[0]] == None:
                    ran = random.choice(list('xilt'))
                    if ran == 'x':
                        dilky.append(Dilek_X(self.pos[0],self.pos[1]+1,0))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]+1][self.pos[0]] = Dilek_X(self.pos[0],self.pos[1]+1,0)
                        self.pos[1] += 1
                    if ran == 'i':
                        dilky.append(Dilek_I(self.pos[0],self.pos[1]+1,0))
                        dilky[-1].nakresli()
                        mapa_sezn[self.pos[1]+1][self.pos[0]] = Dilek_I(self.pos[0],self.pos[1]+1,0)
                        self.pos[1] += 1
                    if ran == 'l':
                        if random.randrange(0,2) == 0:
                            dilky.append(Dilek_L(self.pos[0],self.pos[1]+1,0))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]+1][self.pos[0]] = Dilek_L(self.pos[0],self.pos[1]+1,0)
                            self.pos[1] += 1
                        else:
                            dilky.append(Dilek_L(self.pos[0],self.pos[1]+1,90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]+1][self.pos[0]] = Dilek_L(self.pos[0],self.pos[1]+1,90)
                            self.pos[1] += 1
                    if ran == 't':
                        r = random.randrange(0,3)
                        if r == 0:
                            dilky.append(Dilek_T(self.pos[0],self.pos[1]+1,180))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]+1][self.pos[0]] = Dilek_T(self.pos[0],self.pos[1]+1,180)
                            self.pos[1] += 1
                        elif r == 1:
                            dilky.append(Dilek_T(self.pos[0],self.pos[1]+1,90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]+1][self.pos[0]] = Dilek_T(self.pos[0],self.pos[1]+1,90)
                            self.pos[1] += 1
                        else:
                            dilky.append(Dilek_T(self.pos[0],self.pos[1]+1,-90))
                            dilky[-1].nakresli()
                            mapa_sezn[self.pos[1]+1][self.pos[0]] = Dilek_T(self.pos[0],self.pos[1]+1,-90)
                            self.pos[1] += 1
                    nova_potvora(self.pos[0],self.pos[1])




def nova_potvora(x,y):
    ran = random.randrange(0,3)
    if ran == 0:
        ran = random.choice(list('tttttttttt0000000011112222222233333333333344444555667'))
        if ran == 't':
            potvory.append(Truhla(x,y))
            mapa_potvor[y][x] = Truhla(x,y)
        if ran == '0':
            potvory.append(Krysa(x,y))
            mapa_potvor[y][x] = Krysa(x,y)
        if ran == '1':
            potvory.append(Pavouk(x,y))
            mapa_potvor[y][x] = Pavouk(x,y)
        if ran == '2':
            potvory.append(Mumie(x,y))
            mapa_potvor[y][x] = Mumie(x,y)
        if ran == '3':
            potvory.append(Klicnik(x,y))
            mapa_potvor[y][x] = Klicnik(x,y)
        if ran == '4':
            potvory.append(Sermir(x,y))
            mapa_potvor[y][x] = Sermir(x,y)
        if ran == '5':
            potvory.append(Sekernik(x,y))
            mapa_potvor[y][x] = Sekernik(x,y)
        if ran == '6':
            potvory.append(Duch(x,y))
            mapa_potvor[y][x] = Duch(x,y)
        if ran == '7':
            if random.randrange(0,1) == 0:
                potvory.append(Drak(x,y))
                mapa_potvor[y][x] = Drak(x,y)

def objev_potvory():
    for dilek in dilky:
        if random.randrange(0,1000) == 0 and mapa_veci[dilek.y][dilek.x] == None and mapa_potvor[dilek.y][dilek.x] == None and hrac.pos != [dilek.x,dilek.y]:
            nova_potvora(dilek.x,dilek.y)

def dostan_vec(key):
    if mapa_veci[hrac.pos[1]][hrac.pos[0]] != None and (key == pygame.K_q or key == pygame.K_SPACE):
        try:
            hrac.dostan(mapa_veci[hrac.pos[1]][hrac.pos[0]])
            mapa_veci[hrac.pos[1]][hrac.pos[0]] = None
        except:
            time.sleep(0)

def boj(potvora):
    kostka1 = random.randrange(1,7)
    kostka2 = random.randrange(1,7)
    zbrane_sila = 0
    for zbran in hrac.predmety['zbrane']:
        zbrane_sila += zbran
    hrac_utok = kostka1 + kostka2 + zbrane_sila
    potvora_utok = potvora.sila
    nakresli_vse()
    info_boj = pygame.Surface((570,100),pygame.SRCALPHA)
    pygame.draw.rect(info_boj,'#ffffff',pygame.Rect(0,0,570,100))
    pygame.draw.rect(info_boj,'#000000',pygame.Rect(0,0,570,100),width = 2)
    pygame.draw.rect(info_boj,'#000000',pygame.Rect(200,10,40,40),width = 2)
    pygame.draw.rect(info_boj,'#000000',pygame.Rect(250,10,40,40),width = 2)
    font = pygame.font.SysFont('Arial',30)
    info_boj.blit(font.render('tvoje síla: '+str(hrac_utok),True,'#000000'),(10,10))
    info_boj.blit(font.render(' (                + '+str(zbrane_sila)+' ze zbraní)',True,'#000000'),(170,10))
    info_boj.blit(font.render(str(kostka1),True,'#000000'),(210,15))
    info_boj.blit(font.render(str(kostka2),True,'#000000'),(260,15))
    info_boj.blit(font.render('síla protivníka ('+potvora.jmeno+') : '+str(potvora_utok),True,'#000000'),(10,60))
    info_boj.set_alpha(200)
    screen.blit(info_boj,((hrac.pos[0]+1)*40,(hrac.pos[1]+1)*40))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_q:
                    running = False
        if pygame.mouse.get_pressed()[0]:
            for kouzlo,pozice in zip(hrac.predmety['kouzla'],range(len(hrac.predmety['kouzla']))):
                if kouzlo == 'magicky_mec':
                    if pygame.Rect(1150,10+(pozice*70),74,70).collidepoint(pygame.mouse.get_pos()):
                        hrac.pouzij_kouzlo(pozice)
                        zbrane_sila += 1
                        hrac_utok = kostka1 + kostka2 + zbrane_sila
        nakresli_vse()
        info_boj = pygame.Surface((570,100),pygame.SRCALPHA)
        pygame.draw.rect(info_boj,'#ffffff',pygame.Rect(0,0,570,100))
        pygame.draw.rect(info_boj,'#000000',pygame.Rect(0,0,570,100),width = 2)
        pygame.draw.rect(info_boj,'#000000',pygame.Rect(200,10,40,40),width = 2)
        pygame.draw.rect(info_boj,'#000000',pygame.Rect(250,10,40,40),width = 2)
        font = pygame.font.SysFont('Arial',30)
        info_boj.blit(font.render('tvoje síla: '+str(hrac_utok),True,'#000000'),(10,10))
        info_boj.blit(font.render(' (                + '+str(zbrane_sila)+' ze zbraní)',True,'#000000'),(170,10))
        info_boj.blit(font.render(str(kostka1),True,'#000000'),(210,15))
        info_boj.blit(font.render(str(kostka2),True,'#000000'),(260,15))
        info_boj.blit(font.render('síla protivníka ('+potvora.jmeno+') : '+str(potvora_utok),True,'#000000'),(10,60))
        info_boj.set_alpha(200)
        screen.blit(info_boj,((hrac.pos[0]+1)*40,(hrac.pos[1]+1)*40))
        pygame.display.flip()
    if hrac_utok > potvora_utok:
        mapa_veci[potvora.pos[1]][potvora.pos[0]] = potvora.dava
        mapa_potvor[potvora.pos[1]][potvora.pos[0]] = None
        del potvory[potvory.index(potvora)]
    elif hrac_utok < potvora_utok:
        hrac.zdravi -= 1
        hrac.uskoc()
    elif hrac_utok == potvora_utok:
        hrac.uskoc()

def boj_a_n():
    for potvora in potvory:
        if potvora.pos[0] == hrac.pos[0] and potvora.pos[1] == hrac.pos[1] and potvora.sila != '0':
            boj(potvora)
        if potvora.pos[0] == hrac.pos[0] and potvora.pos[1] == hrac.pos[1] and potvora.sila == '0':
            if hrac.predmety['klic']:
                del potvory[potvory.index(potvora)]
                hrac.dostan('truhla')
                mapa_potvor[hrac.pos[1]][hrac.pos[0]] = None
                hrac.odemkni()

screen = pygame.display.set_mode((1500,1000))
mapa = pygame.Surface((1000,1000))
dilky = [Dilek_X(12,12,0)]
dilky[-1].nakresli()
hrac = Hrdina()
potvory = []

def nakresli_vse():
    screen.blit(mapa,(0,0))
    for y in range(len(mapa_veci)):
        for x in range(len(mapa_veci[y])):
            vec = mapa_veci[y][x]
            if not vec == None:
                img = pygame.image.load(f'obrazky/zmensene20/{vec}.png')
                img.set_colorkey('#ffffff')
                screen.blit(img,(x*40+13,y*40+13))
    hrac.nakresli()
    for potvora in potvory:
        potvora.nakresli()
    pygame.draw.rect(screen,'#9a9996',pygame.Rect(1000,0,500,1000))
    zivot = -1
    for zivot in range(hrac.zdravi):
        screen.blit(pygame.image.load('obrazky/srdce.png'),(1020,20+zivot*30))
    for smrt in range(10-hrac.zdravi):
        screen.blit(pygame.image.load('obrazky/lebka.png'),(1020,50+smrt*30+zivot*30))
    hrac.nakresli_stav()

mapa_sezn = [
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
mapa_potvor = [
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
mapa_veci = [
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
mapa_sezn[12][12] = Dilek_X(12,12,0)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            hrac.pohyb(event.key)
            dostan_vec(event.key)
    if pygame.mouse.get_pressed()[0]:
        for kouzlo,pozice in zip(hrac.predmety['kouzla'],range(len(hrac.predmety['kouzla']))):
            if kouzlo == 'uzdraveni':
                if pygame.Rect(1150,10+(pozice*70),74,70).collidepoint(pygame.mouse.get_pos()):
                    hrac.pouzij_kouzlo(pozice)
                    hrac.uzdrav_se()
    objev_potvory()
    nakresli_vse()
    boj_a_n()
    pygame.display.flip()
