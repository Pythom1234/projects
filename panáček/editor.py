
'''
tento editor je navržen pro kresleni map k programu 'panacek.py'

velikost_x = sirka,
velikost_y = vyska
'''


import glob
import pyglet
import numpy
import json

jmeno = input('Jmeno mapy: ')
if 'mapy/' + jmeno + '.json' in glob.glob('mapy/*'):
    with open('mapy/'+jmeno+'.json') as soubor:
            slovnik = json.load(soubor)
            mapa = slovnik['mapa']
            pozice = slovnik['pozice']
            velikost_x = len(mapa[0])
            velikost_y = len(mapa)
else:
    try:
        velikost_x = int(input('Sirka mapy (ve ctvereccich; max. 88): '))
    except:
        velikost_x = 30
    try:
        velikost_y = int(input('Vyska mapy (ve ctvereccich; max. 51): '))
    except:
        velikost_y = 20
    mapa = list(numpy.zeros((velikost_y,velikost_x)))
    for i in range(velikost_y):
        mapa[i] = list(mapa[i])
    pozice = [0,0]
    mapa[0] = [1]*velikost_x
    mapa[-1] = [1]*velikost_x
    for i in range(len(mapa)):
        mapa[i][0] = 1
        mapa[i][-1] = 1
    for i in range(len(mapa)):
        for y in range(len(mapa[i])):
            mapa[i][y] = int(mapa[i][y])
win2 = pyglet.window.Window(caption='Panacek: Napoveda',width = 366,height = 166, style=pyglet.window.Window.WINDOW_STYLE_DIALOG)
win2.set_icon(pyglet.image.load('obrazky/panacek_16_nap.png'),pyglet.image.load('obrazky/panacek_32_nap.png'))
win2.set_location(1100,540)
window = pyglet.window.Window(caption='Panacek: Editor',width = velikost_x*20,height = velikost_y*20)
window.set_icon(pyglet.image.load('obrazky/panacek_16_edit.png'),pyglet.image.load('obrazky/panacek_32_edit.png'))
napoveda = pyglet.image.load('obrazky/napoveda.png')
zed = pyglet.image.load('obrazky/ctverecek.png')
stanoviste_h = pyglet.image.load('obrazky/stanoviste_h.png')
stanoviste_n = pyglet.image.load('obrazky/stanoviste_n.png')
panacek_m = pyglet.image.load('obrazky/panacek_m.png')
klic = pyglet.image.load('obrazky/klic.png')
dvere = pyglet.image.load('obrazky/dvere.png')
panacek_v = pyglet.image.load('obrazky/panacek_v.png')
panacek = pyglet.image.load('obrazky/panacek.png')
panacek_s = pyglet.image.load('obrazky/panacek_s.png')
penizek = pyglet.image.load('obrazky/penizek.png')
trampolina = pyglet.image.load('obrazky/trampolina.png')
bodaky = pyglet.image.load('obrazky/bodaky.png')
cil = pyglet.image.load('obrazky/cil.png')
vybrany = 0
vybrano = 1
konec = False
porad = False
batch = pyglet.graphics.Batch()
pozice_mysi = {'x' : 0, 'y' : 0}
kliknuto = None
sprites = []
klavesy = []
co_to_znamena = {
0:'nic',
1:'zed',
2:'bodaky',
3:'trampolina',
4:'cil',
5:'penizek',
6:'stanoviste_nehotove',
7:'stanoviste_hotove',
8:'klic',
9:'dvere'
}

