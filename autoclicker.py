import pyautogui
import time
import tkinter as tk
pyautogui.FAILSAFE = False

def stop():
    if pyautogui.position().x == 0 and pyautogui.position().y == 0:
        root.destroy()
        exit()

def start(co):
    root.iconify()
    prikazy = co.split('-')
    for prikaz in prikazy:
        if prikaz.split('=')[0] == 'mleft':
            pyautogui.PAUSE = float(prikaz.split('=')[1].split(',')[1])+0.01
            for i in range(int(prikaz.split('=')[1].split(',')[0])):
                pyautogui.click(x=pyautogui.position()[0], y=pyautogui.position()[1], button='left')
                stop()
                root.title(str(i))
        if prikaz.split('=')[0] == 'mright':
            pyautogui.PAUSE = float(prikaz.split('=')[1].split(',')[1])+0.01
            for i in range(int(prikaz.split('=')[1].split(',')[0])):
                pyautogui.click(x=pyautogui.position()[0], y=pyautogui.position()[1], button='right')
                stop()
                root.title(str(i))
        if prikaz.split('=')[0] == 'mmiddle':
            pyautogui.PAUSE = float(prikaz.split('=')[1].split(',')[1])+0.01
            for i in range(int(prikaz.split('=')[1].split(',')[0])):
                pyautogui.click(x=pyautogui.position()[0], y=pyautogui.position()[1], button='middle')
                stop()
                root.title(str(i))
        else:
            pyautogui.PAUSE = float(prikaz.split('=')[1].split(',')[1])+0.01
            for i in range(int(prikaz.split('=')[1].split(',')[0])):
                for name in prikaz.split('=')[0].split(','):
                    pyautogui.press(name)
                    stop()
                    root.title(str(i))
    root.destroy()

def spustit(b):
    start(a.get())

root = tk.Tk()
root.title('autoclick')
tk.Label(root,text='''
Zadej hodnotu:
a,space=10,0-mleft=100,1:
nejdřív "a" potom "space", opakovat "10" krát, čekat "0", potom "mouse_left", "100" krát, čekat "1"
''').pack()
a = tk.Entry(root,width=100)
a.pack()
tk.Button(root,text='OK',command=lambda: start(a.get())).pack()
a.bind('<Return>', spustit)
root.mainloop()
