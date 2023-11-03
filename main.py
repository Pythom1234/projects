#!/usr/bin/python3

import socket
import tkinter

def server():
    global server_or_client
    server_or_client = 'server'
    button1.destroy()
    button2.destroy()
    text1.destroy()
    text2.pack()
    entry1.insert(0,socket.gethostbyname(socket.gethostname()))
    entry1.pack()
    text3.pack()
    entry2.insert(0,12345)
    entry2.pack()
    button3.pack()

def client():
    global server_or_client
    server_or_client = 'client'
    button1.destroy()
    button2.destroy()
    text1.destroy()
    text2.pack()
    entry1.insert(0,socket.gethostbyname(socket.gethostname()))
    entry1.pack()
    text3.pack()
    entry2.insert(0,12345)
    entry2.pack()
    button4.pack()

def pripojit():
    try:
        soc.connect((entry1.get(),int(entry2.get())))
        tk1.destroy()
    except:
        pass

def spustit():
    global conn, addr
    try:
        soc.bind((entry1.get(),int(entry2.get())))
        soc.listen(2)
        conn, addr = soc.accept()
        tk1.destroy()
    except:
        pass

server_or_client = None
conn = None
addr = None
soc = socket.socket()
tk1 = tkinter.Tk()
tk1.option_add('*Font', 'Arial 15')
text1 = tkinter.Label(text='spustit jako')
text2 = tkinter.Label(text='IP adresa:')
text3 = tkinter.Label(text='port')
text4 = tkinter.Label(text='připojování...')
entry1 = tkinter.Entry()
entry2 = tkinter.Entry()
button1 = tkinter.Button(text='server',command=server)
button2 = tkinter.Button(text='client',command=client)
button3 = tkinter.Button(text='spustit',command=spustit)
button4 = tkinter.Button(text='připojit',command=pripojit)

text1.pack()
button1.pack()
button2.pack()
tk1.mainloop()

def konec():
    tk2.destroy()
tk2 = tkinter.Tk()
tk2.option_add('*Font','Arial 15')
moznosti = ['pistole','raketomet','brokovnice']
opt1 = tkinter.StringVar(tk2)
opt1.set(moznosti[0])
opt_menu1 = tkinter.OptionMenu(tk2, opt1, *moznosti)
opt_menu1.pack()
button5 = tkinter.Button(text='OK',command=konec)
button5.pack()
tk2.mainloop()

zbran = opt1.get()

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import json
import asyncio
import random
import math
import numpy

vrcholy = [
    [1, 1, -1], [1, 1, 1], [-1, 1, 1], [-1, 1, -1],
    [1, -1, -1], [1, -1, 1], [-1, -1, 1], [-1, -1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1],
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, 1, -1], [1, -1, -1], [1, -1, 1],
    [-1, 1, 1], [-1, 1, -1], [-1, -1, -1], [-1, -1, 1]
    ]
otoceni_pohyb = {'w':{'s':0.05,'j':-0.05,'z':-0.05,'v':0.05},'a':{'s':-0.05,'j':0.05,'z':-0.05,'v':0.05}}
kulky = []
hrac_pos = [0,0,0]
znicene_zdi = []

class Strela:
    def __init__(self,pos,rychlost):
        self.pos = pos
        self.rychlost = rychlost
    def tik(self):
        global kulky
        self.pos[0] += self.rychlost[0]
        self.pos[1] += self.rychlost[1]
        self.pos[2] += self.rychlost[2]
        try:
            if not -200 < self.pos[0] < 200:
                del kulky[kulky.index(self)]
            if not -200 < self.pos[2] < 200:
                del kulky[kulky.index(self)]
            if self.pos[1] >= 0:
                del kulky[kulky.index(self)]
            if bludiste_cele.get_at((round(self.pos[0])+200,round(self.pos[2])+200)) == (0,0,0):
                del kulky[kulky.index(self)]
        except:
            pass



