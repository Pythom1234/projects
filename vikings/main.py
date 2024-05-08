#!/usr/bin/python3
from ursina import *
import random
from PIL import Image

class Viking(Entity):
    def __init__(self,**kwargs):
        super().__init__(model='assets/models/viking.obj',y=1,color=(1,1,1,1),**kwargs)
        #self.collider = BoxCollider(self,(0,1,0),(1,2,1))
        self.feet = Entity(parent=self,visible=False,model='cube',y=.05,scale=(.5,.1,.5))
        self.head = Entity(parent=self,visible=False,model='cube',y=1.95,scale=(.5,.1,.5))
        self.air_time = 0
        self._active = False
        self.pivot = Entity(parent=self,y=1.8)
        self.speed = 5
        self.lives = 3
        self.suspended_gravity = 0
        self.live = True
        self.grounded = False
        self.ladder = 1000
        self.normal_gravity = True
        self.in_exit = False
        self.inventory = {'1':None,'2':None,'3':None,'4':None}
        self.inventory_selected = '1'
        self.jumping = 0
    def reduce_lives(self,lives):
        self.lives -= lives
        if self._active:
            red_screen.blink(5)
        if self.lives <= 0:
            self.lives = -1
            self.position = (9999,9999,9999)
    def pick_up_item(self,item):
        if self.inventory['1'] == None:
            self.inventory['1'] = item
            return '1'
        elif self.inventory['2'] == None:
            self.inventory['2'] = item
            return '2'
        elif self.inventory['3'] == None:
            self.inventory['3'] = item
            return '3'
        elif self.inventory['4'] == None:
            self.inventory['4'] = item
            return '4'
        else:
            return False
    def set_inventory_selected(self):
        if self.inventory['1'] != None:
            self.inventory_selected = '1'
        elif self.inventory['2'] != None:
            self.inventory_selected = '2'
        elif self.inventory['3'] != None:
            self.inventory_selected = '3'
        elif self.inventory['4'] != None:
            self.inventory_selected = '4'
        else:
            self.inventory_selected = '1'
    def set_collider(self,collider):
        if collider:
            self.collider = BoxCollider(self,(0,1,0),(1,2,1))
        else:
            self.collider = None
    def update(self):
        if self.lives > 0:
            if self.animations and raycast(self.head.world_position,direction=self.up,ignore=[shield,self,exit_entity] + objs_not_collides + acids + [player.erik,player.olaf,player.baleog],distance=1).hit:
                try:
                    for i in self.animations:
                        i.kill()
                except:
                    pass
            if shield.is_up:
                ignore = [self.feet,self,exit_entity] + objs_not_collides + acids + [player.erik,player.olaf,player.baleog] + enemies
            else:
                ignore = [self.feet,self,shield,exit_entity] + objs_not_collides + acids + [player.erik,player.olaf,player.baleog] + enemies
            hit_info_feet = raycast(self.feet.world_position + (0,.1,0),direction=self.down,distance=.3,ignore=ignore)
            if self.suspended_gravity == 0:
                if not hit_info_feet.hit:
                    if self.normal_gravity:
                        self.y -= min((self.air_time / 1000) * 100 * time.dt, raycast(self.feet.world_position,direction=self.down,ignore=ignore).distance - 0.1)
                        self.air_time += (.25 * time.dt) * 1000
                        self.grounded = False
                    else:
                        self.y -= .08
                        self.air_time = 0
                else:
                    if self.air_time > 270 and not hit_info_feet.entity.type == 'k':
                        self.reduce_lives(1)
                    self.air_time = 0
                    self.grounded = True
            try:
                if hit_info_feet.entity.type == 'h':
                    hit_info_feet.entity.h_stand()
            except:
                pass
            try:
                if hit_info_feet.entity.type == 'k' and self.jumping < 0:
                    if self.type == 'ERIK' and held_keys['SPACE']:
                        self.animate_y(value=self.y+9.5,duration=.6,resolution=int(1//time.dt),curve=curve.out_circ)
                        hit_info_feet.entity.k_stand()
                        self.jumping = 10
                    else:
                        self.animate_y(value=self.y+6,duration=.6,resolution=int(1//time.dt),curve=curve.out_circ)
                        hit_info_feet.entity.k_stand()
                        self.jumping = 10
            except:
                pass
            self.jumping -= 1
            try:
                ladders_distances = []
                for i in objs_not_collides:
                    if i.type == 'b':
                        ladders_distances.append(distance(self,i))
                if ladders_distances:
                    self.ladder = min(ladders_distances)
                else:
                    self.ladder = 9999
            except:
                self.ladder = 9999
            self.set_collider(True)
            hit_info = self.intersects()
            self.in_exit = False
            for i in hit_info.entities:
                if i == exit_entity:
                    self.in_exit = True
                if i.type == 'c':
                    self.reduce_lives(10)
                if i.type == 'f':
                    if self.pick_up_item(i.item):
                        i.f_pick_up()
                if i.type == 'j':
                    if 'k' + i.type_color == self.inventory[self.inventory_selected] and held_keys['E']:
                        i.j_open()
                        self.inventory[self.inventory_selected] = None
                        self.set_inventory_selected()
                if i.type == 'LASER':
                    self.reduce_lives(1)
                    i.delete()
            self.set_collider(False)
            if self._active:
                if held_keys['SPACE'] and self.ladder < 1.8:
                    self.y += .1
                    self.air_time = 0
                    self.suspended_gravity = 20
                elif held_keys['SPACE'] and self.ladder < 2:
                    self.suspended_gravity = 20
                if self.suspended_gravity != 0:
                    self.suspended_gravity -= 1
                    self.air_time = 0
                self.y += self.suspended_gravity / 500
                self.pivot.rotation_x -= mouse.velocity[1] * 150
                self.pivot.rotation_x = clamp(self.pivot.rotation_x, -90, 90)
                self.rotation_y += mouse.velocity[0] * 150
                direction = Vec3(
                    (self.forward * (held_keys['W'] - held_keys['S']))
                    + (self.right * (held_keys['D'] - held_keys['A']))
                    ).normalized()
                ignore = [shield,exit_entity] + objs_not_collides + acids + [player.erik,player.olaf,player.baleog] + enemies
                feet_ray = raycast(self.position+(0,0.1,0), direction, distance=.6, ignore=ignore)
                mid_ray = raycast(self.position+(0,0.9,0), direction, distance=.6, ignore=ignore)
                head_ray = raycast(self.position+(0,1.8,0), direction, distance=.6, ignore=ignore)
                if not feet_ray.hit and not mid_ray.hit and not head_ray.hit:
                    move_amount = direction * time.dt * self.speed
                    if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.6, ignore=ignore).hit:
                        move_amount[0] = min(move_amount[0], 0)
                    if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.6, ignore=ignore).hit:
                        move_amount[0] = max(move_amount[0], 0)
                    if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.6, ignore=ignore).hit:
                        move_amount[2] = min(move_amount[2], 0)
                    if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.6, ignore=ignore).hit:
                        move_amount[2] = max(move_amount[2], 0)
                    self.position += move_amount
    def input(self,key):
        if key == 'E' and self.active:
            item = self.inventory[self.inventory_selected]
            used = False
            if item == 'a':
                if self.lives != 4:
                    self.lives = 4
                    used = True
                else:
                    used = False
            if item == 'f':
                if self.lives < 3:
                    self.lives += 1
                    used = True
                else:
                    used = False
            if item == 'fa':
                if self.type == 'BALEOG':
                    self.fire_arrow = True
                    used = True
                else:
                    used = False
            if used:
                self.inventory[self.inventory_selected] = None
                self.set_inventory_selected()
    @property
    def active(self):
        return self._active
    @active.setter
    def active(self,value):
        self._active = value
        if self._active:
            black_screen.blink(5)
            camera.parent = self.pivot
            camera.position = (0,0,0)

