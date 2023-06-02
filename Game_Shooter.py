#Створи власний Шутер!
from pygame import *
from random import randint

score = 0
lost = 0

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<0:
            self.kill() 

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.x, self.rect.y,20,40,50)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y +=5
        if self.rect.y >500:
            self.rect.x = randint(80, 600)
            self.rect.y = 0
            lost+=1

window = display.set_mode((700, 500))

display.set_caption("Шутер")

background = transform.scale(image.load("galaxy.jpg"),(700, 500))

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (225, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

game = True
clock = time.Clock()
FPS = 60
finish = False

ship = Player("rocket.png", 5,400,60,100,10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, 600),-80,60,60, randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()     

while game:  
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire.play()
    if finish!=True:
        window.blit(background,(0, 0))
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.reset()
        monsters.draw(window)
        monsters.update()
        ship.update()
        bullets.draw(window)
        bullets.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, 600), -40, 60, 60, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost>=3:
            finish=True
            window.blit(lose, (200, 200))
        if score>=10:
            finish=True
            window.blit(win, (200, 200))

    display.update()
    time.delay(50)
    clock.tick(FPS)