def stisk_klavesy(klavesa, modifikatory):
    global vybrano, mapa, pozice, konec
    if klavesa == pyglet.window.key.D:
        vybrano += 1
        if vybrano == 7:
            vybrano = 8
        if vybrano == 10:
            vybrano = 0
    elif klavesa == pyglet.window.key.S:
        mapa = list(numpy.full((velikost_y,velikost_x),vybrano))
        for i in range(velikost_y):
            mapa[i] = list(mapa[i])
        mapa[0] = [1]*velikost_x
        mapa[-1] = [1]*velikost_x
        for i in range(len(mapa)):
            mapa[i][0] = 1
            mapa[i][-1] = 1
        for i in range(len(mapa)):
            for y in range(len(mapa[i])):
                mapa[i][y] = int(mapa[i][y])
    elif klavesa == pyglet.window.key.A:
        pozice = [pozice_mysi['x']//20, velikost_y-pozice_mysi['y']//20-1]
    elif klavesa == pyglet.window.key.F1:
        vybrano = 0
    elif klavesa == pyglet.window.key.F2:
        vybrano = 1
    elif klavesa == pyglet.window.key.F3:
        vybrano = 2
    elif klavesa == pyglet.window.key.F4:
        vybrano = 3
    elif klavesa == pyglet.window.key.F5:
        vybrano = 4
    elif klavesa == pyglet.window.key.F6:
        vybrano = 5
    elif klavesa == pyglet.window.key.F7:
        vybrano = 6
    elif klavesa == pyglet.window.key.F8:
        vybrano = 8
    elif klavesa == pyglet.window.key.F9:
        vybrano = 9
    elif klavesa == pyglet.window.key.F:
        jmeno_souboru = jmeno
        with open('mapy/'+jmeno_souboru+'.json', mode = 'w') as soubor:
            soubor.write(json.dumps({'mapa':mapa, 'pozice':pozice}))
        konec = True

def stisk(x, y, tlacitko, modifikatory):
    global kliknuto, porad
    kliknuto = {'x' : x, 'y' : y, 'tlacitko' : tlacitko}
    if tlacitko == 2:
        if porad == True:
            porad = False
        else:
            porad = True

def pohyb(x, y, dx, dy):
    global pozice_mysi
    pozice_mysi = {'x' : x, 'y' : y}

def pusteni(x, y, tlacitko, modifikatory):
    global kliknuto
    kliknuto = None

def kresleni():
    try:
        if kliknuto['tlacitko'] == 1:
            mapa[len(mapa)-kliknuto['y']//20-1][kliknuto['x']//20] = vybrano
        elif kliknuto['tlacitko'] == 4:
            mapa[len(mapa)-kliknuto['y']//20-1][kliknuto['x']//20] = 0
    except:
        pass
    try:
        if porad == True:
            mapa[len(mapa)-pozice_mysi['y']//20-1][pozice_mysi['x']//20] = vybrano
    except:
        pass

def tik(dt):
    kresleni()
    if konec:
        exit('SAVE')
    print('Vybrano:',co_to_znamena[vybrano])

def vykr2():
    sprite_napoveda = pyglet.sprite.Sprite(napoveda, x=3, y=3)
    sprite_napoveda.draw()

def zavreno():
    exit()

def vykresli():
    global sprites
    sprites.clear()
    window.clear()
    mapa.reverse()
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if mapa[y][x] == 0:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek,x=x*20,y=y*20,batch=batch)) 
            if mapa[y][x] == 1:
                sprites.append(pyglet.sprite.Sprite(zed,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 2:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_m,x=x*20,y=y*20,batch=batch))
                else:
                    sprites.append(pyglet.sprite.Sprite(bodaky,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 3:
                sprites.append(pyglet.sprite.Sprite(trampolina,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 4:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_v,x=x*20,y=y*20,batch=batch))
                else:
                    sprites.append(pyglet.sprite.Sprite(cil,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 5:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek,x=x*20,y=y*20,batch=batch))
                else:
                    sprites.append(pyglet.sprite.Sprite(penizek,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 6:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_s,x=x*20,y=y*20,batch=batch)) 
                else:
                    sprites.append(pyglet.sprite.Sprite(stanoviste_n,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 7:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek_s,x=x*20,y=y*20,batch=batch)) 
                else:
                    sprites.append(pyglet.sprite.Sprite(stanoviste_h,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 8:
                if pozice[0] == x and pozice[1] == len(mapa)-y-1:
                    sprites.append(pyglet.sprite.Sprite(panacek,x=x*20,y=y*20,batch=batch)) 
                else:
                    sprites.append(pyglet.sprite.Sprite(klic,x=x*20,y=y*20,batch=batch))
            if mapa[y][x] == 9:
                sprites.append(pyglet.sprite.Sprite(dvere,x=x*20,y=y*20,batch=batch))
    mapa.reverse()
    batch.draw()
    sprites.clear()

window.push_handlers(
on_draw = vykresli,
on_mouse_press = stisk,
on_mouse_motion = pohyb,
on_mouse_release = pusteni,
on_key_press = stisk_klavesy,
on_close = zavreno,
)
win2.push_handlers(on_draw = vykr2,on_close = zavreno)

pyglet.clock.schedule(tik)

pyglet.app.run()
