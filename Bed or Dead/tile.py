import pygame as pg 
import os
class Tile(pg.sprite.Sprite):
    def __init__(self ,pos, size,img, group):
        super().__init__(group)

        self.rect = pg.Rect(pos, size)
        self.img = pg.image.load(os.path.join(f'{img}')).convert_alpha()
        self.img = pg.transform.scale(self.img, (self.rect.w, self.rect.h))
    def update(self, surf):
        surf.blit(self.img, (self.rect))

class Carpet(pg.sprite.Sprite):
    def __init__(self, pos, size, img,group):
        super().__init__(group)

        self.rect = pg.Rect(pos, size)
        self.img = pg.image.load(os.path.join(f'{img}')).convert_alpha()
        self.img = pg.transform.scale(self.img, (self.rect.w, self.rect.h))
    def update(self, surf):
        surf.blit(self.img, (self.rect))

class Door(pg.sprite.Sprite):
    def __init__(self, pos,size, group):
        super().__init__(group)
        self.rect = pg.Rect(pos,size)
        self.player = None
        self.animation = None
        self.collide = False
    def draw(self, screen, darkness):
        pg.draw.rect(screen, (255, 255,0), self.rect, 0, 6)
        pg.draw.rect(darkness, (255, 255, 0, 50), (self.rect.x-15, self.rect.y-15, self.rect.w+30, self.rect.h+30),0,12)
        if self.player != None :
            if self.rect.colliderect(self.player):
                self.collide = True
                self.animation()
            else:
                self.collide = False

class Bed(pg.sprite.Sprite):
    def __init__(self, pos, size,img, group):
        super().__init__(group)
        self.player = None
        self.level_change = None
        self.rect= pg.Rect(pos, size)
        self.img = pg.image.load(os.path.join(f'{img}')).convert_alpha()
        self.img = pg.transform.scale(self.img, (self.rect.w, self.rect.h))
        self.work = True 
    def update(self, screen):
        screen.blit(self.img, self.rect)
        if self.player != None:
            if self.rect.colliderect(self.player.rect) and self.work:
                self.level_change()
                self.work = False