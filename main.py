#!/usr/bin/python3

import cv2                                   #opencv-python
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw    #Pillow
import tkinter.simpledialog
import tkinter.messagebox
import tkinter.filedialog
import tkinter.colorchooser
import numpy                                 #numpy
import datetime
import sys

err_file = open('err.txt','w')
sys.stderr = err_file

tkroot = tk.Tk()



def add_scene(a=''):
    name = tkinter.simpledialog.askstring('Název scény','Zadejte název scény:')
    tksceny_listbox.insert(tk.END,name)
    sceny.append({'jmeno':name,'kamera':None,'kresleni':Image.new('RGBA', (640,480), (255, 255, 255, 0))})

def add_camera(a=''):
    try:
        sceny[tksceny_listbox.curselection()[0]]['kamera'] = cv2.VideoCapture(tkinter.simpledialog.askinteger('ID kamery','Zadejte ID kamery:'))
    except:
        pass

def draw_camera(id):
    if sceny[id]['kamera']:
        img = Image.fromarray(cv2.cvtColor(sceny[id]['kamera'].read()[1], cv2.COLOR_BGR2RGBA))
    else:
        img = Image.new('RGBA', (640, 480), (255,255,255,255))
    return img

def draw_sceny():
    global img2
    try:
        img1 = draw_camera(tksceny_listbox.curselection()[0])
        kresleni = sceny[tksceny_listbox.curselection()[0]]['kresleni']
        img1.paste(kresleni, (0, 0), kresleni)
        img1 = ImageTk.PhotoImage(img1)
        if img1:
            tkscena1_canvas.configure(width=img1.width(), height=img1.height())
            tkscena1_canvas.create_image(0, 0, anchor=tk.NW, image=img1)
            tkscena1_canvas.image = img1
    except:
        pass
    try:
        img2 = draw_camera(vybrana_scena)
        kresleni = sceny[tksceny_listbox.curselection()[0]]['kresleni']
        img2.paste(kresleni, (0, 0), kresleni)
        if pustene:
            img3 = ImageTk.PhotoImage(img2)
            if img3:
                tkscena2_canvas.configure(width=img3.width(), height=img3.height())
                tkscena2_canvas.create_image(0, 0, anchor=tk.NW, image=img3)
                tkscena2_canvas.image = img3
    except:
        pass
    tkroot.after(1,draw_sceny)

def save_sceny():
    if pustene and img2:
        frames.append(img2)
        tkdelka_label.config(text=f'délka: {len(frames)} snímků = {round((len(frames)*0.06),2)} sekund')
        tkroot.update_idletasks()
    tkroot.after(17,save_sceny)

def save_image(a=''):
    if img2:
        img3 = ImageTk.PhotoImage(img2)
        if img2:
            tkscena2_canvas.configure(width=img3.width(), height=img3.height())
            tkscena2_canvas.create_image(0, 0, anchor=tk.NW, image=img3)
            tkscena2_canvas.image = img3
        frames.append(img2)
        tkdelka_label.config(text=f'délka: {len(frames)} snímků = {round((len(frames)*0.06),2)} sekund')
        tkroot.update_idletasks()

def save_images(a=''):
    if img2:
        img3 = ImageTk.PhotoImage(img2)
        if img2:
            tkscena2_canvas.configure(width=img3.width(), height=img3.height())
            tkscena2_canvas.create_image(0, 0, anchor=tk.NW, image=img3)
            tkscena2_canvas.image = img3
        pocet_snimku = tkinter.simpledialog.askinteger('Počet snímků','Kolikrát tento snímek uložit',initialvalue=10)
        for i in range(pocet_snimku):
            frames.append(img2)
        tkdelka_label.config(text=f'délka: {len(frames)} snímků = {round((len(frames)*0.06),2)} sekund')
        tkroot.update_idletasks()

def save_images17(a=''):
    if img2:
        img3 = ImageTk.PhotoImage(img2)
        if img2:
            tkscena2_canvas.configure(width=img3.width(), height=img3.height())
            tkscena2_canvas.create_image(0, 0, anchor=tk.NW, image=img3)
            tkscena2_canvas.image = img3
        for i in range(17):
            frames.append(img2)
        tkdelka_label.config(text=f'délka: {len(frames)} snímků = {round((len(frames)*0.06),2)} sekund')
        tkroot.update_idletasks()


