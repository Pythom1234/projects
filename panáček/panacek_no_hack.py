#!/usr/bin/python3
#!venv/bin/python3
'↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑'



import time
import pyglet
import json
import glob
import threading
import datetime


vsechny_mapy = glob.glob('mapy/*.json')
vsechny_mapy.sort()
for i in vsechny_mapy:
    vsechny_mapy[vsechny_mapy.index(i)] = (vsechny_mapy[vsechny_mapy.index(i)])[5:-5]
while True:
    print('Mas tyto mapy:',str(vsechny_mapy)[1:-1])
    nazev_mapy = input('Kterou chces hrat? ')
    try:
        with open('mapy/'+nazev_mapy+'.json') as soubor:
            slovnik = json.load(soubor)
            mapa = slovnik['mapa']
            startovni_pozice = slovnik['pozice']
        break
    except:
        pass
penize_celkem = 0
for i in range(len(mapa)):
    penize_celkem += mapa[i].count(5)
velikost_ctverecku = 20
window = pyglet.window.Window(caption='Panacek', width=len(mapa[0])*velikost_ctverecku, height=len(mapa)*velikost_ctverecku+velikost_ctverecku)
window.set_icon(pyglet.image.load('obrazky/panacek_32.png'),pyglet.image.load('obrazky/panacek_16.png'))
zed = pyglet.image.load('obrazky/ctverecek.png')
stanoviste_h = pyglet.image.load('obrazky/stanoviste_h.png')
stanoviste_n = pyglet.image.load('obrazky/stanoviste_n.png')
panacek_m = pyglet.image.load('obrazky/panacek_m.png')
panacek_v = pyglet.image.load('obrazky/panacek_v.png')
klic = pyglet.image.load('obrazky/klic.png')
dvere = pyglet.image.load('obrazky/dvere.png')
panacek = pyglet.image.load('obrazky/panacek.png')
panacek_s = pyglet.image.load('obrazky/panacek_s.png')
penizek = pyglet.image.load('obrazky/penizek.png')
trampolina = pyglet.image.load('obrazky/trampolina.png')
bodaky = pyglet.image.load('obrazky/bodaky.png')
cil = pyglet.image.load('obrazky/cil.png')
batch = pyglet.graphics.Batch()
pozice = startovni_pozice.copy()
sprites = []
klavesy = []
posledni_stanoviste = startovni_pozice.copy()
penize = 0
zivot = 1
ma_klic = False
thread = None
co_to_znamena = {0:'nic',
                 1:'zed',
                 2:'bodaky',
                 3:'trampolina',
                 4:'cil',
                 5:'penizek',
                 6:'stanoviste_nehotove',
                 7:'stanoviste_hotove',
                 8:'klic',
                 9:'dvere'}
start = datetime.datetime.now()
stop = 0

#pozice 0,0 je vlevo nahore

def stisk(kl,mod):
    global pozice, posledni_stanoviste, zivot
    if kl == pyglet.window.key.LEFT:
        klavesy.append('LEFT')
    if kl == pyglet.window.key.RIGHT:
        klavesy.append('RIGHT')
    if kl == pyglet.window.key.UP:
        klavesy.append('UP')
    if kl == pyglet.window.key.K:
        zivot += 1
        pozice = posledni_stanoviste.copy()
    if kl == pyglet.window.key.F:
        klavesy.append('F')
    if kl == pyglet.window.key.R:
        pozice = startovni_pozice.copy()
    if kl == pyglet.window.key.N:
        if co_je() == 7:
            mapa[pozice[1]][pozice[0]] = 7
            posledni_stanoviste = pozice.copy()
    
def pusteni(kl,mod):
    if kl == pyglet.window.key.LEFT:
        klavesy.remove('LEFT')
    if kl == pyglet.window.key.RIGHT:
        klavesy.remove('RIGHT')    
    if kl == pyglet.window.key.UP:
        klavesy.remove('UP')
    if kl == pyglet.window.key.F:
        klavesy.remove('F')

def co_je(kde='h', slovy=False):
    if slovy == True:
        if kde == 'h':
            return co_to_znamena[mapa[pozice[1]][pozice[0]]]
        if kde == 'u':
            return co_to_znamena[mapa[pozice[1]-1][pozice[0]]]
        if kde == 'd':
            return co_to_znamena[mapa[pozice[1]+1][pozice[0]]]
        if kde == 'l':
            return co_to_znamena[mapa[pozice[1]][pozice[0]-1]]
        if kde == 'r':
            return co_to_znamena[mapa[pozice[1]][pozice[0]+1]]
    elif slovy == False:
        if kde == 'h':
            return mapa[pozice[1]][pozice[0]]
        if kde == 'u':
            return mapa[pozice[1]-1][pozice[0]]
        if kde == 'd':
            return mapa[pozice[1]+1][pozice[0]]
        if kde == 'l':
            return mapa[pozice[1]][pozice[0]-1]
        if kde == 'r':
            return mapa[pozice[1]][pozice[0]+1]

