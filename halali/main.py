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

import pygame
import random
import numpy
import asyncio
import json
pygame.init()
file = '/'.join(os.path.abspath(__file__).split('/')[:-1])+'/'
obrazky = {
'l': pygame.image.load(file+'obrazky/liska.png'),
'me': pygame.image.load(file+'obrazky/medved.png'),
'd': pygame.image.load(file+'obrazky/drevorubec.png'),
'my0': pygame.image.load(file+'obrazky/myslivec0.png'),
'my1': pygame.image.load(file+'obrazky/myslivec1.png'),
'my2': pygame.image.load(file+'obrazky/myslivec2.png'),
'my3': pygame.image.load(file+'obrazky/myslivec3.png'),
'k': pygame.image.load(file+'obrazky/kachna.png'),
'b': pygame.image.load(file+'obrazky/bazant.png'),
's1': pygame.image.load(file+'obrazky/strom1.png'),
's2': pygame.image.load(file+'obrazky/strom2.png'),
'lv': pygame.image.load(file+'obrazky/liska_v.png'),
'mev': pygame.image.load(file+'obrazky/medved_v.png'),
'dv': pygame.image.load(file+'obrazky/drevorubec_v.png'),
'my0v': pygame.image.load(file+'obrazky/myslivec0_v.png'),
'my1v': pygame.image.load(file+'obrazky/myslivec1_v.png'),
'my2v': pygame.image.load(file+'obrazky/myslivec2_v.png'),
'my3v': pygame.image.load(file+'obrazky/myslivec3_v.png'),
'kv': pygame.image.load(file+'obrazky/kachna_v.png'),
'bv': pygame.image.load(file+'obrazky/bazant_v.png'),
'p': pygame.image.load(file+'obrazky/plan.png'),
'.': pygame.image.load(file+'obrazky/prazdne.png'),
'm': pygame.image.load(file+'obrazky/muze.png')
}
obrazky['m'].set_colorkey('#ffffff')

body = {'k':2,'b':3,'l':5,'my0':5,'my1':5,'my2':5,'my3':5,'d':5,'me':10,'s1':2,'s2':2,' ':0}

