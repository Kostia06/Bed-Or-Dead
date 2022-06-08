
import pygame as pg 
import random as r
from level import Level
import clipboard
import json
import os
import sys
import time

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption("Space Traveler")
WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
darkness = pg.Surface((screen.get_size()), pg.SRCALPHA)
clock = pg.time.Clock()
font = None

class Label():
    def __init__(self, text, pos, color = 'Black',shade=['Gray','Gray'], rotate = 0, size = 20, bg = 'White', outline='Black', side = 'center'):
        self.font = pg.font.Font(font,size)
        self.font_size = size
        self.display = self.font.render(str(text), True, color)
        self.rect_new = self.display.get_rect()
        self.side = 'self.rect_new.' + side + ' = (pos)'
        exec(self.side)
        self.rect_new.w += self.font_size
        self.rect_new.h += self.font_size
        self.display = pg.transform.rotate(self.display, rotate)
        if bg != None:
            if rotate == 90 or rotate == 270:
                if shade[1] != None:
                    pg.draw.rect(screen, (shade[1]), (self.rect_new.x - self.font_size/2+5, self.rect_new.y - self.font_size/2+5, self.rect_new.h, self.rect_new.w), 0, 10)
                pg.draw.rect(screen, (bg), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.h, self.rect_new.w), 0, 10)
                if outline != None:
                    pg.draw.rect(screen, (outline), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.h, self.rect_new.w), 3, 10)
            else:
                if shade[1] != None:
                    pg.draw.rect(screen, (shade[1]), (self.rect_new.x - self.font_size/2+5, self.rect_new.y - self.font_size/2+5, self.rect_new.w, self.rect_new.h), 0, 10)
                pg.draw.rect(screen, (bg), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.w, self.rect_new.h), 0, 10)
                if outline != None:
                    pg.draw.rect(screen, (outline), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.w, self.rect_new.h), 3, 10)
        if shade[0] != None:
            self.shade = self.font.render(str(text), True, shade[0])
            self.shade = pg.transform.rotate(self.shade, rotate)
            screen.blit(self.shade, (self.rect_new.x + 4, self.rect_new.y + 4))
        screen.blit(self.display, (self.rect_new))
        self.rect = pg.Rect(self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.w, self.rect_new.h)
class Switch():
    def __init__(self,text, pos, turn, color = 'Black', shade = ['Gray', 'Gray'], size = 20, bg = 'White', outline= 'Black', sides='center'):
        self.font_size = size 
        self.turn = turn
        self.size = size/2
        self.text = text
        self.pos = pos
        self.circle = pg.Vector2()
        self.clicked = False
        self.rect_new = pg.Rect(pos[0], pos[1], size * 5, size * 1.5)
        self.max = self.rect_new.right - 5
        self.least = self.rect_new.left + 5
        self.circle.x = self.least
        self.circle.y = self.rect_new.centery
        self.side = sides
        self.color = color
        self.bg = bg
        self.outline = outline
        self.shades = shade
    def draw(self):
        pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0] ==1 :
            if self.rect_new.collidepoint(pos) and  not self.clicked:
                self.clicked = True
                if self.turn:
                    self.turn= False
                elif not self.turn:
                    self.turn = True
        if pg.mouse.get_pressed()[0] == 0:
            self.size = self.font_size/1.5 + 2
        
        if pg.mouse.get_pressed()[0] == 0 and self.clicked:
            self.clicked = False
        elif pg.mouse.get_pressed()[0] == 0 and not self.rect_new.collidepoint(pos):
            self.size = self.font_size/1.5
        if self.turn:
            self.color_circle = 'Green'
            self.circle.x = self.max
        elif not self.turn: 
            self.color_circle = 'Red'
            self.circle.x = self.least
        pg.draw.rect(screen, ('White'), (self.rect_new), 0, 15)
        pg.draw.rect(screen, ('Gray'), (self.rect_new), 0, 15)
        pg.draw.rect(screen, (self.color_circle), (self.rect_new), 0, 15)
        pg.draw.rect(screen, ('Black'), (self.rect_new), 3, 15)
        pg.draw.circle(screen, ('white'), (self.circle.x, self.circle.y), self.size)
        pg.draw.circle(screen, ('Black'), (self.circle.x, self.circle.y), self.size, 2)
        Label(self.text, (self.rect_new.x, self.rect_new.centery - self.font_size - self.rect_new.w/10 - 5), size=self.font_size, side=self.side, shade=self.shades, outline=self.outline, bg=self.bg, color = self.color)
    def choice(self):
        if self.turn:
            return True
        else:
            return False