def save(a=''):
    video_writer = cv2.VideoWriter(
        tkinter.filedialog.asksaveasfilename(initialfile='output.avi',initialdir='~',defaultextension='.avi'),
        cv2.VideoWriter_fourcc(*'XVID'),
        16,
        (640,480))
    tksceny_listbox.selection_set(vybrana_scena)
    for frame in range(len(frames)):
        video_writer.write(cv2.cvtColor(numpy.array(frames[frame]),cv2.COLOR_RGB2BGR))
        print(f'ukládání snímku {frame+1} z {len(frames)}')
    video_writer.release()
    tkinter.messagebox.showinfo('Ukládání dokončeno','Video bylo úspěšně uloženo')
    tksceny_listbox.selection_set(vybrana_scena)

def pause(a=''):
    global pustene
    pustene = not pustene

def set_scene(a=''):
    global vybrana_scena
    vybrana_scena = tksceny_listbox.curselection()[0]

def del_frame(a=''):
    global frames
    frames = frames[:-1]
    tkdelka_label.config(text=f'délka: {len(frames)} snímků = {round((len(frames)*0.06),2)} sekund')
    img3 = ImageTk.PhotoImage(frames[-1])
    if img3:
        tkscena2_canvas.configure(width=img3.width(), height=img3.height())
        tkscena2_canvas.create_image(0, 0, anchor=tk.NW, image=img3)
        tkscena2_canvas.image = img3
    tkroot.update_idletasks()

def del_frames17(a=''):
    global frames
    frames = frames[:-17]
    tkdelka_label.config(text=f'délka: {len(frames)} snímků = {round((len(frames)*0.06),2)} sekund')
    img3 = ImageTk.PhotoImage(frames[-1])
    if img3:
        tkscena2_canvas.configure(width=img3.width(), height=img3.height())
        tkscena2_canvas.create_image(0, 0, anchor=tk.NW, image=img3)
        tkscena2_canvas.image = img3
    tkroot.update_idletasks()

def draw(event):
    global posledni
    if posledni == None:
        posledni = (event.x,event.y)
    kreslic = ImageDraw.Draw(sceny[tksceny_listbox.curselection()[0]]['kresleni'])
    polomer = tktloustka_scale.get() // 2
    kreslic.line([posledni, (event.x, event.y)], barva, tktloustka_scale.get())
    kreslic.ellipse([event.x - polomer, event.y - polomer, event.x + polomer, event.y + polomer], fill=barva)
    posledni = (event.x,event.y)

def end_draw(a=''):
    global posledni
    posledni = None

def clear_draw(a=''):
    global kreslic
    sceny[tksceny_listbox.curselection()[0]]['kresleni'] = Image.new('RGBA', (640,480), (255, 255, 255, 0))

def set_color(a=''):
    global barva
    barva = (tkr_scale.get(),tkg_scale.get(),tkb_scale.get(),tka_scale.get())
    tkr_entry.delete(0, tk.END)
    tkr_entry.insert(0, tkr_scale.get())
    tkg_entry.delete(0, tk.END)
    tkg_entry.insert(0, tkg_scale.get())
    tkb_entry.delete(0, tk.END)
    tkb_entry.insert(0, tkb_scale.get())
    tka_entry.delete(0, tk.END)
    tka_entry.insert(0, tka_scale.get())



frames = []

sceny = []

vybrana_scena = 0

pustene = False

img2 = None


barva = (0,0,0,255)

posledni = None

tksceny_canvas = tk.Canvas(tkroot)
tksceny_listbox = tk.Listbox(tksceny_canvas)
tksceny_listbox.pack()
tk.Button(tksceny_canvas,text='+',command=add_scene).pack()

tkmenu1_canvas = tk.Canvas(tkroot)
tk.Button(tkmenu1_canvas,text='nastavit kameru (a)',command=add_camera).pack()
tksave_button = tk.Button(tkmenu1_canvas,text='uložit (s)',command=save)
tksave_button.pack()

