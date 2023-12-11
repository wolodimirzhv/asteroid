from pygame import *
from random import randint, uniform, choice
from time import time as timer

w, h = 700, 500



window = display.set_mode((w, h))
clock = time.Clock()

game = True
finish = False

background = image.load("galaxy2.png")
class GameSprite(sprite.Sprite):
    def __init__(self, pImage, x, y, sizeX, sizeY, speed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Button(sprite.Sprite):
    def __init__(self, pImage, x, y, sizeX, sizeY):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >=0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= w-65:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx-7,self.rect.top,15,30,15)
        bullets.add(bullet)

bullets = sprite.Group()
ship = Player("rocket.png",0,400,100,100,8)

score = 0
lost = 0


        

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        global hearts
        if self.rect.y > h:
            try:
                hearts.pop()
            except:
                pass
            self.rect.x = randint(0,600)
            self.rect.y = randint(-60,-40)
            lost += 1

enemis = sprite.Group()
def creat_enemis():
    for i in range(6):
        images = ["asteroid.png","ufo.png"]
        enemy_image = choice(images)
        enemy = Enemy(enemy_image,randint(0,600),randint(-60,-40),50,50,randint(1,2))
        enemis.add(enemy)
creat_enemis()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.15)

fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.15)

win_sound = mixer.Sound("win.ogg")
win_sound.set_volume(0.15)

font.init()
mainfont = font.Font("mainfont.ttf",40)
mainfont2 = font.Font("mainfont.ttf",80)

num_fire = 0
reload_timer = False

hearts = []

def create_hearts():

    x = 350
    for i in range(10):
        heart = GameSprite("heart.png",x,10,30,30,0)
        hearts.append(heart)
        x += 30
create_hearts()

start = Button('start.png',255,255,195,80)
menu = True 
finish = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x,y = e.pos
                if start.rect.collidepoint(x,y):
                    menu = False
                    finish = False


        if e.type == KEYDOWN:
            if e.key == K_RCTRL:
                if reload_timer == False and num_fire < 20:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                elif num_fire >= 20 and reload_timer == False:
                    reload_timer = True
                    reload_start = timer()
            if e.key == K_ESCAPE and finish == True:
                for enemy in enemis:
                    enemis.remove(enemy)
                creat_enemis()
                create_hearts()
                score = 0
                lost = 0
                finish = False
#################################################
        
    if menu:
        window.blit(background,(0,0))
        start.draw()
    
    if not finish:
        window.blit(background,(0,0))

        score_text = mainfont.render("SCORE: " + str(score),True,(0,255,20))
        lost_text = mainfont.render("LOST: " + str(lost),True,(220,10,20))

        window.blit(score_text,(5,5))
        window.blit(lost_text,(5,50))


        for heart in hearts:
            heart.draw()


        ship.draw()
        ship.update()

        bullets.update()
        bullets.draw(window)
        

        collides = sprite.groupcollide(enemis,bullets,True,True)
        for c in collides:
            images = ["asteroid.png","ufo.png"]
            enemy_image = choice(images)
            enemy = Enemy(enemy_image,randint(0,600),randint(-60,-40),50,50,randint(1,2))
            enemis.add(enemy)
            score += 1
        
        if reload_timer:
            reload_timer = timer()
            if reload_timer - reload_start < 3:
                reload_text = mainfont.render("Reloading ",True,(220,10,20))
                window.blit(reload_text,(230,200))
            else:
                num_fire = 0 
                reload_timer = False
        
        if score == 20:
            finish = True
            RELOADING_text = mainfont2.render("WIN", True, (0, 255, 0))
            RESTART_TEXT = mainfont.render("FOR RESTART ENTER THE ESC", True, (0, 255, 0))
            window.blit(RELOADING_text,(250,200))
            window.blit(RESTART_TEXT,(10,450))
            win_sound.play()
            
       
        if len(hearts) == 0:
            lost_text = mainfont.render("you died",True,(220,10,20))
            window.blit(lost_text,(250,250))
            finish = True
        enemis.update()
        enemis.draw(window)

    display.update()
    clock.tick(60)
