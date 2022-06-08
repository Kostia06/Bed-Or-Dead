from tkinter.tix import Tree
import pygame  as pg
import os 
import math as m
import random as r
particles = []
class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups[0])
        print(groups)
        self.obstacles = groups[1]
        self.rect = pg.Rect(pos[0], pos[1], 25,25)
        self.player= None
        self.direction = None
        self.speed = 2
        self.work = False
        self.first_triangle = [0, 120, 240]
        self.first_pos = []
        self.list = []
        self.second_triangle = [0, 120, 240]
        self.second_pos =[]
        self.direction= pg.Vector2(r.choice([-1,1]), r.choice([-1,1]))
        self.offset = 0
        self.glow = 50
        self.num = 1
        self.build = False
    def update(self,screen: pg.display):
        if self.work and self.player != None:
            if 1 == r.randint(1,50):
                self.direction.x = r.choice((-1,0,1))
                self.direction.y = r.choice((-1,0,1))
            if self.rect.x > screen.get_size()[0] -self.rect.w or 0 > self.rect.x:
                self.direction.x *= -1
            if self.rect.y > screen.get_size()[1] - self.rect.h or 0 > self.rect.y:
                self.direction.y *= -1
            self.move(self.speed)
        if self.build:
            self.work = True
    def draw(self, screen, darkness):
        pg.draw.circle(darkness, (139, 174, 203, self.glow-15), self.rect.center, 45)
        pg.draw.circle(darkness, (139, 174, 203, self.glow), self.rect.center, 30)
        pg.draw.circle(screen, (139, 174, 203), self.rect.center, 2)

        for i in self.first_triangle:
            self.first_pos.append(pg.Vector2(self.rect.center) + pg.Vector2(1,0).rotate( i-90 + self.offset) * 25)
        pg.draw.polygon(darkness, (139, 174, 203, 120), self.first_pos)
        for i in self.first_pos:
            Particle(self.list,(i), (r.choice((-0.3,0.3)),r.choice((-0.3,0.3))), (1, 'c'), (139, 174, 203),(5, 10, None) )
        self.first_pos.clear()

        for i in self.second_triangle:
            self.second_pos.append(pg.Vector2(self.rect.center) + pg.Vector2(1,0).rotate( i+ 90 + self.offset) * 25)
        pg.draw.polygon(darkness, (139, 174, 203, 120), self.second_pos,)
        for i in self.second_pos:
            Particle(self.list,(i), (r.choice((-0.3,0.3)),r.choice((-0.3,0.3))), (1, 'c'), (139, 174, 203),(5, 10, None) )
        self.second_pos.clear()
        for i in self.list:
            i.draw(screen, darkness, 50)
        self.offset += 8
        if self.glow > 50 or self.glow < 20:
            self.num *= -1
        self.glow += self.num
    def move(self,speed):
        if self.direction != None:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
                self.rect.x += self.direction.x * speed 
                self.collision('x')
                self.rect.y += self.direction.y * speed
                self.collision('y')
                self.rect.center = self.rect.center
        if self.rect.colliderect(self.player.rect):
            self.player.fear += 3
    def collision(self, dir):
        if dir == 'x':
            for sprite in self.obstacles:
                if  self.rect.colliderect(sprite.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                        self.direction.x = -1
                    elif self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                        self.direction.x = 1


        if dir == 'y':
            for sprite in self.obstacles:
                if  self.rect.colliderect(sprite.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = -1
                    elif self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 1
    def get_player_distance_direction(self, player):

        enemy_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(player.rect.center)
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

class Spirate(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.group = groups
        self.player = None
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        self.num = 0
        self.circle = 1
        self.color =  [0,0]
        self.work = False
        self.color_self = None
        self.appear = 0
        self.build = False
        self.red = 200
        self.red_num = 1
        self.random = r.randint(5, 12)
        self.list = []
    def update(self, screen):
        if self.work and self.player != None:
            self.color_self = 'red'
            self.circle += 1.5
            self.color[0] += 0.1
            self.color[1] += 0.5
            if self.circle > 250:
                self.circle = 0
                self.color = [0,0]
                self.random = r.randint(5, 12)
        elif self.build:
            if self.appear < 254:
                self.appear += 2
            else:
                self.work = True
    def draw(self, screen, darkness):
        if self.work:
            try:
                pg.draw.circle(screen,'black', (self.rect.center), 10)
                pg.draw.circle(darkness, (self.red,0,0,50), (self.rect.center), 18)
                pg.draw.circle(darkness, (255,255,255,50 - self.color[0]), (self.rect.center), 18, 4)
                points = self.get_points(self.random, self.rect.center, self.circle)
                for i in points:
                    rect = pg.Rect(i[0] + 1, i[1] + 1, 2, 2)
                    try:
                        pg.draw.circle(darkness, (255,0,0,50 - self.color[0]), (i), 8)
                        pg.draw.circle(darkness, (255,0,0,255 - self.color[1]), (i), 3)
                        Particle(self.list,(i), (r.choice((-0.3,0.3)),r.choice((-0.3,0.3))), (1, 'c'), (255,0,0),(5, 10, None) )
                    except:
                        pass
                    if rect.colliderect(self.player.rect):
                        self.player.fear += 3
                if self.work:
                    if self.red > 254 or self.red_num < 100:
                        self.red_num *= -1
                self.red += self.red_num
                for i in self.list:
                    i.draw(screen,darkness, self.color[0])
            except:
                pass
        pg.draw.circle(darkness,(self.red, 0,0, self.appear), (self.rect.center), 10)
    def get_points(self, num, pos, radius):
        p = pg.Vector2(pos)
        v = pg.Vector2(0, -1)
        return [p + v.rotate(d) * radius for d in range(0, 360, 360 // num)]

class Blast(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.rect = pg.Rect(pos[0], pos[1], 15, 15)
        self.player = None
        self.work = False
        self.build = False
        self.points = []
        self.focus = 1
        self.focus_color = 50
        self.list = []
    def update(self, screen):
        for i  in self.get_points(3, self.rect.center, 20):
            self.points.append(i)
        if self.build:
            self.work = True
    def draw(self, screen, darkness):
        if len(self.points) > 2:
            pg.draw.circle(darkness,(144, 238, 143, 50), self.rect.center, 25 )
            pg.draw.polygon(screen, (144, 238, 143), self.points)
            pg.draw.polygon(screen, (10,10,10), self.points, 5)
            self.points.clear()
            if self.get_player_distance_direction(self.player)[0] < 150:
                pg.draw.line(darkness, (144, 238, 143,self.focus_color), (self.rect.center), (self.player.rect.center), int(self.focus))
                pg.draw.circle(darkness, (144, 238, 143,self.focus_color),self.player.rect.center, self.focus )
                Particle(self.list,(self.player.rect.center), (r.choice((-1,1)),r.choice((-1,1))), (self.focus - 10, 'c'), (144, 238, 143),(5, 10, None) )
                if self.focus < 15:
                    self.focus += 0.1
                    self.focus_color += 1
                elif self.work:
                    self.player.fear += 2
            else:
                self.focus = 1
                self.focus_color = 50
        for i in self.list:
            i.draw(screen, darkness,50)      
    def get_points(self, num, pos, radius):
        p = pg.Vector2(pos)
        v = pg.Vector2(0, -1)
        return [p + v.rotate(d) * radius for d in range(0, 360, 360 // num)]

    def get_player_distance_direction(self, player):

        enemy_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pg.math.Vector2()
        return (distance,direction)

class Mirror(pg.sprite.Sprite):
    def __init__(self, pos, door,groups):
        super().__init__(groups)
        self.obstacles = groups[1]
        self.door = door
        self.rect  = pg.Rect(pos[0], pos[1], 15, 15)
        self.points = []
        self.point = pg.Rect(pos[0], pos[1], 10, 10)
        self.direction= pg.Vector2(r.choice([-1,1]), r.choice([-1,1])) 
        self.range = []
        self.build = False
        self.player = None
    def update(self,screen):
        if self.build:
            if len(self.points) <= 5:
                self.move()
            elif len(self.points) > 5:
                self.points.pop()
    def move(self):
        self.point.x += self.direction.x * 5
        self.collision('x')
        if self.point.x < 2 or self.point.x > 598:
            self.direction.x *= -1
        self.point.y += self.direction.y * 5
        self.collision('y')
        if self.point.y < 2 or self.point.y > 398:
            self.direction.y *= -1
        self.point.center = self.point.center
    def collision(self, dir):
        if dir == 'x':
            for sprite in self.obstacles:
                if  self.point.colliderect(sprite.rect) and sprite.rect != self.rect:
                    if self.direction.x > 0: # moving right
                        self.point.right = sprite.rect.left
                        self.direction.x = -1
                    elif self.direction.x < 0: # moving left
                        self.point.left = sprite.rect.right
                        self.direction.x = 1
                    self.points.append(sprite.rect.clip(self.point))
            for sprite in self.door:
                if  self.point.colliderect(sprite.rect) and sprite.rect != self.rect:
                    if self.direction.x > 0: # moving right
                        self.point.right = sprite.rect.left
                        self.direction.x = -1
                    elif self.direction.x < 0: # moving left
                        self.point.left = sprite.rect.right
                        self.direction.x = 1
                    self.points.append(sprite.rect.clip(self.point))


        if dir == 'y':
            for sprite in self.obstacles:
                if  self.point.colliderect(sprite.rect) and sprite.rect != self.rect:
                    if self.direction.y > 0: # moving down
                        self.point.bottom = sprite.rect.top
                        self.direction.y = -1
                    elif self.direction.y < 0: # moving up
                        self.point.top = sprite.rect.bottom
                        self.direction.y = 1
                    self.points.append(sprite.rect.clip(self.point))
            for sprite in self.door:
                if  self.point.colliderect(sprite.rect) and sprite.rect != self.rect:
                    if self.direction.y > 0: # moving down
                        self.point.bottom = sprite.rect.top
                        self.direction.y = -1
                    elif self.direction.y < 0: # moving up
                        self.point.top = sprite.rect.bottom
                        self.direction.y = 1
                    self.points.append(sprite.rect.clip(self.point))
    def draw(self, screen, darkness):
        pg.draw.circle(screen,(255, 16, 148), (self.rect.center), 15 )
        pg.draw.circle(darkness,(255, 16, 148, 50), (self.rect.center), 30 )
        if len(self.points) == 5:
            for i in range(4):
                a = [(self.points[i].x, self.points[i].y), (self.points[i+1].x ,self.points[i+1].y)]
                pg.draw.line(screen, (255, 0, 0), a[0], a[1], 5)
                pg.draw.line(darkness, (255, 0, 0, 50), a[0], a[1], 10)
                x = range(a[0][0], a[1][0], 1)
                y = range(a[0][1], a[1][1], 1)
                if self.player.rect.centerx in x or self.player.rect.centery in y:
                    self.player.fear += 2
        else:
            pg.draw.rect(screen, 'red', self.point)
            pg.draw.rect(darkness, (255,0,0,50), self.point)
        
class Particle():
    def __init__(self,group, pos, velocity, shape, color,time):
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
        self.group = group
        self.group.append(self)
    def draw(self, screen, darkness, num):
        self.time -= 1
        if self.grav_scale != None:
            self.grav -= self.grav_scale
            self.pos.x += self.velocity.x 
            self.pos.y += self.velocity.y + self.grav
        else:
            self.pos.x += self.velocity.x
            self.pos.y += self.velocity.y
        if self.shape == 'p':
            p = (self.pos[0] + r.randrange(self.r * -1, self.r), self.pos[1] + r.randrange(self.r * -1, self.r))
            a = (self.pos[0] + r.randrange(self.r * -1, self.r), self.pos[1] + r.randrange(self.r * -1, self.r))
            b =(self.pos[0] + r.randrange(self.r * -1, self.r), self.pos[1] + r.randrange(self.r * -1, self.r))
            self.points = [(self.pos[0], self.pos[1]), p,b, a]
        if self.shape == 'c':
            pg.draw.circle(screen, self.color, (self.pos), self.r)
            pg.draw.circle(darkness, (self.color[0], self.color[1], self.color[2], num), (self.pos), self.r + 5)
        elif self.shape == 'r':
            pg.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.r, self.r))
            pg.draw.rect(darkness, (self.color, num), (self.pos[0], self.pos[1], self.r + 5, self.r + 5))
        elif self.shape == 'p':
            pg.draw.polygon(screen, self.color,self.points)
        if self.time <= 0:
            self.group.remove(self)