tkmenu2_canvas = tk.Canvas(tkroot)
tk.Button(tkmenu2_canvas,text='nastavit tuto scénu (q)',command=set_scene).pack()
tk.Button(tkmenu2_canvas,text='spustit/zastavit (mezerník)',command=pause).pack()
tk.Button(tkmenu2_canvas,text='uložit jeden snímek 0.06s (e)',command=save_image).pack()
tk.Button(tkmenu2_canvas,text='uložit 17 snímků cca 1s (r)',command=save_images17).pack()
tk.Button(tkmenu2_canvas,text='uložit více snímků (d)',command=save_images).pack()
tk.Button(tkmenu2_canvas,text='vymazat poslední snímek (z)',command=del_frame).pack()
tk.Button(tkmenu2_canvas,text='vymazat posledních 17 snímků (x)',command=del_frames17).pack()
tk.Button(tkmenu2_canvas,text='smazat kreslení (f)',command=clear_draw).pack()
tkdelka_label = tk.Label(tkmenu2_canvas,text='délka: 0')
tkdelka_label.pack()

tkdelka_label.config(text=f'délka: {len(frames)} snímků = {round((len(frames)*0.06),2)} sekund')
tkroot.update_idletasks()

tkscena1_canvas = tk.Canvas(tkroot,bg='white',width=640,height=480)

tkscena2_canvas = tk.Canvas(tkroot,bg='white',width=640,height=480)

tkkresleni_canvas = tk.Canvas(tkroot,width=640,height=480)
tkr_label = tk.Label(tkkresleni_canvas,text='Červená:').grid(row=0,column=1)
tkr_label = tk.Label(tkkresleni_canvas,text='Zelená:').grid(row=1,column=1)
tkr_label = tk.Label(tkkresleni_canvas,text='Modrá:').grid(row=2,column=1)
tkr_label = tk.Label(tkkresleni_canvas,text='Alfa:').grid(row=3,column=1)
tkr_entry = tk.Entry(tkkresleni_canvas,width=5)
tkg_entry = tk.Entry(tkkresleni_canvas,width=5)
tkb_entry = tk.Entry(tkkresleni_canvas,width=5)
tka_entry = tk.Entry(tkkresleni_canvas,width=5)
tkr_scale = tk.Scale(tkkresleni_canvas,from_=0,to=255,orient=tk.HORIZONTAL,command=set_color)
tkg_scale = tk.Scale(tkkresleni_canvas,from_=0,to=255,orient=tk.HORIZONTAL,command=set_color)
tkb_scale = tk.Scale(tkkresleni_canvas,from_=0,to=255,orient=tk.HORIZONTAL,command=set_color)
tka_scale = tk.Scale(tkkresleni_canvas,from_=0,to=255,orient=tk.HORIZONTAL,command=set_color)
tka_scale.set(255)
tkr_scale.grid(row=0,column=3)
tkg_scale.grid(row=1,column=3)
tkb_scale.grid(row=2,column=3)
tka_scale.grid(row=3,column=3)
tkr_entry.grid(row=0,column=2)
tkg_entry.grid(row=1,column=2)
tkb_entry.grid(row=2,column=2)
tka_entry.grid(row=3,column=2)
tktloustka_scale = tk.Scale(tkkresleni_canvas,from_=1,to=100)
tktloustka_scale.grid(row=0,column=0,rowspan=5)

tksceny_listbox.insert(tk.END,'scena1')
tksceny_listbox.selection_set(0)
sceny.append({'jmeno':'scena1','kamera':None,'kresleni':Image.new('RGBA', (640,480), (255,255,255,0))})

tkroot.bind('<space>',pause)
tkroot.bind('<a>',add_camera)
tkroot.bind('<s>',save)
tkroot.bind('<q>',set_scene)
tkroot.bind('<e>',save_image)
tkroot.bind('<d>',save_images)
tkroot.bind('<r>',save_images17)
tkroot.bind('<z>',del_frame)
tkroot.bind('<x>',del_frames17)
tkroot.bind('<f>',clear_draw)
tkscena1_canvas.bind('<B1-Motion>',draw)
tkscena1_canvas.bind('<ButtonRelease-1>',end_draw)

tksceny_canvas.grid(row=1,column=0)
tkmenu2_canvas.grid(row=0,column=1)
tkscena1_canvas.grid(row=0,column=0)
tkscena2_canvas.grid(row=0,column=2)
tkmenu1_canvas.grid(row=1,column=1)
tkkresleni_canvas.grid(row=1,column=2)



draw_sceny()
save_sceny()

def on_closing():
    for scena in sceny:
        if scena['kamera'] is not None:
            scena['kamera'].release()
    tkroot.destroy()

tkroot.protocol('WM_DELETE_WINDOW', on_closing)
tkroot.mainloop()

err_file.close()