class Button():
    def __init__(self, text, pos,  size = 20, shade = ['Gray', 'Gray'], color='Black', bg='White', outline = 'Black', side = 'center', r =10):
        self.clicked = False
        self.bg = bg
        self.outline = outline
        self.shade = shade
        self.side = side
        self.font = pg.font.Font(font,size)
        self.display = self.font.render(str(text), True, color)
        if shade[0] != None:
            self.shade_display = self.font.render(str(text), True, shade[0])
        self.font_size = size
        self.rect_new = self.display.get_rect()
        self.side = 'self.rect_new.' + side + ' = (pos)'
        self.text = text
        exec(self.side)
        self.rect_new.w += self.font_size
        self.rect_new.h += self.font_size
        self.offset = 0
        self.rect = pg.Rect(-500, -500, 0, 0)
        self.r =r
    def draw(self):
        if self.shade[1] != None:
            pg.draw.rect(screen,(self.shade[1]), (self.rect_new.x - self.font_size/2, self.rect_new.y-self.font_size/2, self.rect_new.w + 5, self.rect_new.h + 5), 0, self.r)
        if self.bg != None:
            pg.draw.rect(screen,(self.bg), (self.rect_new.x - self.font_size/2 + self.offset , self.rect_new.y-self.font_size/2 + self.offset, self.rect_new.w, self.rect_new.h), 0, self.r)
        if self.outline != None:
            pg.draw.rect(screen,(self.outline), (self.rect_new.x - self.font_size/2 + self.offset, self.rect_new.y-self.font_size/2 + self.offset, self.rect_new.w , self.rect_new.h), 3, self.r)
        if self.shade[0] != None:
            screen.blit(self.shade_display, (self.rect_new.x + self.offset, self.rect_new.y + self.offset ))
        screen.blit(self.display, (self.rect_new.x + self.offset , self.rect_new.y + self.offset))
        self.rect = pg.Rect(self.rect_new.x - self.font_size/2 + self.offset, self.rect_new.y-self.font_size/2 + self.offset, self.rect_new.w, self.rect_new.h)
    def choice(self):
        action = False
        if pg.mouse.get_pressed()[0] ==1:
            try:
                if self.rect.collidepoint(pg.mouse.get_pos()):
                    self.clicked = True
                    action = True
                    return action
            except:
                pass
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
class Bar():
    def __init__(self,pos, size, color=['green', 'yellow', 'red'], shade='Grey', outline='Black', time=5000):
        self.color = color
        self.color_choice = 1
        self.size = size
        self.pos = pos
        self.outline = outline
        self.shade = shade
        self.current_time = 0
        self.press_time = 0
        self.time = time
        self.ratio = time/ self.size[0]
        self.show = False
        self.clicked = False
        self.work = True
    def draw(self, item):
        self.rect = pg.Rect(item.rect.centerx-self.pos[0] -self.size[0]/2, item.rect.centery -self.pos[1] - self.size[1]/2, self.size[0],self.size[1])

        if self.show and not self.current_time - self.press_time>self.time:
            if self.shade != None:
                pg.draw.rect(screen, self.shade, (self.rect.x, self.rect.y, self.size[0] +5, self.rect.h + 5), 0, 5)
            try:
                pg.draw.rect(screen, (self.color[self.color_choice-1]), (self.rect.x, self.rect.y, (self.current_time - self.press_time)/self.ratio, self.rect.h), 0, 5)
            except:
                pass
            if self.outline != None:
                pg.draw.rect(screen, (self.outline), self.rect, 3, 5)

        if not item.clicked or not self.work:
            self.press_time = pg.time.get_ticks()
            self.show = False
            self.clicked = False
            self.color_choice = 1
        else:
            self.show = True
        self.current_time = pg.time.get_ticks()
        if self.current_time - self.press_time>self.time and not self.clicked:
            self.color_choice = 1
            self.press_time = 0
            self.current_time = 0
            self.show = False
            self.clicked = True
        if self.current_time - self.press_time > self.time/len(self.color) * self.color_choice:
            self.color_choice += 1
    def choice(self):
        return self.clicked
