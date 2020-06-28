import random
import math

import pygame

from pygame import mixer
#initializing pygame
pygame.init()

#creating screen
screen_dimen = (800,600) #screen dimensions

screen=pygame.display.set_mode(screen_dimen)

#Background
background=pygame.image.load('space.jpg')

#window name and icon
pygame.display.set_caption('Space_Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Player(spacaship) 
player_image=pygame.image.load('spaceship2.png')
px=340
py=460
playerX_change=0

#Enemy(Alien)
enemy_image=[]
ex=[]
ey=[]
enemyX_change=[]
enemyY_change=[]

num=6  
for i in range(num):
    enemy_image.append(pygame.image.load('alien2.png'))
    ex.append(random.randint(0,770))
    ey.append(random.randint(43,200))
    enemyX_change.append(2)
    enemyY_change.append(0)


#Bullet
    #Ready - ready to be fired (you can fire now)
    #Fire - Firing i.e. moving in screen(you cannot fire now)

bullet=pygame.image.load('bullet.png')
bx=400
by=460
bulletX_change=0
bulletY_change=5
bullet_state='ready'

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bullet,(x+16,y+10))

# Explosion

explosion=pygame.image.load('explosion.png')
explosion2=pygame.image.load('explosion2.png')
explosion3=pygame.image.load('explosion3.png')

def explosions(x,y):
    screen.blit(explosion,(x,y))
    screen.blit(explosion2,(x,y))
    screen.blit(explosion3,(x,y))
    

#score

score=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10
score_value=0
def show_score(x,y):
    score=font.render('Score : '+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))


#Game Over

over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    game_over=over_font.render('GAME OVER!',True,(255,0,0))
    screen.blit(game_over,(200,250))
    

def player(x,y):
    screen.blit(player_image,(x,y))


def enemy(x,y,i):
    screen.blit(enemy_image[i],(x,y))


def isCollision(ex, ey, bx, by):
    distance = math.sqrt(math.pow(ex - bx, 2) + (math.pow(ey - by, 2)))
    if distance < 27:
        return True
    else:
        return False
        


###Game Loop############################################################################

running=True
while running:

    #color of the window
    screen.fill((0,0,0))
    #Background Image drawing on screen
    screen.blit(background,(0,0))
    #for quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        #if checking in event.type is left or right key is pressed continuously
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-4
            if event.key == pygame.K_RIGHT:
                playerX_change=4
            if event.key == pygame.K_SPACE:
                if bullet_state=='ready':
                    bulletSound=mixer.Sound('laser.wav')
                    bulletSound.play()
                    bx=px                #get current x-cordinate of spaceship
                    fire_bullet(bx,by)

        if event.type==pygame.KEYUP:          #key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change=0 

        
    

    #the spaceship should not go beyond the limits of the window 
    px+=playerX_change
    if px<=0:
        px=0
    elif px>=730:
        px=730

    #Enemy movement
    for i in range(num):

        #Game over
        if ey[i]>460:
            for j in range(num):
                ey[j]=2000
            game_over_text()
            break
    
        ex[i]+=enemyX_change[i]
        ey[i]+=enemyY_change[i]
        if ex[i]<=0:
            enemyX_change[i]=1
            enemyY_change[i]=0.09
        elif ex[i]>=720:
            enemyX_change[i]=-1
            enemyY_change[i]=0.09

        # Collision
        collision = isCollision(ex[i], ey[i], bx, by)
        if collision:
            explosions(ex[i],ey[i])
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            by = 480
            bullet_state = "ready"
            score_value += 1
            ex[i] = random.randint(0, 736)
            ey[i] = random.randint(50, 150)

        enemy(ex[i],ey[i],i)

    #Bullet Movement
    if by <= 0:
        by = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bx, by)
        by -= bulletY_change

    
            
          

    player(px,py)
    show_score(textX,textY)  


    pygame.display.update()

    