class Arrow(Entity):
    def __init__(self,rotation,position,fire,**kwargs):
        tmp = 'fire_' if fire else ''
        super().__init__(self,texture=f'assets/textures/{tmp}arrow.png',model='assets/models/arrow.obj',double_sided=True,**kwargs)
        self.position = position
        self.rotation = rotation
        if fire:
            self.scale = 2
        self.time_live = 0
        self.fire = fire
        self.collider = BoxCollider(self,(0,0,0),(.1,.1,1))
        self.type = 'ARROW'
        self.speed = .5
        self.time_not_moving = 0
        random_deviation = .001
        self.random = (random.uniform(-random_deviation,random_deviation),random.uniform(-random_deviation,random_deviation),random.uniform(-random_deviation,random_deviation))
    def update(self):
        self.time_live += 1
        if self.speed != 0:
            for i in range(10):
                self.position += (self.forward * self.speed + self.random) / 10
                ignore = [shield] + [player.erik,player.olaf,player.baleog]
                hit_info = self.intersects(ignore=ignore)
                if hit_info.entity and hit_info.entity.type == 'd':
                    hit_info.entity.d_press()
                if hit_info.entity and hit_info.entity.type == 'e':
                    if self.fire:
                        hit_info.entity.kill()
                    else:
                        hit_info.entity.hit()
                    destroy(self)
                    return
                if hit_info.hit:
                    self.speed = 0
                    self.random = (0,0,0)
                    self.collider = None
        else:
            self.time_not_moving += 1
            self.collider = BoxCollider(self,(0,0,0),(.1,.1,1))
            ignore = [shield] + acids + [player.erik,player.olaf,player.baleog]
            hit_info = self.intersects(ignore=ignore)
            if not hit_info.hit:
                destroy(self)
                return
            self.collider = None
        if self.speed != 0 and self.time_live == 300:
            destroy(self)
            return
        if self.speed == 0 and self.time_not_moving == 100:
            destroy(self)
            return

class Sword(Entity):
    def __init__(self,**kwargs):
        super().__init__(model='assets/models/sword.obj',texture='assets/textures/sword.png',rotation=(0,-90,0),**kwargs)
        self.collider = BoxCollider(self,(0,0,1),(1,.1,1))
        self.type = 'SWORD'
        self.animate_rotation_y(90,duration=.3,curve=curve.in_out_sine)
        destroy(self,delay=.3)
    def update(self):
        hit_info = self.intersects()
        if hit_info.hit and hit_info.entity.type == 'e':
            hit_info.entity.hit()
            self.collider = None