def u():
    global pozice
    pozice[1]-=1

def d():
    global pozice
    pozice[1]+=1

def l():
    global pozice
    pozice[0]-=1

def r():
    global pozice
    pozice[0]+=1

def mrtev(dt):
    global pozice
    pozice = posledni_stanoviste.copy()
    
def vyhral(dt):
    global stop
    stop = datetime.datetime.now()
    exit(f'''!YOU WON!\n{penize}/{penize_celkem} penez\nna {zivot} pokusu\ncas: {str(stop - start)[2:4]} min, {str(stop - start)[5:9]} s''')

def akce():
    global mapa, pozice, penize, posledni_stanoviste, zivot, ma_klic
    if co_je() == 6:
        mapa[pozice[1]][pozice[0]] = 7
        posledni_stanoviste = pozice.copy()
    if co_je() == 5:
        penize += 1
        mapa[pozice[1]][pozice[0]] = 0
    if co_je() == 2:
        zivot += 1
        pyglet.clock.schedule_once(mrtev,0.)
        time.sleep(0.45)
    if co_je() == 4:
        pyglet.clock.schedule_once(vyhral,0.1)
        time.sleep(0.1)
    if co_je() == 8 and ma_klic == False:
        ma_klic = True
        mapa[pozice[1]][pozice[0]] = 0
    if co_je('u') == 9 and ma_klic == True:
        mapa[pozice[1]-1][pozice[0]] = 0
        ma_klic = False
    if co_je('d') == 9 and ma_klic == True:
        mapa[pozice[1]+1][pozice[0]] = 0
        ma_klic = False
    if co_je('l') == 9 and ma_klic == True:
        mapa[pozice[1]][pozice[0]-1] = 0
        ma_klic = False
    if co_je('r') == 9 and ma_klic == True:
        mapa[pozice[1]][pozice[0]+1] = 0
        ma_klic = False

def pohyb():
    if not co_je() == 2:
        if (co_je('d') == 1 or co_je('d') == 3 or co_je('d') == 9) and 'F' in klavesy:
            if 'LEFT' in klavesy and 'F' in klavesy:
                for i in range(2):
                    if co_je('l') != 1 and co_je('l') != 3 and co_je('l') != 9 and (co_je('d') == 1 or co_je('d') == 3):
                        l()
                        akce()
            if 'RIGHT' in klavesy and 'F' in klavesy:
                for i in range(2):
                    if co_je('r') != 1 and co_je('r') != 3 and co_je('r') != 9 and (co_je('d') == 1 or co_je('d') == 3):
                        r()
                        akce()
        elif 'LEFT' in klavesy:
            if co_je('l') != 1 and co_je('l') != 3 and co_je('l') != 9:
                l()
        elif 'RIGHT' in klavesy:
            if co_je('r') != 1 and co_je('r') != 3 and co_je('r') != 9:
                r()

def nahoru(a):
    if co_je('u') !=1 and co_je('u') !=3  and co_je('u') != 9:
        u()

def skok(x):
    global mapa, pozice, penize, posledni_stanoviste, ma_klic
    for i in range(x):
        time.sleep(0.1)
        pyglet.clock.schedule_once(nahoru,0.1)
        if co_je() == 6:
            mapa[pozice[1]][pozice[0]] = 7
            posledni_stanoviste = pozice.copy()
        if co_je() == 5:
            penize += 1
            mapa[pozice[1]][pozice[0]] = 0
        if co_je() == 2:
            pyglet.clock.schedule_once(mrtev,0.)
            time.sleep(0.45)
        if co_je() == 4:
            pyglet.clock.schedule_once(vyhral,0.1)
            time.sleep(0.1)
        if co_je() == 8 and ma_klic == False:
            ma_klic = True
            mapa[pozice[1]][pozice[0]] = 0
        if co_je('u') == 9 and ma_klic == True:
            mapa[pozice[1]-1][pozice[0]] = 0
            ma_klic = False
        if co_je('d') == 9 and ma_klic == True:
            mapa[pozice[1]+1][pozice[0]] = 0
            ma_klic = False
        if co_je('l') == 9 and ma_klic == True:
            mapa[pozice[1]][pozice[0]-1] = 0
            ma_klic = False
        if co_je('r') == 9 and ma_klic == True:
            mapa[pozice[1]][pozice[0]+1] = 0
            ma_klic = False
        if co_je('u') == 1 and co_je('u') == 3  and co_je('u') == 9:
            break