class Scale():
    def __init__(self, text, pos, scale, set, size = 20, shade = 'Gray', color = 'Black', bg = True,bg_color = 'White', shades = True, outline = 'Black'):
        self.pos = pos
        self.text = text
        self.scale = scale
        self.font = pg.font.Font(font,size)
        self.scale = scale
        self.list = (bg, bg_color, color, shade, outline, size, shades)
        self.scale_pos = pg.Vector2()
        self.rect_new = pg.Rect(pos[0], pos[1],size * 5, size/2)
        self.scale_pos.x = pos[0] + set * size/100 * 5
        self.font_size = size
        self.scale_pos.y = self.rect_new.centery + self.rect_new.h
        self.rect_new.h += self.font_size
        self.num = 50
        self.font_size = size
        self.changed = False
        self.size =size/2
    def draw(self):
        pos = pg.mouse.get_pos()
        if self.rect_new.collidepoint(pos):
            self.size = self.font_size/2 + 1
        elif pg.mouse.get_pressed()[0] ==0 and not self.rect_new.collidepoint(pos):
            self.size = self.font_size/2
        if self.list[6]:
            pg.draw.rect(screen,(self.list[3]), (self.rect_new.x + 4, self.rect_new.y + 4, self.rect_new.w, self.rect_new.h), 0, 15)
        pg.draw.rect(screen,('White'), (self.rect_new), 0, 15)
        if self.list[4] != None:
            pg.draw.rect(screen,(self.list[4]), (self.rect_new), 2, 15)
        pg.draw.circle(screen, ('White'), (self.scale_pos),self.size)
        pg.draw.circle(screen, ('Black'), (self.scale_pos),self.size, 2)
        if pg.mouse.get_pressed()[0] ==1:
            if self.rect_new.collidepoint(pos):
                self.changed = True
                self.scale_pos.x = pg.mouse.get_pos()[0]
                self.num = (self.pos[0] - self.scale_pos.x)/((self.font_size * 5)/100)
                if abs(self.num) < 0:
                    self.num = 0.0
                self.size = self.font_size/2 + 2
                num_display = self.font.render(str(abs(int(self.num))), True, 'Black')
                num_rect = num_display.get_rect()
                screen.blit(num_display, (self.scale_pos +(-num_rect.w/2,self.font_size/2)))
        Label(self.text, (self.rect_new.centerx, self.rect_new.centery - self.font_size - self.rect_new.w/5), color = self.list[2],bg = self.list[0], bg_color =self.list[1], shade = self.list[3], outline=self.list[4], size = self.list[5], shades=self.list[6])
    def choice(self):
        return abs(self.num)