class Erik(Viking):
    def __init__(self):
        super().__init__()
        self.speed = 7
        self.texture = 'assets/textures/erik.png'
        self.type = 'ERIK'
    def update(self):
        if game_state == 1:
            super().update()
    def input(self,key):
        if game_state == 1:
            if key == 'SPACE' and self.active and not self.ladder < 1.8:
                if self.grounded:
                    self.animate_y(value=self.y+3.5,duration=.6,resolution=int(1//time.dt),curve=curve.out_circ)
            super().input(key)

class Olaf(Viking):
    def __init__(self):
        global shield
        super().__init__()
        self.texture = 'assets/textures/olaf.png'
        self.shield_up = False
        shield = Entity(type='SHIELD',is_up=False,parent=self,model='assets/models/shield.obj',texture='assets/textures/shield.png',color=(1,1,1,.5),position=(0,.9,.6))
        shield.collider = BoxCollider(shield,(0,0,0),(1.5,1.5,.3))
        self.type = 'OLAF'
    def update(self):
        if game_state == 1:
            if self.active:
                shield.color = (1,1,1,.5)
            else:
                shield.color = (1,1,1,1)
            if self.lives == 0:
                self.shield_up = False
                shield.visible = False
                shield.position = (9999,9999,9999)
            shield.is_up = self.shield_up
            if self.shield_up:
                shield.rotation_x = -90
                shield.position = (0,2.1,0)
                self.normal_gravity = False
            else:
                shield.rotation_x = 0
                shield.position = (0,.9,.5)
                self.normal_gravity = True
            super().update()
    def input(self,key):
        if game_state == 1:
            if key == 'SPACE' and self.active and not self.ladder < 1.8:
                self.shield_up = not self.shield_up
            super().input(key)

class Baleog(Viking):
    def __init__(self):
        super().__init__()
        self.texture = 'assets/textures/baleog.png'
        self.tensioning = False
        self.tension = 0
        self.chopping = 0
        self.fire_arrow = False
        self.bow = Entity(parent=self.pivot,texture='assets/textures/bow0.png',always_on_top=False,model='assets/models/bow.obj',color=(1,1,1,1),double_sided=True)
        self.type = 'BALEOG'
    def update(self):
        if game_state == 1:
            self.chopping -= 1
            if self.tensioning and self.active:
                self.tension += time.dt * 50
            if self.tensioning or self.chopping > 10:
                self.speed = 0
            else:
                self.speed = 5
            if not self.active:
                self.tensioning = False
                self.tension = 0
            self.bow.texture = f'assets/textures/bow{int(clamp(self.tension / 15,0,3))}.png'
            if self.active:
                self.bow.always_on_top = True
                self.bow.visible = True
            else:
                self.bow.always_on_top = False
                self.bow.visible = False
            super().update()
    def input(self,key):
        if game_state == 1:
            if key == 'ACTION1':
                self.tensioning = True
            if key == 'ACTION2':
                if self.tension > 50:
                    arrows.append(Arrow(camera.world_rotation,camera.world_position + camera.forward,self.fire_arrow))
                self.tensioning = False
                self.tension = 0
            if self.active:
                if key == 'SPACE' and not self.tensioning and self.chopping < 0:
                    Sword(parent=self,position=(0,.5,0))
                    self.chopping = 25
            super().input(key)

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.erik = Erik()
        self.olaf = Olaf()
        self.baleog = Baleog()
        self.active = 0
        self.set_active(self.active)
        mouse.locked = True
        camera.fov = 90
        self.cursor = Sprite('assets/textures/cursor.png',parent=camera.ui,ppu=600)
    def update(self):
        if game_state == 1:
            if self.erik.lives == -1:
                self.erik.live = False
                self.erik.lives = 0
                self.erik.model = None
                self.erik.inventory = {'1':None,'2':None,'3':None,'4':None}
                if self.erik.active:
                    self.next_viking()
            if self.olaf.lives == -1:
                self.olaf.live = False
                self.olaf.lives = 0
                self.olaf.model = None
                self.olaf.inventory = {'1':None,'2':None,'3':None,'4':None}
                if self.olaf.active:
                    self.next_viking()
            if self.baleog.lives == -1:
                self.baleog.live = False
                self.baleog.lives = 0
                self.baleog.model = None
                self.baleog.inventory = {'1':None,'2':None,'3':None,'4':None}
                if self.baleog.active:
                    self.next_viking()
            t = dedent(f'''\
            Erik: <red>x {round(self.erik.x,3)}<default>, <cyan>y {round(self.erik.y,3)}<default>, <green>z {round(self.erik.z,3)}<default>, <yellow>lives {self.erik.lives}<default>, <magenta>air time {round(self.erik.air_time)}<default>{', <blue>on the floor' if self.erik.grounded else ''}<default>
            Olaf: <red>x {round(self.olaf.x,3)}<default>, <cyan>y {round(self.olaf.y,3)}<default>, <green>z {round(self.olaf.z,3)}<default>, <yellow>lives {self.olaf.lives}<default>, <magenta>air time {round(self.olaf.air_time)}<default>{', <blue>on the floor' if self.olaf.grounded else ''}<default>
            Baleog: <red>x {round(self.baleog.x,3)}<default>, <cyan>y {round(self.baleog.y,3)}<default>, <green>z {round(self.baleog.z,3)}<default>, <yellow>lives {self.baleog.lives}<default>, <magenta>air time {round(self.baleog.air_time)}<default>{', <blue>on the floor' if self.baleog.grounded else ''}<default>
            objects: <gray>{len(objs)+len(objs_not_collides)+len(acids)}<default>
            ''')
            if self.erik.live == False:
                t = t.replace('Erik','<dark_gray>Erik<default>')
            if self.olaf.live == False:
                t = t.replace('Olaf','<dark_gray>Olaf<default>')
            if self.baleog.live == False:
                t = t.replace('Baleog','<dark_gray>Baleog<default>')
            if debug_text.visible:
                debug_text.text = t
                debug_text.create_background()
            if self.erik.in_exit and self.olaf.in_exit and self.baleog.in_exit:
                win()
    def set_active(self,viking):
        self.erik.active = False
        self.olaf.active = False
        self.baleog.active = False
        if viking == 0:
            self.erik.active = True
        if viking == 1:
            self.olaf.active = True
        if viking == 2:
            self.baleog.active = True
    def next_viking(self):
        self.active += 1
        if self.active == 3:
            self.active = 0
        rep = 0
        while True:
            if self.active == 0 and self.erik.live == False:
                self.active += 1
            elif self.active == 1 and self.olaf.live == False:
                self.active += 1
            elif self.active == 2 and self.baleog.live == False:
                self.active += 1
            else:
                break
            if self.active == 3:
                self.active = 0
            rep += 1
            if rep == 6:
                game_over()
                break
        self.set_active(self.active)
    def input(self,key):
        global inventory_timer
        if game_state == 1:
            if key == 'NEXT':
                self.next_viking()
            if key == 'DEBUG':
                debug_text.visible = not debug_text.visible
            if key == 'CMD':
                application.pause()
                Cmd()
            if key == 'INVENTORY' and inventory_timer < 1:
                inventory_timer = 10
                application.pause()
                vikings_images.inventory_enable()
            if key == 'ESC':
                game_over()
    def for_all(self,command):
        exec(f'self.erik.{command}')
        exec(f'self.olaf.{command}')
        exec(f'self.baleog.{command}')
    def restart(self):
        shield.visible = True
        shield.is_up = False
        self.olaf.shield_up = False
        self.baleog.fire_arrow = False
        self.for_all('rotation = (0,0,0)')
        self.for_all('pivot.rotation = (0,0,0)')
        self.for_all('visible = True')
        self.for_all('lives = 3')
        self.for_all('live = True')
        self.for_all('in_exit = False')
        self.for_all('air_time = 0')
        self.for_all("inventory_selected = '1'")
        self.for_all("model='assets/models/viking.obj'")
        self.for_all("inventory = {'1':None,'2':None,'3':None,'4':None}")
        self.active = 0
        self.set_active(self.active)

class E(Entity):
    def __init__(self,**kwargs):
        global max_id, exit_entity
        self.timer = 0
        self.type = kwargs['type']
        self.data = kwargs['data']
        self.signal = ''
        if self.type == 'a':
            self.signal = self.data
            if self.signal:
                super().__init__(model=f'assets/models/wall.obj',texture=f'assets/textures/door.png',collider=None,**kwargs)
            else:
                a = random.randrange(0,100)
                if a in range(0,42):
                    texture_number = '0'
                elif a in range(42,84):
                    texture_number = '1'
                elif a in range(84,92):
                    texture_number = '2'
                elif a in range(92,95):
                    texture_number = '3'
                elif a in range(95,97):
                    texture_number = '4'
                else:
                    texture_number = '5'
                super().__init__(model=f'assets/models/wall.obj',texture=f'assets/textures/wall{texture_number}.png',collider=None,**kwargs)
            self.collider = BoxCollider(self,(0,0,0),(2,2,2))
        if self.type == 'b':
            super().__init__(model=f'assets/models/ladder.obj',texture=f'assets/textures/ladder.png',collider=None,**kwargs)
            if kwargs['data']:
                self.rotation_y = 90 * float(kwargs['data'])
                if float(kwargs['data']) == 0:
                    self.x += 1
                if float(kwargs['data']) == 2:
                    self.x -= 1
                if float(kwargs['data']) == 1:
                    self.z -= 1
                if float(kwargs['data']) == 3:
                    self.z += 1
            else:
                self.x += 1
            self.y -= 1
        if self.type == 'c':
            super().__init__(model=f'assets/models/acid.obj',texture=f'assets/textures/acid0.png',collider=None,**kwargs)
            self.collider = BoxCollider(self,(0,0,0),(1.7,1.7,1.7))
            self.t = 0
            self.signal = self.data
        if self.type == 'd':
            super().__init__(model=f'assets/models/small.obj',texture=f'assets/textures/button.png',collider=None,**kwargs)
            self.signal = self.data
            self.collider = BoxCollider(self,(0,0,0),(.5,.5,.5))
        if self.type == 'f':
            super().__init__(model=f'assets/models/small.obj',texture=f'assets/textures/items/{self.data}.png',collider=None,**kwargs)
            self.collider = BoxCollider(self,(0,0,0),(.5,.5,.5))
            self.item = self.data
        if self.type == 'g':
            super().__init__(model=f'assets/models/small.obj',texture=f'assets/textures/help.png',collider=None,**kwargs)
            self.data = self.data.replace('_',' ')
            self.tooltip = Tooltip(text=self.data,background_color=(0,0,0,1))
            self.tooltip.enabled = False
            self.collider = BoxCollider(self,(0,0,0),(.5,.5,.5))
        if self.type == 'h':
            super().__init__(model=f'assets/models/wall.obj',texture=f'assets/textures/falling.png',collider=None,**kwargs)
            self.collider = BoxCollider(self,(0,0,0),(2,2,2))
            self.fall_after = -1
        if self.type == 'i':
            exit_entity = Entity(model=f'assets/models/exit.obj',texture=f'assets/textures/exit.png',collider='mesh',**kwargs)
        if self.type == 'j':
            self.type_color = self.data.split(',')[0]
            self.signal = self.data.split(',')[1]
            super().__init__(model=f'assets/models/small.obj',texture=f'assets/textures/keyhole{self.type_color}.png',collider=None,**kwargs)
            self.collider = BoxCollider(self,(0,0,0),(.5,.5,.5))
        if self.type == 'k':
            super().__init__(model=f'assets/models/slime0.obj',texture=f'assets/textures/slime.png',collider=None,**kwargs)
            self.collider = BoxCollider(self,(0,0,0),(2,2,2))
            self.change_to_normal = 0
        try:
            self.id = max_id
            max_id += 1
            self.name = str(self.id)
    def update(self):
        if game_state == 1:
            if self.type == 'c':
                if self.timer < 0:
                    self.t += 1
                    if self.t == 3:
                        self.t = 0
                    self.texture = f'assets/textures/acid{self.t}.png'
                    self.timer = 5
            if self.type == 'd':
                if self.timer < 0:
                    self.color = color.rgb(255,255,255)
                if self in mouse_entities and distance(self,camera) < 2.2:
                    self.alpha = 0.5
                else:
                    self.alpha = 1
            if self.type == 'g':
                if self in mouse_entities:
                    self.tooltip.enabled = True
                    self.alpha = 0.5
                else:
                    self.tooltip.enabled = False
                    self.alpha = 1
            if self.type == 'h':
                self.fall_after -= 1
                if self.fall_after == 0:
                    destroy(self)
                    return
            if self.type == 'k':
                self.change_to_normal -= 1
                if self.change_to_normal == 0:
                    self.model = 'assets/models/slime0.obj'
            self.timer -= 1
    def input(self,key):
        if game_state == 1:
            if self.type == 'd':
                if self in mouse_entities and distance(self,camera) < 2.2 and key == 'PRESS':
                    self.d_press()
    def d_press(self):
        self.color = (.2,.1,.1,1)
        self.timer = 10
        signal_send(self.signal.replace('_',''))
    def f_pick_up(self):
        destroy(self)
    def h_stand(self):
        if self.fall_after < 0:
            self.fall_after = 40
    def j_open(self):
        signal_send(self.signal)
    def k_stand(self):
        self.model = 'assets/models/slime1.obj'
        self.change_to_normal = 10
    def check_signal(self,signal):
        if self.signal == signal:
            destroy(self)

class Laser(Entity):
    def __init__(self,**kwargs):
        super().__init__(model='assets/models/laser.obj',texture='assets/textures/laser.png',**kwargs)
        self.collider = BoxCollider(self,(0,0,0),(.1,.1,.5))
        self.type = 'LASER'
    def update(self):
        hit_info = raycast(self.position,self.forward,traverse_target=scene,ignore=[self,player.erik,player.olaf,player.baleog] + enemies + lasers + objs_not_collides,distance=1.5)
        if hit_info.hit:
            self.delete()
            return
        self.position += self.forward / 5
    def delete(self):
        global lasers
        destroy(self)
        del lasers[lasers.index(self)]

class Enemy(Entity):
    def __init__(self,**kwargs):
        self.enemy_type = kwargs['data'][0]
        self.type = 'e'
        super().__init__(model='assets/models/enemy.obj',**kwargs)
        if len(kwargs['data']) == 2:
            self.rotation = int(kwargs['data'][1]) * 90
        self.collider = BoxCollider(self,(0,.5,0))
        self.y -= 1
        rules = { # (m(l|r|b)|M)?(s|Sn?)?(f|F)?[0-9]
            'a':'mlS1',
            'b':'s0',
            'c':'MSf3',
            'd':'mrSF0',
            'e':'mlSnf4'}
        self.rule = rules[self.enemy_type]
        self.lives = int(self.rule[-1])
        if self.lives == 0:
            self.lives = 1000000
        self.hit_info = raycast(self.position + (0,.5,0),self.forward,distance=0,ignore=[self])
        self.shoot_timer = 0
        self.in_air = False
        self.texture_normal = f'assets/textures/enemies/{self.enemy_type}.png'
        self.texture_angry = f'assets/textures/enemies/{self.enemy_type}_a.png'
        self.texture = self.texture_normal
        self.will_shoot = False
        self.will_shoot_after = 0
    def move(self,to_player):
        if not self.in_air:
            if to_player:
                distances = [distance(self,player.erik),distance(self,player.olaf),distance(self,player.baleog)]
                min_distance = distances.index(min(distances))
                if min_distance == 0:
                    self.look_at_xz(player.erik)
                if min_distance == 1:
                    self.look_at_xz(player.olaf)
                if min_distance == 2:
                    self.look_at_xz(player.baleog)
                if self.hit_info.distance > 1:
                    self.position += self.forward / (5 if 'F' in self.rule else (17 if 'f' in self.rule else 30))
            else:
                if self.hit_info.distance > 1:
                    self.position += self.forward / (5 if 'F' in self.rule else (17 if 'f' in self.rule else 30))
                else:
                    if not (self.hit_info.entity == shield or
                            self.hit_info.entity == player.erik or
                            self.hit_info.entity == player.olaf or
                            self.hit_info.entity == player.baleog):
                        if 'l' in self.rule:
                            self.rotation_y -= 90
                        elif 'r' in self.rule:
                            self.rotation_y += 90
                        elif 'b' in self.rule:
                            self.rotation_y += 180
    def hit(self):
        global enemies
        self.lives -= 1
        if self.lives == 0:
            destroy(self)
            del enemies[enemies.index(self)]
    def kill(self):
        global enemies
        self.lives = 0
        destroy(self)
        del enemies[enemies.index(self)]
    def shoot(self,if_player):
        if self.will_shoot and self.will_shoot_after < 0:
            if if_player:
                self.make_shot()
            else:
                self.make_shot_all_directions()
            self.texture = self.texture_normal
            self.will_shoot = False
        if if_player:
            if 'n' in self.rule:
                if self.shoot_timer < 0 and self.hit_info.distance < 5 and (shield in self.hit_info.entities or player.erik in self.hit_info.entities or player.olaf in self.hit_info.entities or player.baleog in self.hit_info.entities):
                    self.texture = self.texture_angry
                    self.shoot_timer = 30
                    self.will_shoot = True
                    self.will_shoot_after = 10
            else:
                if self.shoot_timer < 0 and self.hit_info.distance < 20 and (shield in self.hit_info.entities or player.erik in self.hit_info.entities or player.olaf in self.hit_info.entities or player.baleog in self.hit_info.entities):
                    self.texture = self.texture_angry
                    self.shoot_timer = 100
                    self.will_shoot = True
                    self.will_shoot_after = 20
        else:
            if self.shoot_timer < 0:
                self.texture = self.texture_angry
                self.shoot_timer = 100
                self.will_shoot = True
                self.will_shoot_after = 20
    def make_shot(self):
        lasers.append(Laser(position=self.position + (0,.5,0),rotation=self.rotation))
    def make_shot_all_directions(self):
        lasers.append(Laser(position=self.position + (0,.5,0),rotation=self.rotation + (0,0,0)))
        lasers.append(Laser(position=self.position + (0,.5,0),rotation=self.rotation + (0,90,0)))
        lasers.append(Laser(position=self.position + (0,.5,0),rotation=self.rotation + (0,180,0)))
        lasers.append(Laser(position=self.position + (0,.5,0),rotation=self.rotation + (0,270,0)))
    def update_internal(self):
        if game_state == 1:
            self.will_shoot_after -= 1
            self.shoot_timer -= 1
            self.hit_info = raycast(self.position + (0,.5,0),self.forward,ignore=[self] + lasers)
            if not raycast(self.position,self.down,distance=.15,ignore=[self]).hit:
                self.in_air = True
                self.y -= .1
            else:
                self.in_air = False
            if 'm' in self.rule:
                self.move(False)
            if 'M' in self.rule:
                self.move(True)
            if 's' in self.rule:
                self.shoot(False)
            if 'S' in self.rule:
                self.shoot(True)

class BlackScreen(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui,model='quad',scale=(10000,10000),color=(0,0,0,0),eternal=True)
        self.blink_timer = 0
    def blink(self,duration=10):
        self.blink_timer = duration
    def update(self):
        if self.blink_timer:
            self.color = (0,0,0,1)
            self.blink_timer -= 1
        else:
            self.color = (0,0,0,0)

class RedScreen(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui,model='quad',scale=(10000,10000),color=(1,0,0,0),eternal=True)
        self.blink_timer = 0
    def blink(self,duration=10):
        self.blink_timer = duration
    def update(self):
        if self.blink_timer:
            self.color = (1,0,0,.5)
            self.blink_timer -= 1
        else:
            self.color = (1,0,0,0)

class FPSCounter(Entity):
    def __init__(self):
        super().__init__(eternal=True,ignore_paused=True)
        self.timer = 0
        self.fps = 0
        self.text = Text(parent=camera.ui,origin=(-.5,.5),position=window.top_left,scale=(.7,.7))
        self.text.z = -1000
    def update(self):
        self.current_fps = int(1/time.dt)
        if self.timer <= 0:
            self.fps = self.current_fps
            self.timer = 10
        self.timer -= 1
        self.text.text = self.fps

class Cmd(TextField):
    def __init__(self):
        super().__init__(y=-.4,x=-.45,max_lines=1,character_limit=66)
        self.bg.scale_x = 1
        self.cursor.color = (1,1,1,1)
    def input(self,key):
        if key == 'ENTER':
            application.resume()
            try:
                self.text = self.text.replace('erik','player.erik')
                self.text = self.text.replace('olaf','player.olaf')
                self.text = self.text.replace('baleog','player.baleog')
                self.text = self.text.replace('print','print_on_screen')
                self.text = self.text.replace('*kill','player.for_all("lives = -1")')
                self.text = self.text.replace('*heal','player.for_all("lives = 3")')
                self.text = self.text.replace('*heal+','player.for_all("lives = 4")')
                exec(self.text)
            except:
                pass
            destroy(self)
            return
        super().input(key)

class PasswdInput(Entity):
    def __init__(self):
        super().__init__()
        self.text = Text(text='',origin=(0,0))
        self.content = ['S','T','R','T']
        self.p = 0
    def update(self):
        content = self.content.copy()
        content[self.p] = '<red>' + content[self.p] + '<default>'
        self.text.text = ''.join(content)
    def input(self,key):
        global selected_map
        if key == 'ENTER':
            try:
                selected_map = ''.join(self.content)
                start()
                c = True
            except Exception as e:
                print(e)
                t = Text('invalid password',origin=(0,.5),y=-.01)
                t.fade_out(duration=1)
                destroy(t,1)
                c = False
                self.p = 0
            if c:
                destroy(self.text)
                destroy(self)
                return
        if key in 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 1 2 3 4 5 6 7 8 9 0':
            self.content[self.p] = key
            if self.p != 3:
                self.p += 1
        if key == 'backspace':
            if self.p != 0:
                self.p -= 1
        if key == 'left arrow':
            if self.p != 0:
                self.p -= 1
        if key == 'right arrow':
            if self.p != 3:
                self.p += 1

class VikingsImages(Sprite):
    def __init__(self):
        self.inventory_enabled = False
        self.selected_item = None
        self.selected_item_viking = None
        self.selected_hidden = False
        self.selected_item_hidden = False
        self.hidden_timer = 0
        self.selected_item_position = '1'
        image = Image.open(file+'assets/textures/vikings_images/table.png')
        super().__init__(Texture(image),ignore_paused=True,parent=camera.ui,model='quad',position=window.bottom_left,origin=(-.5,-.5),ppu=350)
    def update(self):
        global inventory_timer
        image = Image.open(file+'assets/textures/vikings_images/table.png')
        if not player.erik.live:
            erik_state = 'd'
        elif player.active == 0:
            erik_state = 's'
        else:
            erik_state = 'u'
        if not player.olaf.live:
            olaf_state = 'd'
        elif player.active == 1:
            olaf_state = 's'
        else:
            olaf_state = 'u'
        if not player.baleog.live:
            baleog_state = 'd'
        elif player.active == 2:
            baleog_state = 's'
        else:
            baleog_state = 'u'
        image.paste(Image.open(file+f'assets/textures/vikings_images/erik_{erik_state}.png'),(1,1))
        image.paste(Image.open(file+f'assets/textures/vikings_images/olaf_{olaf_state}.png'),(1,34))
        image.paste(Image.open(file+f'assets/textures/vikings_images/baleog_{baleog_state}.png'),(1,67))
        life_point_image = Image.open(file+f'assets/textures/vikings_images/life_point.png')
        life_point_extra_image = Image.open(file+f'assets/textures/vikings_images/life_point_extra.png')
        for i in range(player.erik.lives):
            image.paste(life_point_image,(2 + i * 6,27))
            if i == 3:
                image.paste(life_point_extra_image,(2 + i * 6,27))
        for i in range(player.olaf.lives):
            image.paste(life_point_image,(2 + i * 6,60))
            if i == 3:
                image.paste(life_point_extra_image,(2 + i * 6,60))
        for i in range(player.baleog.lives):
            image.paste(life_point_image,(2 + i * 6,93))
            if i == 3:
                image.paste(life_point_extra_image,(2 + i * 6,93))
        for number in '1234':
            item = player.erik.inventory[number]
            if item:
                if number == '1' and not (player.active == 0 and self.selected_item == '1' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(34,1))
                if number == '2' and not (player.active == 0 and self.selected_item == '2' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(50,1))
                if number == '3' and not (player.active == 0 and self.selected_item == '3' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(34,17))
                if number == '4' and not (player.active == 0 and self.selected_item == '4' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(50,17))
            if player.erik.inventory_selected == number:
                if not (player.active == 0 and self.inventory_enabled and self.selected_hidden and not self.selected_item):
                    selected_image = Image.open(file+f'assets/textures/vikings_images/selected.png')
                    if number == '1':
                        image.paste(selected_image,(34,1),mask=selected_image)
                    if number == '2':
                        image.paste(selected_image,(50,1),mask=selected_image)
                    if number == '3':
                        image.paste(selected_image,(34,17),mask=selected_image)
                    if number == '4':
                        image.paste(selected_image,(50,17),mask=selected_image)
        for number in '1234':
            item = player.olaf.inventory[number]
            if item:
                if number == '1' and not (player.active == 1 and self.selected_item == '1' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(34,34))
                if number == '2' and not (player.active == 1 and self.selected_item == '2' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(50,34))
                if number == '3' and not (player.active == 1 and self.selected_item == '3' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(34,50))
                if number == '4' and not (player.active == 1 and self.selected_item == '4' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(50,50))
            if player.olaf.inventory_selected == number:
                if not (player.active == 1 and self.inventory_enabled and self.selected_hidden and not self.selected_item):
                    selected_image = Image.open(file+f'assets/textures/vikings_images/selected.png')
                    if number == '1':
                        image.paste(selected_image,(34,34),mask=selected_image)
                    if number == '2':
                        image.paste(selected_image,(50,34),mask=selected_image)
                    if number == '3':
                        image.paste(selected_image,(34,50),mask=selected_image)
                    if number == '4':
                        image.paste(selected_image,(50,50),mask=selected_image)
        for number in '1234':
            item = player.baleog.inventory[number]
            if item:
                if number == '1' and not (player.active == 2 and self.selected_item == '1' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(34,67))
                if number == '2' and not (player.active == 2 and self.selected_item == '2' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(50,67))
                if number == '3' and not (player.active == 2 and self.selected_item == '3' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(34,83))
                if number == '4' and not (player.active == 2 and self.selected_item == '4' and self.selected_hidden):
                    image.paste(Image.open(file+f'assets/textures/vikings_images/items/{item}.png'),(50,83))
            if player.baleog.inventory_selected == number:
                if not (player.active == 2 and self.inventory_enabled and self.selected_hidden and not self.selected_item):
                    selected_image = Image.open(file+f'assets/textures/vikings_images/selected.png')
                    if number == '1':
                        image.paste(selected_image,(34,67),mask=selected_image)
                    if number == '2':
                        image.paste(selected_image,(50,67),mask=selected_image)
                    if number == '3':
                        image.paste(selected_image,(34,83),mask=selected_image)
                    if number == '4':
                        image.paste(selected_image,(50,83),mask=selected_image)
        self.texture = Texture(image)
        if self.inventory_enabled:
            inventory_timer -= 1
            self.hidden_timer -= 1
            if self.hidden_timer < 0:
                self.selected_hidden = not self.selected_hidden
                self.hidden_timer = 7
    def input(self,key):
        global inventory_timer
        if self.inventory_enabled:
            if key == 'INVENTORY' and inventory_timer < 1:
                self.inventory_disable()
                application.resume()
                inventory_timer = 10
            if key == 'NEXT':
                player.next_viking()
                self.selected_item = False
                self.selected_item_viking = None
            if key in 'W S A D'.split(' ') and not self.selected_item:
                conditions = {
                'W': {'1':'1', '2':'2', '3':'1', '4':'2'},
                'S': {'1':'3', '2':'4', '3':'3', '4':'4'},
                'A': {'1':'1', '2':'1', '3':'3', '4':'3'},
                'D': {'1':'2', '2':'2', '3':'4', '4':'4'}
                }
                if player.active == 0:
                    selected_old = player.erik.inventory_selected
                if player.active == 1:
                    selected_old = player.olaf.inventory_selected
                if player.active == 2:
                    selected_old = player.baleog.inventory_selected
                selected_new = conditions[key.split(' ')[0]][selected_old]
                if player.active == 0:
                    player.erik.inventory_selected = selected_new
                if player.active == 1:
                    player.olaf.inventory_selected = selected_new
                if player.active == 2:
                    player.baleog.inventory_selected = selected_new
            if key == 'SPACE':
                if self.selected_item:
                    self.selected_item = None
                    self.selected_item_viking = None
                    player.for_all('set_inventory_selected()')
                else:
                    if player.active == 0:
                        if not player.erik.inventory[player.erik.inventory_selected] == None:
                            self.selected_item = player.erik.inventory_selected
                            self.selected_item_viking = 0
                    if player.active == 1:
                        if not player.olaf.inventory[player.olaf.inventory_selected] == None:
                            self.selected_item = player.olaf.inventory_selected
                            self.selected_item_viking = 1
                    if player.active == 2:
                        if not player.baleog.inventory[player.baleog.inventory_selected] == None:
                            self.selected_item = player.baleog.inventory_selected
                            self.selected_item_viking = 2
            if key == 'Q':
                if player.active == 0:
                    player.erik.inventory[player.erik.inventory_selected] = None
                    player.erik.set_inventory_selected()
                if player.active == 1:
                    player.olaf.inventory[player.olaf.inventory_selected] = None
                    player.olaf.set_inventory_selected()
                if player.active == 2:
                    player.baleog.inventory[player.baleog.inventory_selected] = None
                    player.baleog.set_inventory_selected()
            if key in 'S D'.split(' ') and self.selected_item:
                if self.selected_item_viking == 0:
                    if distance(player.erik,player.olaf) < 2:
                        a = player.olaf.pick_up_item(player.erik.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 1
                        player.erik.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 1
                        player.set_active(player.active)
                        player.olaf.inventory_selected = a
                    elif distance(player.erik,player.baleog) < 2:
                        a = player.baleog.pick_up_item(player.erik.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 2
                        player.erik.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 2
                        player.set_active(player.active)
                        player.baleog.inventory_selected = a
                elif self.selected_item_viking == 1:
                    if distance(player.olaf,player.baleog) < 2:
                        a = player.baleog.pick_up_item(player.olaf.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 2
                        player.olaf.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 2
                        player.set_active(player.active)
                        player.baleog.inventory_selected = a
                    elif distance(player.olaf,player.erik) < 2:
                        a = player.erik.pick_up_item(player.olaf.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 0
                        player.olaf.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 0
                        player.set_active(player.active)
                        player.erik.inventory_selected = a
                elif self.selected_item_viking == 2:
                    if distance(player.baleog,player.erik) < 2:
                        a = player.erik.pick_up_item(player.baleog.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 0
                        player.baleog.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 0
                        player.set_active(player.active)
                        player.erik.inventory_selected = a
                    elif distance(player.baleog,player.olaf) < 2:
                        a = player.olaf.pick_up_item(player.baleog.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 1
                        player.baleog.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 1
                        player.set_active(player.active)
                        player.olaf.inventory_selected = a
            if key in 'W A'.split(' ') and self.selected_item:
                if self.selected_item_viking == 0:
                    if distance(player.erik,player.baleog) < 2:
                        a = player.baleog.pick_up_item(player.erik.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 2
                        player.erik.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 2
                        player.set_active(player.active)
                        player.baleog.inventory_selected = a
                    elif distance(player.erik,player.olaf) < 2:
                        a = player.olaf.pick_up_item(player.erik.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 1
                        player.erik.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 1
                        player.set_active(player.active)
                        player.olaf.inventory_selected = a
                elif self.selected_item_viking == 1:
                    if distance(player.olaf,player.erik) < 2:
                        a = player.erik.pick_up_item(player.olaf.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 0
                        player.olaf.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 0
                        player.set_active(player.active)
                        player.erik.inventory_selected = a
                    elif distance(player.olaf,player.baleog) < 2:
                        a = player.baleog.pick_up_item(player.olaf.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 2
                        player.olaf.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 2
                        player.set_active(player.active)
                        player.baleog.inventory_selected = a
                elif self.selected_item_viking == 2:
                    if distance(player.baleog,player.olaf) < 2:
                        a = player.olaf.pick_up_item(player.baleog.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 1
                        player.baleog.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 1
                        player.set_active(player.active)
                        player.olaf.inventory_selected = a
                    elif distance(player.baleog,player.erik) < 2:
                        a = player.erik.pick_up_item(player.baleog.inventory[self.selected_item])
                        if not a:
                            return
                        self.selected_item_viking = 0
                        player.baleog.inventory[self.selected_item] = None
                        self.selected_item = a
                        player.active = 0
                        player.set_active(player.active)
                        player.erik.inventory_selected = a
    def inventory_enable(self):
        self.inventory_enabled = True
        self.selected_item = False
        self.selected_item_viking = None
        mouse.visible = True
        mouse.locked = False
        mouse.position = (0,0)
    def inventory_disable(self):
        self.inventory_enabled = False
        self.selected_item = False
        self.selected_item_viking = None
        mouse.visible = False
        mouse.locked = True
        mouse.position = (0,0)

def signal_send(signal):
    for i in objs:
        i.check_signal(signal)
    for i in objs_not_collides:
        i.check_signal(signal)
    for i in acids:
        i.check_signal(signal)

def load_map(n):
    global exit_entity
    with open(file+f'assets/maps/{n}') as f:
        lines = f.read()
    erik_pos = False
    olaf_pos = False
    baleog_pos = False
    for line in lines.split('\n'):
        if not '#' in line:
            data = line.split(' ')
            if len(data) == 4:
                if data[0] in 'bdfgj':
                    objs_not_collides.append(E(type=data[0],data=None,position=(float(data[1])*2,float(data[2])*2,float(data[3])*2)))
                elif data[0] == 'c':
                    acids.append(E(type=data[0],data=None,position=(float(data[1])*2,float(data[2])*2,float(data[3])*2)))
                elif data[0] in 'ahik':
                    objs.append(E(type=data[0],data=None,position=(float(data[1])*2,float(data[2])*2,float(data[3])*2)))
                elif data[0] == 'E':
                    player.erik.position = (float(data[1])*2,float(data[2])*2,float(data[3])*2)
                    erik_pos = True
                elif data[0] == 'O':
                    player.olaf.position = (float(data[1])*2,float(data[2])*2,float(data[3])*2)
                    olaf_pos = True
                elif data[0] == 'B':
                    player.baleog.position = (float(data[1])*2,float(data[2])*2,float(data[3])*2)
                    baleog_pos = True
            if len(data) == 5:
                if data[0] in 'bdfgj':
                    objs_not_collides.append(E(type=data[0],data=data[4],position=(float(data[1])*2,float(data[2])*2,float(data[3])*2)))
                elif data[0] == 'c':
                    acids.append(E(type=data[0],data=data[4],position=(float(data[1])*2,float(data[2])*2,float(data[3])*2)))
                elif data[0] == 'e':
                    enemies.append(Enemy(data=data[4],position=(float(data[1])*2,float(data[2])*2,float(data[3])*2)))
                elif data[0] in 'ahik':
                    objs.append(E(type=data[0],data=data[4],position=(float(data[1])*2,float(data[2])*2,float(data[3])*2)))
                elif data[0] == 'E':
                    player.erik.position = (float(data[1])*2,float(data[2])*2,float(data[3])*2)
                    erik_pos = True
                elif data[0] == 'O':
                    player.olaf.position = (float(data[1])*2,float(data[2])*2,float(data[3])*2)
                    olaf_pos = True
                elif data[0] == 'B':
                    player.baleog.position = (float(data[1])*2,float(data[2])*2,float(data[3])*2)
                    baleog_pos = True
    if not erik_pos:
        player.erik.position = (0,0,0)
    if not olaf_pos:
        player.olaf.position = (0,0,0)
    if not baleog_pos:
        player.baleog.position = (0,0,0)
    try:
        exit_entity
    except:
        exit_entity = Entity(model=None,collider=None,position=(99999,99999,99999))

def update():
    global fps, inventory_timer, mouse_entities
    mouse_entities = []
    for i in mouse.collisions:
        mouse_entities += [i.entity]
    fps = fps_counter.fps
    inventory_timer -= 1
    try:
        player.for_all('set_collider(True)')
        for i in enemies:
            i.update_internal()
        player.for_all('set_collider(False)')
    except:
        pass

def set_game_state_normal():
    global game_state
    game_state = 1

def reload_map(map_name):
    global objs, arrows, acids, objs_not_collides, enemies, lasers
    for i in objs:
        try:
            destroy(i)
        except:
            pass
    for i in objs_not_collides:
        try:
            destroy(i)
        except:
            pass
    for i in arrows:
        try:
            destroy(i)
        except:
            pass
    for i in acids:
        try:
            destroy(i)
        except:
            pass
    for i in lasers:
        try:
            destroy(i)
        except:
            pass
    for i in enemies:
        try:
            destroy(i)
        except:
            pass
    destroy(exit_entity)
    objs = []
    acids = []
    objs_not_collides = []
    arrows = []
    lasers = []
    enemies = []
    load_map(map_name)
    player.restart()
    invoke(set_game_state_normal,delay=.5)

def reset():
    reload_map(selected_map)
    destroy(tmp1)
    destroy(tmp2)
    set_game_state_normal()

def game_over():
    global game_state, tmp1, tmp2
    game_state = 4
    tmp1 = Entity(model='quad',parent=camera.ui,color=(0,0,0,1),scale=(1000,1000))
    some = random.choice([
        '<green>Olaf<default>: A SNAŽ SE!',
        '<red>Erik<default>: Jak dlouho tady ještě budeme šaškovat?',
        '<yellow>Baleog<default>: Cože, my tu ještě pořád jsme?',
        '<red>Erik<default>: Proč nejdeme domů? Vždyť stejně tady nic nezmůžeme!',
        '<green>Olaf<default>: Co jsme komu provedli?',
        ])
    tmp2 = Text(text=f'<scale:2><red>PROHRÁL JSI<default>\n<scale:1>zkus to znovu<default>\n<scale:0.7>{some}<default>',origin=(0,0))

def win():
    global selected_map, game_state, tmp1, tmp2
    game_state = 2
    with open(file+'assets/maps/maps') as f:
        maps = f.read().split('\n')
    next_map = maps[maps.index(selected_map) + 1]
    if next_map != ':':
        selected_map = next_map
        tmp1 = Entity(model='quad',parent=camera.ui,color=(0,0,0,1),scale=(1000,1000))
        tmp2 = Text(text=f'heslo:\n\n<scale:1.5><yellow>{next_map}<default>',origin=(0,0))
    else:
        game_state = 3
        with open(file+'assets/maps/maps') as f:
            levels = f.read().replace(':','')
        tmp1 = Entity(model='quad',parent=camera.ui,color=(0,0,0,1),scale=(1000,1000))
        tmp2 = Text(text='<green>VYHRÁL JSI<default>',ignore_paused=True,origin=(0,.6),position=(0,.5),scale=(5,5))
        tmp3 = Text(text='seznam levelů:\n<yellow>'+levels+'<default>',ignore_paused=True,origin=(0,.5),position=(0,.35))
        mouse.locked = False
        mouse.visible = True

def start():
    global player, vikings_images, game_state
    with open(file+f'assets/maps/{selected_map}'):
        pass
    player = Player()
    load_map(selected_map)
    vikings_images = VikingsImages()
    game_state = 1

def input(key):
    if game_state == 4 or game_state == 2:
        if key in 'SPACE up/ENTER up'.split('/'):
            reset()

file = '/'.join(os.path.abspath(__file__).split('/')[:-1])+'/'
objs = []
acids = []
objs_not_collides = []
arrows = []
enemies = []
lasers = []
mouse_entities = []
max_id = 0
fps = 0
inventory_timer = 0
# 0 = before game
# 1 = game
# 2 = win
# 3 = full win
# 4 = game over
game_state = 0

app = Ursina(development_mode=False,borderless=False,title='Lost Vikings 3D')
window.color = (0,0,0,1)

debug_text = Text(visible=False,origin=(0,.5),position=(0,.47),ignore_paused=True)
black_screen = BlackScreen()
red_screen = RedScreen()
fps_counter = FPSCounter()

# input_handler.bind('f10','None')
input_handler.bind('f12','DEBUG')
input_handler.bind('f11','CMD')
input_handler.bind('control','NEXT')
input_handler.bind('enter','ENTER')
input_handler.bind('space','SPACE')
input_handler.bind('right mouse down','PRESS')
input_handler.bind('left mouse down','ACTION1')
input_handler.bind('left mouse up','ACTION2')
input_handler.bind('tab','INVENTORY')
input_handler.bind('escape','ESC')
input_handler.bind('a','A')
input_handler.bind('b','B')
input_handler.bind('c','C')
input_handler.bind('d','D')
input_handler.bind('e','E')
input_handler.bind('f','F')
input_handler.bind('g','G')
input_handler.bind('h','H')
input_handler.bind('i','I')
input_handler.bind('j','J')
input_handler.bind('k','K')
input_handler.bind('l','L')
input_handler.bind('m','M')
input_handler.bind('n','N')
input_handler.bind('o','O')
input_handler.bind('p','P')
input_handler.bind('q','Q')
input_handler.bind('r','R')
input_handler.bind('s','S')
input_handler.bind('t','T')
input_handler.bind('u','U')
input_handler.bind('v','V')
input_handler.bind('w','W')
input_handler.bind('x','X')
input_handler.bind('y','Y')
input_handler.bind('z','Z')

PasswdInput()

app.run(info=False)
