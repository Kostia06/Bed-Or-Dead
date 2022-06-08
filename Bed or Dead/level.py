
from player import Player
import pygame as pg
from tile import Bed, Tile, Carpet, Door
from enemy import Enemy, Spirate, Blast, Mirror
from setting import Map,name
import json

obstacle_sprites = pg.sprite.Group()
visible_sprites = pg.sprite.Group()
objects ={
    'Player':{'name':'Player', 'size': (32,32), 'img': './Img/Tiles/player.png', 'groups':'[visible_sprites, obstacle_sprites]'},
    'Table_1': {'name': 'Tile', 'size': (64,140), 'img':'./Img/Tiles/table_1.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Table_2': {'name': 'Tile', 'size': (140,64), 'img':'./Img/Tiles/table_2.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Table_3': {'name': 'Tile', 'size': (40,40), 'img':'./Img/Tiles/small_table.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Closet': {'name': 'Tile', 'size': (64,100), 'img':'./Img/Tiles/closet.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Carpet': {'name': 'Carpet', 'size': (50, 80), 'img':'./Img/Tiles/carpet.png', 'groups': '[visible_sprites]'},
    'Spirate': {'name': 'Spirate', 'size': (30,30), 'img':'./Img/Ghost/red.png', 'groups': '[visible_sprites]'},
    'Ghost': {'name': 'Ghost', 'size': (30, 30), 'img':'./Img/Ghost/blue.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Blast': {'name': 'Blast', 'size': (30, 30), 'img':'./Img/Ghost/green.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Door_Left':{'name':'Door','size': (90, 30), 'img':'./Img/Tiles/yellow.png', 'groups': '[visible_sprites]' },
    'Door_right':{'name':'Door','size': (30, 90), 'img':'./Img/Tiles/yellow.png', 'groups': '[visible_sprites]' },
    'Bed_1': {'name': 'Bed', 'size': (50,100), 'img':'./Img/Tiles/bed_1.png', 'groups': '[visible_sprites]'},
    'Bed_2': {'name': 'Bed', 'size': (100,50), 'img':'./Img/Tiles/bed_2.png', 'groups': '[visible_sprites]'},
    'Wall_1': {'name': 'Tile', 'size': (200, 40), 'img':'./Img/Tiles/wall_1.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Wall_2': {'name': 'Tile', 'size': (40, 200), 'img':'./Img/Tiles/wall_2.png', 'groups': '[visible_sprites, obstacle_sprites]'},
    'Block': {'name': 'Tile', 'size': (40, 40), 'img':'./Img/Tiles/block.png', 'groups': '[visible_sprites, obstacle_sprites]'},
   
}
class Level():
    def __init__(self, screen):
        self.map = Map('d', 'p', screen)
        self.map.mapping(objects)
        self.screen = screen
        self.player =Player((-100, -100),[visible_sprites, obstacle_sprites])
        self.enemy = []
        self.door = []
        self.bed = []
        self.room = 0
        self.level = 1
        self.current_level = 1
        self.name = f'Levels/{self.current_level}/{self.room}.txt'
    def save(self):
        self.map.save()
    def new_level(self):
        self.enemy.clear()
        self.door.clear()
        self.bed.clear()
        visible_sprites.empty()
        obstacle_sprites.empty()
        self.create_map()
    def lose(self):
        self.room = 0
        self.enemy.clear()
        self.bed.clear()
        self.door.clear()
        visible_sprites.empty()
        obstacle_sprites.empty()
        self.player =Player((-100, -100),[visible_sprites, obstacle_sprites])
    def create_map(self):
        self.room += 1
        self.name = f'Levels/{self.current_level}/{self.room}.txt'
        try: 
            with open(self.name) as datas:
                objects = json.load(datas)
            for _, i in enumerate(objects):
                if i[0]['name'] == 'Player':
                    self.player.rect.x, self.player.rect.y = i[1]
                    self.player.update_groups(eval(i[0]['groups']))
                elif i[0]['name'] == 'Tile':
                    Tile((i[1]), i[0]['size'],i[0]['img'] ,eval(i[0]['groups']))
                elif i[0]['name'] == 'Carpet':
                    Carpet((i[1]), i[0]['size'],i[0]['img'] ,eval(i[0]['groups']))
                elif i[0]['name'] =='Ghost':
                    self.enemy.append(Enemy((i[1]),eval(i[0]['groups'])))
                elif i[0]['name'] =='Spirate':
                    self.enemy.append(Spirate((i[1]),eval(i[0]['groups'])))
                elif i[0]['name'] =='Blast':
                    self.enemy.append(Blast((i[1]),eval(i[0]['groups'])))
                elif i[0]['name'] =='Door':
                    self.door.append(Door((i[1]),i[0]['size'],eval(i[0]['groups'])))
                elif i[0]['name'] =='Bed':
                    self.bed.append(Bed(i[1],i[0]['size'],i[0]['img'],eval(i[0]['groups'])))
        except  FileNotFoundError:
            pass
    def run(self):
        visible_sprites.update(self.screen)
        if self.player != None:
            self.screen.blit(self.player.img, (self.player.rect))