class Input():
    def __init__(self, text, pos, num, size = 20, color='Black',bg='White', shade=['Gray', "Gray"], type=str, sides=['center', 'center']):
        self.num = num + 1
        self.text = text[0]
        self.rect_new = pg.Rect(0,0,0,0)
        self.rect_new.center = (pos)
        self.clicked = False
        self.output = text[1]
        self.type = type       
        self.offset = 0
        self.size = size
        self.output_rect = None
        self.shade = shade
        self.bg = bg
        self.color = color
        self.sides = sides
    def draw(self,event, single = False):
        pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0] ==1 and self.output_rect != None:
            if self.output_rect.rect.collidepoint(pos):
                self.clicked = True
        if pg.mouse.get_pressed()[0] == 1 and self.clicked:
            if not self.output_rect.rect.collidepoint(pos):
                self.clicked = False
        if self.clicked:
            for event in event:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.output = self.output[:-1]
                    elif len(self.output) + 1 < self.num and not single:
                        if self.type == str:
                            self.output += event.unicode
                        elif event.key != 1073742051:
                            try:
                                send = event.unicode
                                send = int(send)
                                self.output += str(send)
                            except:
                                pass
                        if event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                            self.output = self.output[:-1]
                            text = clipboard.paste()
                            self.output += text
                    elif len(self.output) + 1 < self.num and single:
                        self.output = event.key
                    else:
                        self.clicked = False
        if self.text != '':
            Label(self.text, (self.rect_new.center),shade=self.shade, bg=self.bg, color=self.color, size = self.size, side=self.sides[0])
            if self.clicked:
                self.output_rect = Label(self.output + '|', (self.rect_new.centerx, self.rect_new.bottom +self.rect_new.h*2 + self.size*2 + 20),shade=self.shade, bg=self.bg, color=self.color, size = self.size, side=self.sides[1])
            else:
                self.output_rect = Label(self.output, (self.rect_new.centerx, self.rect_new.bottom + self.rect_new.h*2 + self.size*2 + 20),shade=self.shade, bg=self.bg, color=self.color, size = self.size, side=self.sides[1])
        else:
            if self.clicked:
                self.output_rect = Label(self.output + '|', (self.rect_new.center),shade=self.shade, bg=self.bg, color=self.color, size = self.size, side=self.sides[1])
            else:
                self.output_rect = Label(self.output, (self.rect_new.center),shade=self.shade, bg=self.bg, color=self.color, size = self.size, side=self.sides[1])
    def choice(self):
        if not self.clicked:
            return self.output

class Game():
    def __init__(self):
        self.clock = pg.time.Clock()
        self.level = Level(screen)
        self.menu = Menu()
        self.edit =False
        if self.edit:
            self.menu.start = True
        self.darkness = False
        self.change_work = False
        self.bg = BackGround()
        self.start_work = False
        self.back_work = False
        self.light = pg.Surface((screen.get_size()), pg.SRCALPHA)
        self.light_num = 0
        self.run()
    def start(self, num):
        self.level.current_level = num
        self.level.create_map()
        self.start_scene()
        self.bg.start_scene()
    def start_scene(self):
        self.start_work = True
        if self.bg.start_scene():
            self.start_work = False
        if self.bg.open < 0:
            self.menu.start = True
    def back_scene(self):
        self.back_work =True
        if self.bg.start_scene():
            self.back_work = False
            self.level.lose()
        if self.bg.open <0:
            self.menu.start = False
    def chnage_bg(self, turn):
        self.darkness = turn

    def change(self):
        if self.bg.change_scene(self.level.new_level, self.chnage_bg):
            self.change_work = False
    def change_it(self):
        self.change_work = True

    def won(self):
        self.level.room = 0 
        if self.level.current_level == self.level.level:
            for i in range(5):
                if self.level.level == i+1:
                    self.level.level = i+2
                    break
        self.darkness = False
        self.back_work = True
    def run(self):
        info = Info()
        while True:
            player = self.level.player
            events = pg.event.get()
            clock.tick(60)
            for i in events:
                if i.type == pg.QUIT:
                    if self.edit:
                        self.level.save()
                    pg.quit()
                    sys.exit()
                if i.type ==pg.KEYDOWN and not info.lose():
                    if i.key == pg.K_SPACE and self.menu.start:
                        self.darkness = True
            if self.darkness:
                screen.fill((28, 5, 32))
            else:
                player.work = False
                screen.fill((255, 241, 118))
            if not self.menu.start:
                self.menu.draw(events, self.level.level, self.start, self.start_work)


            if self.menu.start:
                self.level.run()
                if self.darkness:
                    player.work = True
                    pg.draw.rect(darkness, (1, 1, 1, 255), (0,0,screen.get_size()[0], screen.get_size()[1]))
                    pg.draw.circle(darkness, (55,55,55, 150), (player.rect.centerx, player.rect.centery), 70)
                    pg.draw.circle(darkness, (200,200,200, 100), (player.rect.centerx, player.rect.centery), 60)
                    pg.draw.circle(darkness, (225,225,225, 0), (player.rect.centerx, player.rect.centery), 30)
                    if player != None:
                        for i in self.level.enemy:
                            i.build = True

                            i.player = player
                            i.draw(screen, darkness)
                        for i in self.level.door:
                            i.player = player
                            i.animation = self.change_it
                            i.draw(screen, darkness)
                        for i in self.level.bed:
                            i.level_change = self.won
                            i.player = player
                    screen.blit(darkness, (0,0))
                    
            for i in self.level.door:
                if i.collide:
                    player.work = False
                    for i in self.level.enemy:
                        i.work = False
                        i.build = False
            if not self.edit:
                self.bg.draw(self.darkness)
            else:
                self.level.map.debug(events)

            if self.change_work:
                self.change()
            elif self.start_work:
                self.start_scene()
            elif self.back_work:
                self.back_scene()

            if player != None and self.menu.start:
                info.update(player) 

            if self.menu.start:
                if info.lose():
                    player.work = False
                    for i in self.level.enemy:
                        i.work = False
                    if info.start.choice():
                        self.menu.start = False
                        self.level.lose()
                        self.back_work = True
                        self.darkness = False
            Label(f'{int(clock.get_fps())}, {self.level.level}', (WIDTH-100, 10), shade=[None,None], bg='black', color='white')
            if not self.edit:
                self.light_num = ((self.level.level -1) * 40)
                pg.draw.rect(self.light, (0, 0,0, self.light_num), (0,0,screen.get_size()[0], screen.get_size()[1]))
                screen.blit(self.light, (0,0))
            pg.display.update()


