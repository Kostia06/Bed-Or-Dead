
import pygame as pg 
import os
import json
WIDTH, HEIGHT = 600, 400
name = 'Levels/5/1.txt'
class Map():
    def __init__(self, dir, name, screen:pg.display):
        self.file_name = name
        self.dir = dir
        self.list = {}
        self.object_list = []
        self.draw = []
        self.screen = screen
        self.num = 0
        self.rect = pg.Rect(10, self.screen.get_size()[1]- 90, 80, 80)
        self.pos = None
        self.transparency = pg.Surface((screen.get_size()), pg.SRCALPHA)
        self.selected = False
        self.loaded =False
        self.outside = True
    def mapping(self, info):
        for _, name in enumerate(info):
            self.list[_] = info[name]
    def debug(self, event):
        if not self.loaded:
            self.loading()
            self.loaded = True
        mouse = pg.mouse.get_pressed(), pg.mouse.get_pos()
        img = pg.image.load(os.path.join(self.list[self.num]['img'])).convert_alpha()
        img = pg.transform.scale(img, (80, 80))
        for i in event:
            if i.type == pg.MOUSEBUTTONDOWN and not self.selected:
                if i.button == 4:#down
                    if self.num != 0:
                        self.num -= 1
                    else:
                        self.num = len(self.list) -1
                elif i.button ==5:#up
                    if self.num != len(self.list) -1:
                        self.num += 1
                    else:
                        self.num = 0
            if i.type == pg.KEYDOWN:
                if i.key == pg.K_z:
                    self.draw.pop()
                    self.object_list.pop()
                if i.key == pg.K_a:
                    self.outside = not self.outside

        pg.draw.rect(self.screen, 'white', self.rect)
        pg.draw.rect(self.screen, 'black', self.rect, 2)
        self.screen.blit(img, (self.rect))
        if mouse[0][0] == 1 and self.rect.collidepoint(mouse[1]):
            self.selected = True
        if self.selected and  mouse[0][0] == 1:
            self.img = pg.image.load(os.path.join(self.list[self.num]['img'])).convert_alpha()
            self.img = pg.transform.scale(self.img,self.list[self.num]['size'] )
            self.pos = [int(mouse[1][0] -self.list[self.num]['size'][0]/2), int(mouse[1][1] - self.list[self.num]['size'][1]/2)]
            self.screen.blit(self.img, (self.pos))
        elif self.selected and  mouse[0][0] == 0:
            self.selected = False
            self.build(self.img,self.pos, self.list[self.num])
        for i in self.draw:
            self.screen.blit(i[0], i[1])
    def loading(self):
        try: 
            with open(name) as datas:
                objects = json.load(datas)
            for _, i in enumerate(objects):
                img = pg.image.load(os.path.join(i[0]['img'])).convert_alpha()
                img = pg.transform.scale(img, i[0]['size'])
                pos = i[1]
                l = [img, pos]
                self.draw.append(l)
                self.object_list.append(i)
        except  FileNotFoundError:
            pass
    def save(self):
        with open(name, 'w') as datas:
            json.dump(self.object_list, datas)
    def build(self,img,pos, info):
        for i in self.draw:
            if self.outside:
                if pos[0] < 0:
                    pos[0] = 0
                elif pos[0] > self.screen.get_size()[0]:
                    pos[0] = self.screen.get_size()[0]
                if pos[1] < 0:
                    pos[1] = 0
                elif pos[1] > self.screen.get_size()[1]:
                    pos[1] = self.screen.get_size()[1]
            x = range(i[1][0] -2, i[1][0] +2, 1)
            y = range(i[1][1] -2, i[1][1]+2, 1)
            if pos[0] in x :
                print('x snapted')
                pos[0] = i[1][0]
                if pos[1] < i[1][1]:
                    if abs(pos[1] + info['size'][1] - i[1][1]) < 5:
                        pos[1] = i[1][1] - info['size'][1]
                        print('y top snapted')
                elif pos[1] > i[1][1]:
                    if abs(pos[1] - info['size'][1] - i[1][1]) < 5:
                        pos[1] = i[1][1] + info['size'][1]
                        print('y bottom snapted')

            elif pos[1] in y:
                print('y snapted')
                pos[1] = i[1][1]
                if pos[0] < i[1][0]:
                    if abs(pos[0] + info['size'][0] - i[1][0]) < 5:
                        pos[0] = i[1][0] - info['size'][0]
                        print('x left snapted')
                elif pos[0] > i[1][0]:
                        if abs(pos[0] - info['size'][0] - i[1][0]) < 5:
                            pos[0] = i[1][0] + info['size'][0]
                            print('x right snapted')
        draw = [img, pos]
        self.draw.append(draw)
        self.object_list.append([info, pos])