def tik_skok(dt):
    global thread
#    if 'UP' in klavesy and (co_je('d') == 1 or (co_je('l') == 1 and 'LEFT' in klavesy) or (co_je('r') == 1 and 'RIGHT' in klavesy)):
    if 'UP' in klavesy and (co_je('d') == 1 or co_je('d') == 9):
        if threading.active_count() <= 1:
            thread = threading.Thread(target=skok, args=[4])
            thread.start()
    akce()

def tik_pohyb(dt):
    if 'LEFT' in klavesy or 'RIGHT' in klavesy:
        pohyb()
    akce()

def tik_dolu(dt):
    if threading.active_count() != 2:
        if co_je('d') == 0 or co_je('d') == 2 or co_je('d') == 4 or co_je('d') == 5 or co_je('d') == 6 or co_je('d') == 7 or co_je('d') == 8:
            d()
    akce()



def tik_akce(dt):
    akce()
    if co_je('d') == 3:
        if threading.active_count() <= 1:
            thread = threading.Thread(target=skok, args=[6])
            thread.start()
def vykr_sprites(dt):
    global sprites
    sprites.clear()
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if mapa[len(mapa)-y-1][x] == 0:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 1:
                sprites.append(pyglet.sprite.Sprite(zed,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 2:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_m,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
                else:
                    sprites.append(pyglet.sprite.Sprite(bodaky,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 3:
                sprites.append(pyglet.sprite.Sprite(trampolina,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 4:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_v,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
                else:
                    sprites.append(pyglet.sprite.Sprite(cil,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 5:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
                else:
                    sprites.append(pyglet.sprite.Sprite(penizek,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 6:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_s,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch)) 
                    sprites[-1].scale = velikost_ctverecku/20
                else:
                    sprites.append(pyglet.sprite.Sprite(stanoviste_n,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 7:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_s,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch)) 
                    sprites[-1].scale = velikost_ctverecku/20
                else:
                    sprites.append(pyglet.sprite.Sprite(stanoviste_h,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 8:
                sprites.append(pyglet.sprite.Sprite(klic,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                sprites[-1].scale = velikost_ctverecku/20
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                    sprites[-1].scale = velikost_ctverecku/20
            elif mapa[len(mapa)-y-1][x] == 9:
                sprites.append(pyglet.sprite.Sprite(dvere,x=x*velikost_ctverecku,y=y*velikost_ctverecku,batch=batch))
                sprites[-1].scale = velikost_ctverecku/20
    sprites.append(pyglet.sprite.Sprite(penizek,x=1,y=window.height-velikost_ctverecku,batch=batch))
    sprites[-1].scale = velikost_ctverecku/20
    sprites.append(pyglet.sprite.Sprite(panacek,x=window.width-velikost_ctverecku,y=window.height-velikost_ctverecku,batch=batch))
    sprites[-1].scale = velikost_ctverecku/20
    if ma_klic == True:
        sprites.append(pyglet.sprite.Sprite(klic,x=140*(velikost_ctverecku/20),y=window.height-velikost_ctverecku,batch=batch))
        sprites[-1].scale = velikost_ctverecku/20

def vykresli():
    global sprites
    window.clear()
    batch.draw()
    napis = pyglet.text.Label(f'{penize}/{penize_celkem}',font_size=velikost_ctverecku-2,x=velikost_ctverecku+3,y=window.height-velikost_ctverecku,color=(255,255,255,255))
    napis.draw()
    napis2 = pyglet.text.Label(f'{zivot}. ',font_size=velikost_ctverecku-2,anchor_x='right',x=window.width-23,y=window.height-velikost_ctverecku,color=(255,255,255,255))
    napis2.draw()

window.push_handlers(
on_draw=vykresli,
on_key_press=stisk,
on_key_release=pusteni,
)

pyglet.clock.schedule_interval(tik_skok,0.01)
pyglet.clock.schedule_interval(tik_pohyb,0.08)
pyglet.clock.schedule_interval(tik_dolu,0.2)
pyglet.clock.schedule(tik_akce)
pyglet.clock.schedule(vykr_sprites)
pyglet.app.run()

