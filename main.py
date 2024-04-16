import tkinter
import glob
import os

if not os.name == 'posix':
    raise EnvironmentError('linux only')

def download(name):
    delete(name)
    with open('includes',mode='r') as s:
        dirs = s.read().split('\n')
    with open('includes',mode='a') as s:
        if not name in dirs:
            s.write('\n'+name)
    name = name.split('==')[0]
    os.system(f'git clone -qb {name} https://github.com/Pythom1234/projects.git')
    os.system('rm -rf projects/.git')
    os.system(f'mv ~/.pydownload/projects ~/.pydownload/{name}')
    with open(name+'/req') as s:
        req = s.read()
    os.system(f'source ~/.pydownload/venv/bin/activate; python3 -m pip install {req}')
    prepare()

def run(name):
    with open(name+'/run') as s:
        run = s.read()
    os.system(f"""konsole --hold -e 'bash -c "source ~/.pydownload/venv/bin/activate; python3 ~/.pydownload/{run}"'""")

def delete(name):
    with open('includes',mode='r') as s:
        dirs = s.read().replace(name,'')
    with open('includes',mode='w') as s:
        s.write(dirs)
    name = name.split('==')[0]
    os.system(f'rm -rf {name}')
    prepare()

def delete_all():
    os.chdir(os.path.expanduser('~'))
    os.system('rm -rf .pydownload')
    exit()

def install_all():
    for i in includes:
        if not i == '':
            download(i)

def get_func_for_download(name):
    return lambda: download(name)

def get_func_for_run(name):
    return lambda: run(name)

def get_func_for_delete(name):
    return lambda: delete(name)

def prepare():
    global tk_downloads, tk_labels, tk_runs, tk_deletes
    for i in tk_downloads:
        i.destroy()
    for i in tk_labels:
        i.destroy()
    for i in tk_runs:
        i.destroy()
    for i in tk_deletes:
        i.destroy()
    tk_downloads = []
    tk_labels = []
    tk_runs = []
    tk_deletes = []
    with open('includes') as s:
        dirs = s.read()
    for i in includes:
        if not i == '':
            tk_labels.append(tkinter.Label(text=i.split('==')[0]))
            tk_labels[-1].grid(row=includes.index(i),column=0)
            if not i.split('==')[0] in dirs:
                tk_downloads.append(tkinter.Button(text='Stáhnout',command=get_func_for_download(i)))
                tk_downloads[-1].grid(row=includes.index(i),column=1)
            elif not i in dirs:
                tk_downloads.append(tkinter.Button(text='Aktualizovat',command=get_func_for_download(i)))
                tk_downloads[-1].grid(row=includes.index(i),column=1)
            else:
                tk_downloads.append(tkinter.Button(text='Aktuální',state='disabled'))
                tk_downloads[-1].grid(row=includes.index(i),column=1)
                tk_runs.append(tkinter.Button(text='Spustit',command=get_func_for_run(i.split('==')[0])))
                tk_runs[-1].grid(row=includes.index(i),column=2)
                tk_deletes.append(tkinter.Button(text='Smazat',command=get_func_for_delete(i)))
                tk_deletes[-1].grid(row=includes.index(i),column=3)

try:
    os.chdir(os.path.expanduser('~')+'/.pydownload')
except:
    os.system('mkdir ~/.pydownload')
    os.system('python3 -m venv ~/.pydownload/venv')
    os.system(f'source ~/.pydownload/venv/bin/activate; python3 -m pip install --upgrade pip')
    os.chdir(os.path.expanduser('~')+'/.pydownload')


os.chdir(os.path.expanduser('~')+'/.pydownload')

os.system('git clone -qb main https://github.com/Pythom1234/projects.git')
with open('projects/includes') as s:
    includes = s.read().split('\n')
os.system('rm -rf projects')

if not 'includes' in glob.glob('*'):
    with open('includes',mode='w'):
        pass

tk_labels = []
tk_downloads = []
tk_runs = []
tk_deletes = []

root = tkinter.Tk()
root.title('Stáhnout projekty')

menu_bar = tkinter.Menu(root)
menu = tkinter.Menu(menu_bar, tearoff=0)
menu.add_command(label='Vyčistit paměť (automaticky ukončí)',command=delete_all)
menu.add_command(label='Nainstalovat vše (pomalé)',command=install_all)
menu_bar.add_cascade(label='Možnosti', menu=menu)

root.config(menu=menu_bar)

prepare()

root.mainloop()