class Hra:
    def __init__(self):
        karticky = ['l']*6+['me']*2+['d']*2+['my']*8+['k']*7+['b']*8+['s1']*7+['s2']*8
        self.plan = numpy.full((7,7),'xxx')
        self.plan = list(self.plan)
        for i in range(len(self.plan)):
            self.plan[i] = list(self.plan[i])
        for y in range(7):
            for x in range(7):
                if not (y == 3 and x == 3):
                    self.plan[y][x] = '.' + karticky.pop(karticky.index(random.choice(karticky)))
                    #self.plan[y][x] = karticky.pop(karticky.index(random.choice(karticky)))
                    if self.plan[y][x] == '.my':
                        self.plan[y][x] += random.choice(['0','1','2','3'])
        self.plan[3][3] = ' '
        self.screen = pygame.display.set_mode([914,964])
        self.run = True
        if server_or_client == 'server':
            self.hraje = True
        else:
            self.hraje = False
        self.vybrano = None
        self.hraje_za = None
        self.muze_cele = None
        self.body = 0
        self.protihracovy_body = 0
        self.zbyva_tahu = None
        self.muze_vyvest = False
    def main(self):
        while self.run:
            asyncio.run(self.tik())
    async def nakresli(self):
        self.screen.fill((0,0,0))
        self.screen.blit(obrazky['p'],[0,0])
        for x in range(7):
            for y in range(7):
                if self.plan[y][x] != ' ':
                    if self.plan[y][x][0] == '.':
                        self.screen.blit(obrazky['.'],[6+(x*1.009)*128,6+(y*1.009)*128])
                    else:
                        if self.vybrano and self.vybrano[0] == x and self.vybrano[1] == y:
                            self.screen.blit(obrazky[self.plan[y][x]+'v'],[6+(x*1.009)*128,6+(y*1.009)*128])
                        else:
                            self.screen.blit(obrazky[self.plan[y][x]],[6+(x*1.009)*128,6+(y*1.009)*128])
        if self.muze_cele:
            for i in self.muze_cele:
                self.screen.blit(obrazky['m'],[6+(i[0]*1.009)*128,6+(i[1]*1.009)*128])
        self.screen.blit(pygame.font.SysFont('Arial',20).render('Tvoje body: '+str(self.body),True,(255,255,255)),(10,915))
        self.screen.blit(pygame.font.SysFont('Arial',20).render('Protivníkovy body: '+str(self.protihracovy_body),True,(255,255,255)),(10,940))
        if self.hraje:
            self.screen.blit(pygame.font.SysFont('Arial',20).render('JSI NA TAHU',True,(0,255,0)),(300,915))
        if self.hraje_za == 'z':
            self.screen.blit(pygame.font.SysFont('Arial',20).render('hraješ za zvířata',True,(0,255,255)),(300,940))
        if self.hraje_za == 'l':
            self.screen.blit(pygame.font.SysFont('Arial',20).render('hraješ za lidi',True,(255,255,0)),(300,940))
        if self.zbyva_tahu:
            self.screen.blit(pygame.font.SysFont('Arial',20).render('zbývající tahy: '+str(self.zbyva_tahu),True,(255,255,0)),(500,940))
        if self.muze_vyvest:
            self.screen.blit(pygame.font.SysFont('Arial',20).render('VYVÉST',True,(0,0,0),(255,255,255)),(800,915))
        pygame.display.flip()
    async def update(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                self.run = False
        if self.hraje:
            tahne_z_pos = [7,7]
            tahne_na_pos = None
            if pygame.mouse.get_pressed()[0]:
                if not self.muze_cele:
                    tahne_z_pos = (int((pygame.mouse.get_pos()[0]*1.009)//128),int((pygame.mouse.get_pos()[1]*1.009)//128))
                else:
                    tahne_na_pos = [int((pygame.mouse.get_pos()[0]*1.009)//128),int((pygame.mouse.get_pos()[1]*1.009)//128)]
                if tahne_z_pos[0] != 7 and tahne_z_pos[1] != 7:
                    if self.plan[tahne_z_pos[1]][tahne_z_pos[0]][0] == '.':
                        self.plan[tahne_z_pos[1]][tahne_z_pos[0]] = self.plan[tahne_z_pos[1]][tahne_z_pos[0]][1:]
                        self.vybrano = None
                        self.muze_cele = None
                        self.hraje = False
                        if self.zbyva_tahu:
                            self.zbyva_tahu -= 1
                        if not self.hraje_za and (self.plan[tahne_z_pos[1]][tahne_z_pos[0]] == 'me' or
                                                  self.plan[tahne_z_pos[1]][tahne_z_pos[0]] == 'l'):
                            self.hraje_za = 'z'
                        if not self.hraje_za and ('my' in self.plan[tahne_z_pos[1]][tahne_z_pos[0]]  or
                                                  self.plan[tahne_z_pos[1]][tahne_z_pos[0]] == 'd'):
                            self.hraje_za = 'l'
                        posli([self.plan,self.hraje_za,self.body])
                    else:
                        if self.hraje_za == 'z':
                            if self.plan[tahne_z_pos[1]][tahne_z_pos[0]] in 'lmebk':
                                self.vybrano = tahne_z_pos
                        if self.hraje_za == 'l':
                            if self.plan[tahne_z_pos[1]][tahne_z_pos[0]] in 'my0my1my2my3dbk':
                                self.vybrano = tahne_z_pos
                        if self.hraje_za == None:
                            if self.plan[tahne_z_pos[1]][tahne_z_pos[0]] in 'bk':
                                self.vybrano = tahne_z_pos
                if self.vybrano:
                    self.muze_cele = self.muze()
                    if tahne_na_pos:
                        if tahne_na_pos in self.muze_cele:
                            self.body += body[self.plan[tahne_na_pos[1]][tahne_na_pos[0]]]
                            self.plan[tahne_na_pos[1]][tahne_na_pos[0]] = self.plan[self.vybrano[1]][self.vybrano[0]]
                            self.plan[self.vybrano[1]][self.vybrano[0]] = ' '
                            self.vybrano = None
                            self.muze_cele = None
                            self.hraje = False
                            if self.zbyva_tahu:
                                self.zbyva_tahu -= 1
                            posli([self.plan,self.hraje_za,self.body])
                        elif tahne_na_pos != list(self.vybrano) and not pygame.Rect(800,915,80,25).collidepoint(pygame.mouse.get_pos()):
                            self.muze_cele = None
                            self.vybrano = None
                    if pygame.Rect(800,915,80,25).collidepoint(pygame.mouse.get_pos()):
                        self.body += body[self.plan[self.vybrano[1]][self.vybrano[0]]]
                        self.plan[self.vybrano[1]][self.vybrano[0]] = ' '
                        self.vybrano = None
                        self.muze_cele = None
                        self.hraje = False
                        posli([self.plan,self.hraje_za,self.body])
                        if self.zbyva_tahu:
                            self.zbyva_tahu -= 1
                br = False
                if self.zbyva_tahu == None:
                    for y in self.plan:
                        for x in y:
                            if '.' in x:
                                br = True
                    if not br:
                        self.zbyva_tahu = 5
            if (self.zbyva_tahu and
                self.vybrano and ((
                ([0,3] in self.muze_cele and self.plan[3][0] == ' ') or
                ([3,0] in self.muze_cele and self.plan[0][3] == ' ') or
                ([6,3] in self.muze_cele and self.plan[3][6] == ' ') or
                ([3,6] in self.muze_cele and self.plan[6][3] == ' ')) or (
                (0,3) == self.vybrano or
                (3,0) == self.vybrano or
                (6,3) == self.vybrano or
                (3,6) == self.vybrano)) and
                (self.vybrano[0] == 3 or
                self.vybrano[1] == 3 or
                (self.vybrano[0] == 3 and self.vybrano[1] == 3))):
                self.muze_vyvest = True
            else:
                self.muze_vyvest = False


    def muze(self):
        muze = []
        muze_p = []
        muze_p1 = []
        muze_p2 = []
        muze_p3 = []
        muze_p4 = []
        if self.plan[self.vybrano[1]][self.vybrano[0]] == 'me':
            muze_p = [[self.vybrano[0]+1,self.vybrano[1]],
                      [self.vybrano[0]-1,self.vybrano[1]],
                      [self.vybrano[0],self.vybrano[1]+1],
                      [self.vybrano[0],self.vybrano[1]-1]]
            for i in muze_p:
                try:
                    if self.plan[i[1]][i[0]] in ' dmy0my1my2my3':
                        muze.append(i)
                except:
                    pass
        if self.plan[self.vybrano[1]][self.vybrano[0]] == 'd':
            muze_p = [[self.vybrano[0]+1,self.vybrano[1]],
                      [self.vybrano[0]-1,self.vybrano[1]],
                      [self.vybrano[0],self.vybrano[1]+1],
                      [self.vybrano[0],self.vybrano[1]-1]]
            for i in muze_p:
                try:
                    if self.plan[i[1]][i[0]] in ' s1s2':
                        muze.append(i)
                except:
                    pass
        if self.plan[self.vybrano[1]][self.vybrano[0]] == 'l':
            for i in range(len(self.plan[:][:self.vybrano[0]])):
                muze_p1.append([i,self.vybrano[1]])
            for i in range(len(self.plan[:][self.vybrano[0]+1:])):
                muze_p2.append([self.vybrano[0]+1+i,self.vybrano[1]])
            for i in range(len(self.plan[:self.vybrano[1]][:])):
                muze_p3.append([self.vybrano[0],i])
            for i in range(len(self.plan[self.vybrano[1]+1:][:])):
                muze_p4.append([self.vybrano[0],self.vybrano[1]+1+i])
            muze_p1.reverse()
            muze_p3.reverse()
            muze_p.append(muze_p1)
            muze_p.append(muze_p2)
            muze_p.append(muze_p3)
            muze_p.append(muze_p4)
            for y in muze_p:
                for i in y:
                    if self.plan[i[1]][i[0]] == ' ':
                        muze.append(i)
                    elif self.plan[i[1]][i[0]] in 'kb':
                        muze.append(i)
                        break
                    else:
                        break
        if self.plan[self.vybrano[1]][self.vybrano[0]] in 'kb':
            for i in range(len(self.plan[:][:self.vybrano[0]])):
                muze_p1.append([i,self.vybrano[1]])
            for i in range(len(self.plan[:][self.vybrano[0]+1:])):
                muze_p2.append([self.vybrano[0]+1+i,self.vybrano[1]])
            for i in range(len(self.plan[:self.vybrano[1]][:])):
                muze_p3.append([self.vybrano[0],i])
            for i in range(len(self.plan[self.vybrano[1]+1:][:])):
                muze_p4.append([self.vybrano[0],self.vybrano[1]+1+i])
            muze_p1.reverse()
            muze_p3.reverse()
            muze_p.append(muze_p1)
            muze_p.append(muze_p2)
            muze_p.append(muze_p3)
            muze_p.append(muze_p4)
            for y in muze_p:
                for i in y:
                    if self.plan[i[1]][i[0]] == ' ':
                        muze.append(i)
                    else:
                        break
        if self.plan[self.vybrano[1]][self.vybrano[0]] in 'my0my1my2my3':
            for i in range(len(self.plan[:][:self.vybrano[0]])):
                muze_p1.append([i,self.vybrano[1]])
            for i in range(len(self.plan[:][self.vybrano[0]+1:])):
                muze_p2.append([self.vybrano[0]+1+i,self.vybrano[1]])
            for i in range(len(self.plan[:self.vybrano[1]][:])):
                muze_p3.append([self.vybrano[0],i])
            for i in range(len(self.plan[self.vybrano[1]+1:][:])):
                muze_p4.append([self.vybrano[0],self.vybrano[1]+1+i])
            muze_p1.reverse()
            muze_p3.reverse()
            if self.plan[self.vybrano[1]][self.vybrano[0]] != 'my2':
                muze_p.append(muze_p1)
            if self.plan[self.vybrano[1]][self.vybrano[0]] != 'my0':
                muze_p.append(muze_p2)
            if self.plan[self.vybrano[1]][self.vybrano[0]] != 'my3':
                muze_p.append(muze_p3)
            if self.plan[self.vybrano[1]][self.vybrano[0]] != 'my1':
                muze_p.append(muze_p4)
            if self.plan[self.vybrano[1]][self.vybrano[0]] == 'my2':
                for i in muze_p1:
                    if self.plan[i[1]][i[0]] == ' ':
                        muze.append(i)
                    elif self.plan[i[1]][i[0]] in 'kblme':
                        muze.append(i)
                        break
                    else:
                        break
            if self.plan[self.vybrano[1]][self.vybrano[0]] == 'my0':
                for i in muze_p2:
                    if self.plan[i[1]][i[0]] == ' ':
                        muze.append(i)
                    elif self.plan[i[1]][i[0]] in 'kblme':
                        muze.append(i)
                        break
                    else:
                        break
            if self.plan[self.vybrano[1]][self.vybrano[0]] == 'my3':
                for i in muze_p3:
                    if self.plan[i[1]][i[0]] == ' ':
                        muze.append(i)
                    elif self.plan[i[1]][i[0]] in 'kblme':
                        muze.append(i)
                        break
                    else:
                        break
            if self.plan[self.vybrano[1]][self.vybrano[0]] == 'my1':
                for i in muze_p4:
                    if self.plan[i[1]][i[0]] == ' ':
                        muze.append(i)
                    elif self.plan[i[1]][i[0]] in 'kblme':
                        muze.append(i)
                        break
                    else:
                        break
            for y in muze_p:
                for i in y:
                    if self.plan[i[1]][i[0]] == ' ':
                        muze.append(i)
                    else:
                        break
        return muze
    async def prijmi(self):
        sl = prijmi()
        if sl != '':
            self.hraje = True
            self.plan = sl[0]
            if sl[1] == 'l':
                self.hraje_za = 'z'
            if sl[1] == 'z':
                self.hraje_za = 'l'
            self.protihracovy_body = sl[2]
        br = False
        if self.zbyva_tahu == None:
            for y in self.plan:
                for x in y:
                    if '.' in x:
                        br = True
            if not br:
                self.zbyva_tahu = 5
    async def tik(self):
        await asyncio.gather(self.update(),self.prijmi(),self.nakresli())

def posli(sl):
    try:
        try:
            conn.send(json.dumps(sl).encode())
        except:
            soc.send(json.dumps(sl).encode())
    except:
        pass

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

hra = Hra()
hra.main()
tk2 = tkinter.Tk()
tk2.option_add('*Font','Arial 15')
if hra.body < hra.protihracovy_body:
    tkinter.Label(text='Prohrál jsi').pack()
if hra.body > hra.protihracovy_body:
    tkinter.Label(text='Vyhrál jsi').pack()
if hra.body == hra.protihracovy_body:
    tkinter.Label(text='Remíza').pack()
tk2.mainloop()