one = Button('1', (-100, -100), shade=[None,None], size=30, r=50)
two = Button('2', (-100, -100), shade=[None,None], size = 30, r=50)
three = Button('3', (-100, -100), shade=[None,None], size=30, r =50)
four = Button('4', (-100, -100), shade=[None,None], size=30, r=50)
five = Button('5', (-100, -100), shade=[None,None], size=30, r=50)
class Menu():
    def __init__(self):
        self.start = False
        self.pos = []
        self.levels = [five, four, three, two, one]
        for i in range(5):
            i += 1
            self.pos.append(i * 72)
        self.level_pos = []
        self.offset = 0
    def draw(self, event, level, start, work):
        for i in event:
            if i.type == pg.MOUSEBUTTONDOWN:
                if i.button == 4:#down
                    self.offset -= 72
                elif i.button ==5:#up
                    self.offset += 72
        for i in self.pos:
            self.level_pos.append(pg.Vector2((WIDTH//2, HEIGHT//2)) + pg.Vector2(1,0).rotate( i+90 + self.offset) * 150)
        
        for i in range(5):
            self.levels[i].rect_new.x, self.levels[i].rect_new.y = self.level_pos[i]
        pg.draw.polygon(screen, (28, 5, 32), self.level_pos, 10)
        for i in self.levels:
            i.offset = -5
            i.draw()
            if int(i.text) <= level:
                i.bg = '#05ff00'
                if i.choice() and not work:
                    start(int(i.text))

            else:
                i.bg = '#E61B35'
        self.level_pos.clear()
class Info():
    def __init__(self):
        self.color = [0,255,0]
        self.health = 255
        self.health_max = 255
        self.h_length = 100
        self.start = Button('Start Over', (WIDTH//2, HEIGHT//2 + 80),  shade=[None,None], bg='black', color='white', size=30, outline='white')
        self.health_ratio = self.health_max / self.h_length
    def update(self, player):
        try:
            pg.draw.rect(screen,self.color, (10, 10, self.health/self.health_ratio, 20), 0, 5)
            pg.draw.rect(screen,'black', (10, 10, 100, 20), 2, 5)
        except:
            pass
        self.color[0] =   0 + player.fear 
        self.color[1] = 255 - player.fear
        self.health = 255 - player.fear
    def lose(self):
        if self.health <= 0:
            Label('You Lost', (WIDTH//2, HEIGHT//2),  shade=[None,None], bg='black', color='white', size=40, outline='white')
            self.start.draw()
            return True
        else: 
            return False
class Dots():
    def __init__(self, pos):
        self.pos = pos
        self.size = r.randint(5,10)
        self.x = r.choice((-1,1))
        self.y = r.choice((-1,1))
        self.prev_time = time.perf_counter()
    def draw(self):
        self.transparent = pg.Surface((screen.get_size()), pg.SRCALPHA)
        now = time.perf_counter()
        dt = now - self.prev_time
        self.prev_time = now
        pg.draw.circle(screen, ('black'), (self.pos),self.size)
        pg.draw.circle(self.transparent, (0,0,0, 50), (self.pos), self.size+5)
        if r.randint(1,1000) == 1:
            self.x = r.choice((-1,1))
            self.y = r.choice((-1,1))
        self.pos[0] += self.x * dt * 30
        self.pos[1] += self.y * dt * 30 
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.x *= -1
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.y *= -1
        screen.blit(self.transparent, (0,0))
class BackGround():
    def __init__(self):
        self.speed = 3
        self.left = []
        self.right =[]
        self.triangle = {1:[[0,0],[0,0],[0,0]], 2:[[WIDTH, HEIGHT], [WIDTH, HEIGHT], [WIDTH, HEIGHT]]}
        self.open = 10
        self.change_color = (28, 5, 32)
        self.offset = 0
        self.offset_num = 0.5
        for i in range(-200, HEIGHT , 75):
            self.left.append([0,i])
        for i in range(-200, HEIGHT , 75):
            self.right.append([WIDTH,i + 75])
        self.shines = []
        for i in range(20):
            self.shines.append(Dots([r.randint(0, WIDTH),r.randint(0, HEIGHT) ]))
    def draw(self, darkness):
        if darkness:
            self.speed = 3
            for i in range(8):
                if self.left[i][1]> 400:
                    self.left[i][1] = - 200
                    self.right[i][1] = - 125
                pg.draw.line(screen, 'black', (self.left[i][0],self.left[i][1] ), (self.right[i][0], self.right[i][1] + self.offset), 10)
                self.left[i][1] += self.speed 
                self.right[i][1] += self.speed 
            for i in self.shines:
                i.draw()
            if self.offset > 200 or self.offset < 0:
                    self.offset_num *= -1
        else:
            self.speed = 1
            for i in range(8):
                if self.left[i][1]> 400:
                    self.left[i][1] = - 200
                    self.right[i][1] = - 125
                pg.draw.line(screen, (245,127,23), (self.left[i][0],self.left[i][1] ), (self.right[i][0], self.right[i][1] + self.offset), 10)
                self.left[i][1] += self.speed 
                self.right[i][1] += self.speed 
            self.offset +=self.offset_num
            if self.offset > 200 or self.offset < 0:
                self.offset_num *= -1
    def change_scene(self, change, bg):
        pg.draw.polygon(screen, self.change_color, self.triangle[1])
        pg.draw.polygon(screen, self.change_color, self.triangle[2])
        self.triangle[1][1][0] += self.open
        self.triangle[1][2][1] += self.open
        self.triangle[2][1][0] -= self.open
        self.triangle[2][2][1] -= self.open
        if self.triangle[1][1][0] > WIDTH//1.1:
            self.open *= -1
            if bg != None:
                self.change_color = (255, 241, 118)
                bg(False)
                change()
        if self.triangle[1][1][0] < 0:
            self.open *= -1
            if bg != None:
                self.change_color = (28, 5, 32)
            return True
    def win_scene(self):
        pg.draw.polygon(screen, self.change_color, self.triangle[1])
        pg.draw.polygon(screen, self.change_color, self.triangle[2])
        if self.triangle[1][1][0] > WIDTH//1.1:
            Label('You Won', (WIDTH//2, HEIGHT//2),shade=[None,None], bg=None, color='Black', size=40)
        else:
            self.triangle[1][1][0] += self.open
            self.triangle[1][2][1] += self.open
            self.triangle[2][1][0] -= self.open
            self.triangle[2][2][1] -= self.open
    def start_scene(self):
        self.change_color = (255, 241, 118)
        pg.draw.polygon(screen, self.change_color, self.triangle[1])
        pg.draw.polygon(screen, self.change_color, self.triangle[2])
        self.triangle[1][1][0] += self.open
        self.triangle[1][2][1] += self.open
        self.triangle[2][1][0] -= self.open
        self.triangle[2][2][1] -= self.open
        if self.triangle[1][1][0] > WIDTH//1.1:
            self.open *= -1
        elif self.triangle[1][1][0] < 0:
            self.open *= -1
            self.change_color = (28, 5, 32)
            return True
        else:
            return False

Game()
