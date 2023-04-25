import pygame, sys
import random
pygame.init()

score = 0
score2 = 0

# цвета
BLACK = (0, 0, 0)
YELLOW = (230, 230, 140)
GREEN = (0, 90, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SPEED = 10
changeX = 0
changeX2 = 0

# настройки главного экрана
WIDTH = 1920
HEIGHT = 1080
mainScreen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
mainScreenColor = pygame.image.load("fon2.png")
pygame.display.set_caption("Моя игра")

# число кадров в секунду
FPS = 60
clock = pygame.time.Clock()

vel = 5
jump = False
jumpCount = 0
jumpMax = 25
onGround = True
onPlatform = False
jump2 = False
jumpCount2 = 0
jumpMax2= 25
onGround2 = True
onPlatform2 = False

# block2 = pygame.Surface((100, 100))
manstand = pygame.image.load('c1_stand.png')
manjump = pygame.image.load('c1_jump.png')
manr = pygame.image.load('c1_walk.png')
manl = manr.copy()
manl = pygame.transform.flip(manl, True, False)

man = manstand
manrect = manr.get_rect()
manrect.bottom = 1050
manrect.left = 50


manstand2 = pygame.image.load('c1_stand.png')
manjump2 = pygame.image.load('c1_jump.png')
manr2 = pygame.image.load('c1_walk.png')
manl2 = manr2.copy()
manl2 = pygame.transform.flip(manl2, True, False)

man2 = manstand2
manrect2 = manr2.get_rect()
manrect2.bottom = 1050
manrect2.left = 1600

platform = pygame.image.load('кирпич шоколадка small.png')

c = pygame.font.Font(None, 60)
c2 = pygame.font.Font(None, 100)

coinblock = pygame.image.load('f2.png')
coinblock2 = pygame.image.load('f2.png')
# platform = pygame.Surface((250, 100))
coin = coinblock
coin2 = coinblock2
# массив rect'ов для еды
coins = [ ]
coins2 = [ ]

# массив rect'ов для еды
platforms = []
platforms2 = []

map =  [
    '****************************************************************',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*         **************************************               *',
    '*                                                              *',
    '*                                                              *',
    '*                                                      ***     *',
    '****                                                           *',
    '*                                                              *',
    '*                                                              *',
    '*             ******                         ******          ***',
    '*                                                              *',
    '*                                                              *',
    '*                                       *                      *',
    '*                                                              *',
    '*                        *************                         *',
    '*                                                              *',
    '*                                                              *',
    '*          ********                           *******          *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*****                                                      *****',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '*                                                              *',
    '****************************************************************'
]

while 1:
    # проверяем события, которые произошли (если они были)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not jump and event.key == pygame.K_UP:
                jump = True
                jumpCount = jumpMax
                onGround = False 
                onPlatform = False

            if not jump2 and event.key == pygame.K_w:
                jump2 = True
                jumpCount2 = jumpMax2
                onGround2 = False 
                onPlatform2 = False    

    platforms = []
    
    
    # заливаем главный фон черным цветом
    #mainScreen.fill(WHITE)
    mainScreen.blit(mainScreenColor, (0,0))

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '*':
                platformrect = platform.get_rect()
                platformrect.x = 30 * j
                platformrect.y = 30 * i
                platforms.append(platformrect)
                mainScreen.blit(platform, platformrect)

    manrect_old = manrect.copy()
    manrect_old2 = manrect2.copy()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        changeX = -1 * SPEED
        man = manl

    if keys[pygame.K_RIGHT]:
        changeX = SPEED
        man = manr

    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        changeX = 0
        man = manstand

    if jump:
        manrect.y -= jumpCount
        man = manjump

    if jumpCount > -jumpMax or (manrect.bottom < HEIGHT and onGround == False):
        jumpCount -= 1
        man = manjump
    else:
        jump = False
        onGround = True

    if manrect.bottom > HEIGHT:
        manrect.bottom = HEIGHT
        onGround = True
        jump = False
 



    if keys[pygame.K_a]:
        changeX2 = -1 * SPEED
        man2 = manl2

    if keys[pygame.K_d]:
        changeX2 = SPEED
        man2 = manr2

    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        changeX2 = 0
        man2 = manstand2

    if jump2:
        manrect2.y -= jumpCount2
        man2 = manjump2

    if jumpCount2 > -jumpMax2 or (manrect2.bottom < HEIGHT and onGround2 == False):
        jumpCount2 -= 1
        man2 = manjump2
    
    else:
        jump2 = False
        onGround2 = True

    if manrect2.bottom > HEIGHT:
        manrect2.bottom = HEIGHT
        onGround2 = True
        jump2 = False

    if keys[pygame.K_ESCAPE]:
        break

    manrect.x += changeX
    manrect2.x += changeX2

    # проверка столкновения блока еды и змеи
    for platformrect in platforms:
        if manrect.colliderect(platformrect) == True:
            # движемся налево
            if manrect.left < manrect_old.left:
                manrect.x -= changeX
                # manrect.left = platformrect.right

            # движемся направо
            if manrect.right > manrect_old.right:
                manrect.x -= changeX
                # manrect.left = platformrect.right

        if manrect.colliderect(platformrect) == True:
            if manrect.top < manrect_old.top:
                jump = True
                onGround = False
                onPlatform = False
                jumpCount = -1
                manrect.top = platformrect.bottom
            
            # движемся вниз
            if manrect.bottom > manrect_old.bottom:
                jump = False
                onGround = True
                onPlatform = True
                manrect.bottom = platformrect.top

    # Проверка падаем с платформы, потому что вышли с неё
    if onPlatform == True:
        manrect_next = manrect.copy()
        manrect_next.y += 1

        if manrect_next.collidelist(platforms) == -1:
            jump = True
            jumpCount = -1
            onGround = False
            onPlatform = False

    
    for platformrect in platforms:
        if manrect2.colliderect(platformrect) == True:
            # движемся налево
            if manrect2.left < manrect_old2.left:
                manrect2.x -= changeX2
                # manrect.left = platformrect.right

            # движемся направо
            if manrect2.right > manrect_old2.right:
                manrect2.x -= changeX2
                # manrect.left = platformrect.right

        if manrect2.colliderect(platformrect) == True:
            if manrect2.top < manrect_old2.top:
                jump2 = True
                onGround2 = False
                onPlatform2 = False
                jumpCount2 = -1
                manrect2.top = platformrect.bottom
            
            # движемся вниз
            if manrect2.bottom > manrect_old2.bottom:
                jump2 = False
                onGround2 = True
                onPlatform2 = True
                manrect2.bottom = platformrect.top

    # Проверка падаем с платформы, потому что вышли с неё
    if onPlatform2 == True:
        manrect2_next = manrect2.copy()
        manrect2_next.y += 1

        if manrect2_next.collidelist(platforms) == -1:
            jump2 = True
            jumpCount2 = -1
            onGround2 = False
            onPlatform2 = False

    # рисуем блок
    for platformrect in platforms:
        mainScreen.blit(platform, platformrect)

    # рисуем змею
    mainScreen.blit(man, manrect)
    mainScreen.blit(man2, manrect2)

    #создание ректа блока еды
    if len(coins) == 0:
        for i in range(10):
            coinrect = coinblock.get_rect()
            while True:
                coinrect.centerx = random.randint(50, WIDTH-50)
                coinrect.centery = random.randint(50, HEIGHT-50)
                if coinrect.collidelist(platforms) == -1:
                    break
                else:
                    print("Рыба в блоке")
            coins.append(coinrect)
                   
            

    #проверка столкновения блока еды и змеи
    for i in range(len(coins)):
        if manrect.colliderect(coins[i]) == True:
            #foods = [ ]

            coins.pop(i)
            score += 1
            print("Количество набранных очков: " + str(score))
            break
        if score == 10:
            jumpMax == 30
    
    for i in range(len(coins)):
        if manrect2.colliderect(coins[i]) == True:
            #foods = [ ]
            coins.pop(i)
            score2 += 1
            print("Количество набранных очков: " + str(score2))
            break
        if score2 == 10:
            jumpMax == 30
    
    #рисуем блок еды
    for coinrect in coins: 
        mainScreen.blit(coinblock, coinrect)

    
    mainScreen.blit(man, manrect)
    sc_text = c.render('Собрано рыбок: ' + str(score), 1, RED)
    mainScreen.blit(sc_text, (0,0))

    mainScreen.blit(man2, manrect2)
    sc_text = c.render('Собрано рыбок: ' + str(score2), 1, RED)
    mainScreen.blit(sc_text, (1500,0))

    pygame.display.flip()
    clock.tick(FPS)