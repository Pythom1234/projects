#!/usr/bin/python3
from ursina import *
from ursina.prefabs.first_person_controller import *

file = '/'.join(os.path.abspath(__file__).split('/')[:-1])+'/'
objs = []
max_id = 0


class Player(FirstPersonController):
    def __init__(self):
        super().__init__()
        # destroy(self.cursor)
        self.cursor.color = (1,1,1,1)
        self.cursor.scale = 0.001
        self.p = 0
        self.vikings = [] ## position
        self.traverse_target=scene
        self.y = 1
        self.gravity = 3
        self.jump_height = 0
        self.mouse_sensitivity=(200,200)
    def update(self):
        up =  False
        ladders = []
        ladders_distances = []
        for i in objs:
            if i.type == 'b':
                ladders.append(i)
                ladders_distances.append(distance(self,i))
        ladder = ladders[ladders_distances.index(min(ladders_distances))]
        if held_keys['space'] and distance(self,ladder) < 1.9:
            self.y += .1
            self.gravity = 0
            self.air_time = 0
        else:
            self.gravity = 3
        super().update()

class E(Entity):
    def __init__(self,**kwargs):
        global max_id
        self.type = kwargs['type']
        self.data = kwargs['data']
        if kwargs['type'] == 'a':
            super().__init__(model=f'assets/models/wall.obj',texture=f'assets/textures/wall.png',collider='mesh',**kwargs)
        if kwargs['type'] == 'b':
            super().__init__(model=f'assets/models/ladder.obj',texture=f'assets/textures/ladder.png',collider=None,**kwargs)
            if kwargs['data']:
                self.rotation_y = 90 * int(kwargs['data'])
                if int(kwargs['data']) == 0:
                    self.x += 1
                if int(kwargs['data']) == 2:
                    self.x -= 1
                if int(kwargs['data']) == 1:
                    self.z -= 1
                if int(kwargs['data']) == 3:
                    self.z += 1
            else:
                self.x += 1
            self.y -= 1
        if kwargs['type'] == 'd':
            super().__init__(model=f'assets/models/small.obj',texture=f'assets/textures/button.png',collider='mesh',**kwargs)
        if kwargs['type'] == 'g':
            super().__init__(model=f'assets/models/small.obj',texture=f'assets/textures/help.png',collider='mesh',**kwargs)
            self.data = self.data.replace('_',' ')
            self.tooltip = Tooltip(text=self.data,background_color=(0,0,0,1))
            self.tooltip.enabled = False
        self.id = max_id
        max_id += 1
        self.name = str(self.id)
    def update(self):
        if self.type == 'g':
            if str(mouse.hovered_entity) == str(self.id):
                self.tooltip.enabled = True
                self.alpha = 0.5
            else:
                self.tooltip.enabled = False
                self.alpha = 1

def load_map(n):
    with open(file+f'assets/maps/{n}') as f:
        lines = f.read()
    for line in lines.split('\n'):
        if not '#' in line:
            data = line.split(' ')
            if len(data) == 4:
                objs.append(E(type=data[0],data=None,position=(int(data[1])*2,int(data[2])*2,int(data[3])*2)))
            if len(data) == 5:
                objs.append(E(type=data[0],data=data[4],position=(int(data[1])*2,int(data[2])*2,int(data[3])*2)))


app = Ursina(development_mode=False,borderless=False)

text = Text()
load_map('001')

Player()


app.run()
