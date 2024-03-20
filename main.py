import os
import tkinter
import glob

if os.name == 'posix':
    try:
        os.chdir(os.path.expanduser('~')+'/.pydownload')
    except:
        os.system('mkdir ~/.pydownload')
        os.system('python3 -m venv ~/.pydownload/venv')
        os.system(f'source ~/.pydownload/venv/bin/activate; python3 -m pip install --upgrade pip')
        os.chdir(os.path.expanduser('~')+'/.pydownload')

    os.system('git clone -qb main https://github.com/Pythom1234/projects.git')
    with open('projects/includes') as s:
        includes = s.read().split('\n')
    os.system('rm -rf projects')


    def b2():
        global b4
        os.system(f'rm -rf {l1.get(l1.curselection()[0])}')
        os.system(f'git clone -qb {l1.get(l1.curselection()[0])} https://github.com/Pythom1234/projects.git')
        os.system('rm -rf projects/.git')
        os.system(f'mv ~/.pydownload/projects ~/.pydownload/{l1.get(l1.curselection()[0])}')
        with open(l1.get(l1.curselection()[0])+'/req') as s:
            req = s.read()
        os.system(f'source ~/.pydownload/venv/bin/activate; python3 -m pip install {req}')
        b4 = tkinter.Button(text='Spustit',command=b3)
        b4.grid(row=3,column=2)

    def b3():
        with open(l1.get(l1.curselection()[0])+'/run') as s:
            run = s.read()
        os.system(f"""konsole --hold -e 'bash -c "source ~/.pydownload/venv/bin/activate; python3 {os.path.expanduser('~')}/.pydownload/{run}"'""")

    def c1(c):
        global b4
        if os.path.expanduser('~') + '/.pydownload/' + l1.get(l1.curselection()[0]) in glob.glob(os.path.expanduser('~')+'/.pydownload/*'):
            #b4 = tkinter.Button(text='Spustit',command=b3)
            b4.grid(row=3,column=2)
        else:
            #b4.destroy()
            b4.widget.grid_forget()

    b4 = None

    root = tkinter.Tk()
    tkinter.Label(text='Nainstalovat: ').grid(row=2,column=0)
    l1 = tkinter.Listbox()
    for i in includes:
        if not i == '':
            l1.insert('end',i)
    b1 = tkinter.Button(text='Nainstalovat',command=b2)
    b1.grid(row=2,column=2)
    l1.grid(row=2,column=1)
    l1.bind('<ButtonRelease-1>', c1)
    root.mainloop()