class Kulka(Strela):
    def tik(self):
        super().tik()
    def nakresli(self):
        glColor3f(0,0,0)
        glPointSize(2)
        glBegin(GL_POINTS)
        glVertex3f(self.pos[0]-hrac_pos[0],self.pos[1]-hrac_pos[1],self.pos[2]-hrac_pos[2])
        glEnd()
        glColor3f(1,1,1)
        glPointSize(4)
        glBegin(GL_POINTS)
        glVertex3f(self.pos[0]-hrac_pos[0],self.pos[1]-hrac_pos[1],self.pos[2]-hrac_pos[2])
        glEnd()
    def poslat(self):
        return [round(self.pos[0],3),round(self.pos[1],3),round(self.pos[2],3),'k']

class Raketa(Strela):
    def tik(self):
        global kulky
        self.pos[0] += self.rychlost[0]
        self.pos[1] += self.rychlost[1]
        self.pos[2] += self.rychlost[2]
        try:
            if not -200 < self.pos[0] < 200:
                del kulky[kulky.index(self)]
            if not -200 < self.pos[2] < 200:
                del kulky[kulky.index(self)]
            if self.pos[1] >= 0:
                del kulky[kulky.index(self)]
            if bludiste_cele.get_at((round(self.pos[0])+200,round(self.pos[2])+200)) == (0,0,0):
                while True:
                    if bludiste.get_at((round((self.pos[0]-10)/20)+10,round((self.pos[2]-10)/20)+10)) == (0,0,0):
                        bludiste.blit(pygame.image.fromstring(b'\xff\xff\xff',(1,1),'RGB'),(round((self.pos[0]-10)/20)+10,round((self.pos[2]-10)/20)+10))
                        break
                    else:
                        self.pos[0] += self.rychlost[0] / 10
                        self.pos[1] += self.rychlost[1] / 10
                        self.pos[2] += self.rychlost[2] / 10
                znicene_zdi.append((round((self.pos[0]-10)/20)+10,round((self.pos[2]-10)/20)+10))
                del kulky[kulky.index(self)]
        except:
            pass
    def nakresli(self):
        glColor3f(1,0,0)
        glPointSize(3)
        glBegin(GL_POINTS)
        glVertex3f(self.pos[0]-hrac_pos[0],self.pos[1]-hrac_pos[1],self.pos[2]-hrac_pos[2])
        glEnd()
        glColor3f(1,1,1)
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex3f(self.pos[0]-hrac_pos[0],self.pos[1]-hrac_pos[1],self.pos[2]-hrac_pos[2])
        glEnd()
    def poslat(self):
        return [round(self.pos[0],3),round(self.pos[1],3),round(self.pos[2],3),'r']


class Zbran:
    def __init__(self):
        self.nabijeni = 0
    def tik(self):
        self.nabijeni -= 0.1


class Pistole(Zbran):
    def pal(self,pos,rot):
        global kulky
        if self.nabijeni <= 0:
            self.nabijeni = 0.5
            smer = [0, 0, 0]
            smer = [math.cos(smer[0]+math.radians(rot[0]+90)),
                    -math.sin(smer[1]+math.radians(rot[1])),
                    math.sin(smer[2]+math.radians(rot[0]+90))]
            rychlost_strely = 3
            kulky.append(Kulka([pos[0], pos[1], pos[2]+1], [smer[0] * rychlost_strely, smer[1] * rychlost_strely, smer[2] * rychlost_strely]))

class Raketomet(Zbran):
    def pal(self,pos,rot):
        global kulky
        if self.nabijeni <= 0:
            self.nabijeni = 4
            smer = [0, 0, 0]
            smer = [math.cos(smer[0]+math.radians(rot[0]+90)),
                    -math.sin(smer[1]+math.radians(rot[1])),
                    math.sin(smer[2]+math.radians(rot[0]+90))]
            rychlost_strely = 2.5
            kulky.append(Raketa([pos[0], pos[1], pos[2]+1], [smer[0] * rychlost_strely, smer[1] * rychlost_strely, smer[2] * rychlost_strely]))

