import pygame, sys
import random
pygame.init()

score = 0

# цвета
BLACK = (0, 0, 0)
YELLOW = (230, 230, 140)
GREEN = (0, 90, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SPEED = 10
changeX = 0

# настройки главного экрана
WIDTH = 1920
HEIGHT = 1080
mainScreen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
mainScreenColor = WHITE
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

# block2 = pygame.Surface((100, 100))
manstand = pygame.image.load('c_stand.png')
manjump = pygame.image.load('c_jump.png')
manr = pygame.image.load('c_walk.png')
manl = manr.copy()
manl = pygame.transform.flip(manl, True, False)

man = manstand
manrect = manr.get_rect()
manrect.bottom = 1050
manrect.left = 50

platform = pygame.image.load('кирпич шоколадка small.png')

c = pygame.font.Font(None, 60)

coinblock = pygame.image.load('f2.png')
# platform = pygame.Surface((250, 100))
coin = coinblock
# массив rect'ов для еды
coins = [ ]

# массив rect'ов для еды
platforms = [
    # platform.get_rect(left = 0, bottom = HEIGHT - 200)
]

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
            if not jump and event.key == pygame.K_SPACE:
                jump = True
                jumpCount = jumpMax
                onGround = False
                onPlatform = False

    platforms = []

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '*':
                platformrect = platform.get_rect()
                platformrect.x = 30 * j
                platformrect.y = 30 * i
                platforms.append(platformrect)
                mainScreen.blit(platform, platformrect)

    manrect_old = manrect.copy()

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


    if keys[pygame.K_ESCAPE]:
        break

    manrect.x += changeX

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

    # заливаем главный фон черным цветом
    mainScreen.fill(mainScreenColor)

    # рисуем блок еды
    for platformrect in platforms:
        mainScreen.blit(platform, platformrect)

    # рисуем змею
    mainScreen.blit(man, manrect)

    #создание ректа блока еды
    if len(coins) == 0:
        for i in range(10):
            coinrect = coinblock.get_rect()
            coinrect.centerx = random.randint(50, WIDTH-50)
            coinrect.centery = random.randint(50, HEIGHT-50)
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
            jumpMax = 30
    
    #рисуем блок еды
    for coinrect in coins: 
        mainScreen.blit(coinblock, coinrect)

    
    mainScreen.blit(man, manrect)
    sc_text = c.render('Собрано рыбок: ' + str(score), 1, RED)
    mainScreen.blit(sc_text, (0,0))

    pygame.display.flip()
    clock.tick(FPS)