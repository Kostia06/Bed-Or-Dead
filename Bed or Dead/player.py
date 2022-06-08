import pygame as pg 
import random as r
import time
import math as m
import os
particles = []
class Player(pg.sprite.Sprite):
    def __init__(self, pos,group):
        super().__init__(group[0])
        self.obstacles = group[1]
        self.pos = pos
        self.group = group[0]
        self.size = [24, 24]
        self.rect = pg.Rect(self.pos,self.size)
        self.images = {'stand':"./Img/Player/stand.png", 'jump':'./Img/Player/jump.png', 'walking':['./Img/Player/walking_1.png', './Img/Player/walking_2.png']}
        self.direction = pg.Vector2()
        self.speed = 3.5
        self.image = pg.image.load(os.path.join(f'{self.images["stand"]}')).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.rect.w, self.rect.h))
        self.angles = []
        self.prev_time = time.perf_counter()
        self.animation = 0
        self.img = self.image
        self.fear = 0
        self.work = False
    def input(self):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed(), pg.mouse.get_pos()
        x = int(self.rect.centerx) in range(mouse[1][0]-13,mouse[1][0]+13, 1)
        y = int(self.rect.centery) in range(mouse[1][1]-13,mouse[1][1]+13, 1)
        if mouse[0][0] == 1 and self.work:
            self.direction = self.get_distance_direction()[1]
            angle =m.atan2(mouse[1][1] - self.rect.y, mouse[1][0] -self.rect.x) 
            if not x and self.work or not y and self.work:
                self.walk()
                self.direction.x = m.cos(angle) * self.speed
                self.direction.y = m.sin(angle) * self.speed 
            else:
                self.direction = pg.Vector2()
                self.image = pg.image.load(os.path.join(f'{self.images["stand"]}')).convert_alpha()
                self.image = pg.transform.scale(self.image, (self.rect.w, self.rect.h))
        else:
            self.direction = pg.Vector2()
            self.image = pg.image.load(os.path.join(f'{self.images["stand"]}')).convert_alpha()
            self.image = pg.transform.scale(self.image, (self.rect.w, self.rect.h))


        if self.work:
            self.d_x, self.d_y = self.rect.centerx - mouse[1][0], self.rect.centery - mouse[1][1]
            self.angle = m.degrees(m.atan2(-self.d_y, self.d_x)) - 90 #right = 0, up = 90, left = 180, down = 270
            self.img = self.rotate(self.image, self.angle)[0]
    def walk(self):
        if int(self.animation) == 3:
            self.image =pg.image.load(os.path.join(f'{self.images["walking"][0]}')).convert_alpha()
            self.image = pg.transform.scale(self.image, (self.rect.w, self.rect.h))
        if int(self.animation) == 6:
            self.image =pg.image.load(os.path.join(f'{self.images["walking"][1]}')).convert_alpha()
            self.image = pg.transform.scale(self.image, (self.rect.w, self.rect.h))
            self.animation = 0
        self.animation += 0.5
    def move(self,speed):
        now = time.perf_counter()
        dt = now - self.prev_time
        self.prev_time = now

        self.rect.x += self.direction.x * dt * 40
        self.collision('x')
        self.rect.y += self.direction.y  * dt * 40
        self.collision('y')
        self.rect.center = self.rect.center
    def collision(self, dir):
        if dir == 'x':
            for sprite in self.obstacles:
                if  self.rect.colliderect(sprite.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right


        if dir == 'y':
            for sprite in self.obstacles:
                if  self.rect.colliderect(sprite.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
    def get_distance_direction(self):
        mouse = pg.mouse.get_pos()
        enemy_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(mouse)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pg.math.Vector2()

        return (distance,direction)
    def rotate(self, img, angle):
        img = pg.transform.rotate(img, angle)
        rect = img.get_rect(topleft = (self.rect.x, self.rect.y))
        return img, rect
    def scale(self, img, scale):
        img = pg.transform.scale(img, scale)
        rect = img.get_rect(topleft = (self.rect.x, self.rect.y))
        return img, rect
    def update_groups(self, group):
        super().__init__(group[0])
        self.obstacles = group[1]
    def update(self, screen):
        self.input()
        self.move(self.speed)
        self.rect.w += 0.1
        self.rect.h += 0.1
class Particle():
    def __init__(self, pos, velocity, shape, color,time):
        self.pos = pg.Vector2()
        self.velocity = pg.Vector2()
        self.pos.x, self.pos.y = pos
        self.velocity.x, self.velocity.y = velocity
        self.r = shape[0]
        self.shape = shape[1]
        self.color = color
        self.grav_scale = time[2]
        self.time = r.randrange(time[0], time[1])
        self.grav = r.randrange(5, 10)
        particles.append(self)
    def draw(self, screen):
        self.time -= 1
        if self.grav_scale != None:
            self.grav -= self.grav_scale
            self.pos.x += self.velocity.x 
            self.pos.y += self.velocity.y + self.grav
        else:
            self.pos.x += self.velocity.x
            self.pos.y += self.velocity.y
        p = (self.pos[0] + r.randrange(self.r * -1, self.r), self.pos[1] + r.randrange(self.r * -1, self.r))
        a = (self.pos[0] + r.randrange(self.r * -1, self.r), self.pos[1] + r.randrange(self.r * -1, self.r))
        b =(self.pos[0] + r.randrange(self.r * -1, self.r), self.pos[1] + r.randrange(self.r * -1, self.r))
        self.points = [(self.pos[0], self.pos[1]), p,b, a]
        if self.shape == 'c':
            pg.draw.circle(screen, self.color, (self.pos), self.r)
            pg.draw.circle(screen, 'black', (self.pos), self.r, 1)
        elif self.shape == 'r':
            pg.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.r, self.r))
            pg.draw.rect(screen, 'black', (self.pos[0], self.pos[1], self.r, self.r), 1)
        elif self.shape == 'p':
            pg.draw.polygon(screen, self.color,self.points)
            pg.draw.polygon(screen, 'black',  self.points, 1)
        if self.time <= 0:
            particles.remove(self)