class Brokovnice(Zbran):
    def pal(self,pos,rot):
        global kulky
        rot2 = rot.copy()
        rot2[0] += 20
        if self.nabijeni <= 0:
            self.nabijeni = 2.3
            for i in range(-20,20):
                rot2[0] += i/6
                smer = [0, 0, 0]
                smer = [math.cos(smer[0]+math.radians(rot2[0]+90)),
                        -math.sin(smer[1]+math.radians(rot2[1])),
                        math.sin(smer[2]+math.radians(rot2[0]+90))]
                rychlost_strely = 1
                kulky.append(Kulka([pos[0], pos[1], pos[2]+1], [smer[0] * rychlost_strely, smer[1] * rychlost_strely, smer[2] * rychlost_strely]))


class Hra:
    def __init__(self):
        if server_or_client == 'server':
            self.pos = [-198,-2,-198]
        if server_or_client == 'client':
            self.pos = [198,-2,198]
        self.otoceni = [0,0]
        self.run = True
        self.out = False
        self.mrtev = False
        self.druhy = [[0,0,0],100,[],0,[]]
        self.zivoty = 100
        self.skok = 0
        self.strelen = 0
        if zbran == 'pistole':
            self.zbran = Pistole()
        if zbran == 'brokovnice':
            self.zbran = Brokovnice()
        if zbran == 'raketomet':
            self.zbran = Raketomet()
        pygame.init()
        display = [1600,1000]
        self.screen = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        glViewport(0, 0, display[0],display[1])
        glMatrixMode(GL_PROJECTION)
        gluPerspective(75, (display[0] / display[1]), 0.1, 100000)
        glTranslate(0,0,0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        while self.run:
            asyncio.run(self.tik2())
    async def posli(self):
        global znicene_zdi
        poslat_k = []
        for i in kulky:
            poslat_k.append(i.poslat())
        if len(str([self.pos,self.zivoty,poslat_k,self.strelen,znicene_zdi])) >= 1024:
            while len(str([self.pos,self.zivoty,poslat_k,self.strelen,znicene_zdi])) >= 1024:
                del poslat_k[-1]
        posli([self.pos,self.zivoty,poslat_k,self.strelen,znicene_zdi])
        znicene_zdi = []
        self.strelen = 0
    async def prijmi(self):
        druhy = prijmi()
        if druhy != '':
            self.druhy = druhy
    async def tik(self):
        global hrac_pos, bludiste_cele
        if self.druhy[3]:
            self.zivoty -= self.druhy[3]
        if self.zivoty <= 0:
            self.mrtev = True
            self.out = True
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)
        hrac_pos = self.pos.copy()
        for i in self.druhy[4]:
            bludiste.blit(pygame.image.fromstring(b'\xff\xff\xff',(1,1),'RGB'),i)
        glLoadIdentity()
        gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE and not self.mrtev:
                pygame.event.set_grab(not pygame.event.get_grab())
                pygame.mouse.set_visible(not pygame.mouse.get_visible())
                self.out = not self.out
        dx,dy = pygame.mouse.get_rel()
        if not self.out:
            if pygame.mouse.get_pressed()[2]:
                self.otoceni[0] -= dx/15
                self.otoceni[1] += dy/15
            else:
                self.otoceni[0] -= dx/2
                self.otoceni[1] += dy/2
        if self.otoceni[0] >= 360:
            self.otoceni[0] = self.otoceni[0]-360
        if self.otoceni[1] >= 360:
            self.otoceni[1] = self.otoceni[1]-360
        if self.otoceni[0] <= 0:
            self.otoceni[0] = 360+self.otoceni[0]
        if self.otoceni[1] <= 0:
            self.otoceni[1] = 360+self.otoceni[1]
        glRotatef(self.otoceni[1], 1, 0, 0)
        glRotatef(self.otoceni[0], 0, 1, 0)
        looking_at = 's'
        if round(self.otoceni[0]) in range(0,22) or round(self.otoceni[0]) in range(315,360):
            looking_at = 's'
        if round(self.otoceni[0]) in range(22,45):
            looking_at = 'sz'
        if round(self.otoceni[0]) in range(45,112):
            looking_at = 'z'
        if round(self.otoceni[0]) in range(112,135):
            looking_at = 'jz'
        if round(self.otoceni[0]) in range(225,292):
            looking_at = 'v'
        if round(self.otoceni[0]) in range(292,315):
            looking_at = 'sv'
        if round(self.otoceni[0]) in range(135,202):
            looking_at = 'j'
        if round(self.otoceni[0]) in range(202,225):
            looking_at = 'jv'
        jdi = []
        if not self.out:
            if pygame.key.get_pressed()[pygame.K_w]:
                for la in looking_at:
                    if 's' in la:
                        jdi += [[2,otoceni_pohyb['w']['s']*4]]
                    if 'j' in la:
                        jdi += [[2,otoceni_pohyb['w']['j']*4]]
                    if 'v' in la:
                        jdi += [[0,otoceni_pohyb['w']['v']*4]]
                    if 'z' in la:
                        jdi += [[0,otoceni_pohyb['w']['z']*4]]
            if pygame.key.get_pressed()[pygame.K_s]:
                for la in looking_at:
                    if 's' in la:
                        jdi += [[2,-otoceni_pohyb['w']['s']*4]]
                    if 'j' in la:
                        jdi += [[2,-otoceni_pohyb['w']['j']*4]]
                    if 'v' in la:
                        jdi += [[0,-otoceni_pohyb['w']['v']*4]]
                    if 'z' in la:
                        jdi += [[0,-otoceni_pohyb['w']['z']*4]]
            if pygame.key.get_pressed()[pygame.K_a]:
                for la in looking_at:
                    if 's' in la:
                        jdi += [[0,otoceni_pohyb['a']['s']*4]]
                    if 'j' in la:
                        jdi += [[0,otoceni_pohyb['a']['j']*4]]
                    if 'v' in la:
                        jdi += [[2,otoceni_pohyb['a']['v']*4]]
                    if 'z' in la:
                        jdi += [[2,otoceni_pohyb['a']['z']*4]]
            if pygame.key.get_pressed()[pygame.K_d]:
                for la in looking_at:
                    if 's' in la:
                        jdi += [[0,-otoceni_pohyb['a']['s']*4]]
                    if 'j' in la:
                        jdi += [[0,-otoceni_pohyb['a']['j']*4]]
                    if 'v' in la:
                        jdi += [[2,-otoceni_pohyb['a']['v']*4]]
                    if 'z' in la:
                        jdi += [[2,-otoceni_pohyb['a']['z']*4]]
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                if pygame.key.get_pressed()[pygame.K_w]:
                    for la in looking_at:
                        if 's' in la:
                            jdi += [[2,otoceni_pohyb['w']['s']*10]]
                        if 'j' in la:
                            jdi += [[2,otoceni_pohyb['w']['j']*10]]
                        if 'v' in la:
                            jdi += [[0,otoceni_pohyb['w']['v']*10]]
                        if 'z' in la:
                            jdi += [[0,otoceni_pohyb['w']['z']*10]]
                if pygame.key.get_pressed()[pygame.K_s]:
                    for la in looking_at:
                        if 's' in la:
                            jdi += [[2,-otoceni_pohyb['w']['s']*10]]
                        if 'j' in la:
                            jdi += [[2,-otoceni_pohyb['w']['j']*10]]
                        if 'v' in la:
                            jdi += [[0,-otoceni_pohyb['w']['v']*10]]
                        if 'z' in la:
                            jdi += [[0,-otoceni_pohyb['w']['z']*10]]
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.pos[1] == -2:
                self.skok = 5
        if jdi:
            for i in range(len(jdi)):
                try:
                    if jdi[i][0] == 2 and jdi[i][1] == abs(jdi[i][1]):
                        self.pos[2] += jdi[i][1]
                        if bludiste_cele.get_at((round(self.pos[0])+200,round(self.pos[2])+200)) == (0,0,0):
                            self.pos[2] -= jdi[i][1]
                    if jdi[i][0] == 2 and jdi[i][1] != abs(jdi[i][1]):
                        self.pos[2] += jdi[i][1]
                        if bludiste_cele.get_at((round(self.pos[0])+200,round(self.pos[2])+200)) == (0,0,0):
                            self.pos[2] -= jdi[i][1]
                    if jdi[i][0] == 0 and jdi[i][1] == abs(jdi[i][1]):
                        self.pos[0] += jdi[i][1]
                        if bludiste_cele.get_at((round(self.pos[0])+200,round(self.pos[2])+200)) == (0,0,0):
                            self.pos[0] -= jdi[i][1]
                    if jdi[i][0] == 0 and jdi[i][1] != abs(jdi[i][1]):
                        self.pos[0] += jdi[i][1]
                        if bludiste_cele.get_at((round(self.pos[0])+200,round(self.pos[2])+200)) == (0,0,0):
                            self.pos[0] -= jdi[i][1]
                except:
                    pass
        if self.skok:
            self.pos[1] -= self.skok
            self.skok -= 1

        if self.pos[1] < -2:
            self.pos[1] += 1

        if not -200 < self.pos[0] < 200:
            self.zivoty = 0
        if not -200 < self.pos[2] < 200:
            self.zivoty = 0
        br = False
        for k in kulky:
            i = k.poslat()
            if (self.druhy[0][0] - 1 < i[0] < self.druhy[0][0] + 1 and
                self.druhy[0][1] < i[1] < self.druhy[0][1] + 2 and
                self.druhy[0][2] - 1 < i[2] < self.druhy[0][2] + 1):
                if i[3] == 'k':
                    self.strelen = 3
                    del kulky[kulky.index(k)]
                    br = True
                if i[3] == 'r':
                    self.strelen = 10
                    del kulky[kulky.index(k)]
                    br = True
            if br:
                break


        self.zbran.tik()

        if pygame.mouse.get_pressed()[0]:
            self.zbran.pal(self.pos,self.otoceni)
        for i in kulky:
            i.tik()
            i.nakresli()
        for i in self.druhy[2]:
            glColor3f(0,0,0)
            glPointSize(2)
            glBegin(GL_POINTS)
            glVertex3f(i[0]-self.pos[0],i[1]-self.pos[1],i[2]-self.pos[2])
            glEnd()
            glColor3f(1,1,1)
            glPointSize(4)
            glBegin(GL_POINTS)
            glVertex3f(i[0]-self.pos[0],i[1]-self.pos[1],i[2]-self.pos[2])
            glEnd()


        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-600-self.pos[0], 1-self.pos[1], -600-self.pos[2])
        glVertex3f(600-self.pos[0], 1-self.pos[1], -600-self.pos[2])
        glVertex3f(600-self.pos[0], 1-self.pos[1], 600-self.pos[2])
        glVertex3f(-600-self.pos[0], 1-self.pos[1], 600-self.pos[2])
        glEnd()

        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(-200-self.pos[0], 0-self.pos[1], -200-self.pos[2])
        glVertex3f(200-self.pos[0], 0-self.pos[1], -200-self.pos[2])
        glVertex3f(200-self.pos[0], 0-self.pos[1], 200-self.pos[2])
        glVertex3f(-200-self.pos[0], 0-self.pos[1], 200-self.pos[2])
        glEnd()

        glColor3f(0, 1, 1)
        if self.druhy[1] <= 0:
            glColor3f(1, 0, 0)
        glBegin(GL_QUADS)
        for vrchol in vrcholy:
            glVertex3fv([vrchol[0] + self.druhy[0][0] - self.pos[0],
                        vrchol[1] + self.druhy[0][1] - self.pos[1]+1,
                        vrchol[2] + self.druhy[0][2] - self.pos[2]])
        glEnd()

        mapa = []
        glColor3f(1, 0, 1)
        for x in range(20):
            for y in range(20):
                if bludiste.get_at((x,y)) == (0,0,0):
                    mapa.append([x*20-190,y*20-190])
        vrcholy_kresleni = []
        indexy_kresleni = []
        for i in range(len(mapa)):
            vrcholy_kresleni.extend([
            -10+mapa[i][0]-self.pos[0], -10+-2-self.pos[1]+1, 10+mapa[i][1]-self.pos[2],
            10+mapa[i][0]-self.pos[0], -10+-2-self.pos[1]+1, 10+mapa[i][1]-self.pos[2],
            10+mapa[i][0]-self.pos[0], 10+-2-self.pos[1]+1, 10+mapa[i][1]-self.pos[2],
            -10+mapa[i][0]-self.pos[0], 10+-2-self.pos[1]+1, 10+mapa[i][1]-self.pos[2],
            -10+mapa[i][0]-self.pos[0], -10+-2-self.pos[1]+1, -10+mapa[i][1]-self.pos[2],
            10+mapa[i][0]-self.pos[0], -10+-2-self.pos[1]+1, -10+mapa[i][1]-self.pos[2],
            10+mapa[i][0]-self.pos[0], 10+-2-self.pos[1]+1, -10+mapa[i][1]-self.pos[2],
            -10+mapa[i][0]-self.pos[0], 10+-2-self.pos[1]+1, -10+mapa[i][1]-self.pos[2]])
            for index in [0,1,2,3,1,5,6,2,5,4,7,6,4,0,3,7,3,2,6,7,0,4,5,1]:
                indexy_kresleni.extend([index+i*8])
        vrcholy_array = numpy.array(vrcholy_kresleni, dtype=numpy.float32)
        indexy_array = numpy.array(indexy_kresleni, dtype=numpy.uint32)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vrcholy_array)
        glDrawElements(GL_QUADS, len(indexy_array), GL_UNSIGNED_INT, indexy_array)
        glDisableClientState(GL_VERTEX_ARRAY)

        glColor3f(1, 1, 1)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluOrtho2D(0, 1600, 0, 1000)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        glLineWidth(3)

        glBegin(GL_LINES)
        glVertex2f(800,500-20)
        glVertex2f(800,500+20)
        glVertex2f(800-20,500)
        glVertex2f(800+20,500)
        glEnd()

        glLineWidth(1)

        if self.druhy[3] or self.mrtev:
            glColor3f(1, 0, 0)
            glBegin(GL_QUADS)
            glVertex2f(0,0)
            glVertex2f(1600,0)
            glVertex2f(1600,1000)
            glVertex2f(0,1000)
            glEnd()

        text_surface = pygame.font.Font(None, 36).render('životy: '+str(self.zivoty), True, (255, 255, 255, 255), (0, 0, 0, 255))
        glRasterPos2d(0, 0)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(text_surface, "RGBA", True))

        if self.zbran.nabijeni <= 0:
            text_surface = pygame.font.Font(None, 36).render('nabito', True, (255, 255, 255, 255), (0, 0, 0, 255))
        else:
            text_surface = pygame.font.Font(None, 36).render('nabíjení...', True, (255, 255, 255, 255), (0, 0, 0, 255))
        glRasterPos2d(0, 25)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(text_surface, "RGBA", True))
        bludiste_cele = pygame.transform.scale(bludiste,(400,400))


        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
        pygame.time.wait(25)
    async def tik2(self):
        await asyncio.gather(self.tik(),self.posli(),self.prijmi())



def posli(sl):
    try:
        conn.send(json.dumps(sl).encode())
    except:
        soc.send(json.dumps(sl).encode())

def prijmi():
    try:
        conn.settimeout(0.01)
        try:
            return json.loads(conn.recv(1024).decode())
        except:
            return ''
    except:
        soc.settimeout(0.01)
        try:
            return json.loads(soc.recv(1024).decode())
        except:
            return ''

bludiste_str = b'''\
\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\
'''
bludiste_obr = pygame.image.fromstring(bludiste_str,(20,20),'RGB')

bludiste = pygame.Surface((20,20))
bludiste.blit(bludiste_obr,(0,0))
bludiste_cele = pygame.Surface((400,400))
bludiste_cele.blit(pygame.transform.scale(bludiste_obr,(400,400)),(0,0))
hra=Hra()


