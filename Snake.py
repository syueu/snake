import pygame, sys, time, random  # 引用函式庫
from pygame.locals import *

# ----------------------------遊戲基本設定------------------------------
# pygame初始化
pygame.init()

# 設定調整程式執行速度之物件
mainClock = pygame.time.Clock()                     

# 設定字型
basicFont = pygame.font.SysFont(None, 48)           

# 設定視窗
WINDOWWIDTH = 405                                   
WINDOWHEIGHT = 450
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('貪食蛇')                  

# 設定玩家物件
player = [(60, 60), (80, 60), (100, 60),(120, 60)]
fruit = [(200, 200)]

# pygame.Rect(X,Y,寬,高)

# 設定軌道物件串列
lines = []  
lines.append(pygame.Rect(5, 55, 1, 390))
lines.append(pygame.Rect(5, 55, 390, 1))
lines.append(pygame.Rect(5, 445, 390, 1))
lines.append(pygame.Rect(395, 55, 1, 391))

# 設定軌道物件串列
wall = []  
wall.append(pygame.Rect(15, 60, 5, 375))
wall.append(pygame.Rect(15, 60, 370, 5))
wall.append(pygame.Rect(15, 435, 370, 5))
wall.append(pygame.Rect(380, 60, 5, 375))

# 隱藏滑鼠游標
pygame.mouse.set_visible(False)  

# ------------------------------變數設定------------------------------

# 以變數設定顏色(R,G,B)
BLACK = (25, 25, 25)               
WHITE = (255, 255, 255)
WALL = (31, 34, 50)
FRUIT = (173, 31, 52)
SNAKE = (48, 95, 69)
BG = (238, 227, 211)

# 文字顏色黑色
TEXTCOLOR = (0, 0, 0)               

# 設定鍵盤移動變數,預設為False
moveLeft = False                    
moveRight = False
moveUp = False
moveDown = False

# 初始速度
MOVESPEED = 0.5                  
FPS = 15

# 初始分數
score = 0                           

# 設定字型
font = pygame.font.SysFont(None, 32)

# 初始方向
nowdir = (0, 20)

# 初始level
level = 1


# ------------------------------函式定義------------------------------
# 設定遊戲失敗訊息
def failed_message():  
    windowSurface.fill(WHITE)
    text = basicFont.render('Score: %s'% (score), True, BLACK, BG)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery
    windowSurface.blit(text, textRect)  

# 設定果實生成
def eat_fruit_message():
    x = random.randrange(8, 17)
    y = random.randrange(8, 20)
    fruits = (20 * x, 20 * y)
    A = pygame.Rect(fruits[0], fruits[1], 20, 20)
    for body in snake[:]:  # 當果實與蛇的身體重疊
        if A.colliderect(body):
            x = random.randrange(3, 17)
            y = random.randrange(5, 20)
            fruits = (20 * x, 20 * y)
            
    fruit.insert(0, fruits)
    fruit.pop(len(fruit) - 1)

# 繪製文字
def drawText(text, font, surface, x, y): 
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)




# ------------------------------主程式------------------------------
while True:  # 遊戲本身是個無窮迴圈
        
    
    snake = []
    for i in range(len(player)):
        snake.append(pygame.Rect(player[i][0], player[i][1], 20, 20))
    point = []
    for i in range(len(fruit)):
        point.append(pygame.Rect(fruit[i][0], fruit[i][1], 20, 20))
        
# ------------------------------以鍵盤控制玩家------------------------------

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT:
                moveLeft = False
                moveRight = True
            if event.key == K_UP:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False
            if event.key == K_c:
                player.x = 360
                player.y = 320

    # --------------------運用鍵盤移動變數調整玩家位置--------------------
    if moveDown and snake[0].bottom < WINDOWHEIGHT:
        nowdir = (0, 20)

    if moveUp and snake[0].top > 0:
        nowdir = (0, -20)

    if moveLeft and snake[0].left > 0:
        nowdir = (-20, 0)

    if moveRight and snake[0].right < WINDOWWIDTH:
        nowdir = (20, 0)
    
    nowpos = player[0][0] + nowdir[0], player[0][1] + nowdir[1]
    player.insert(0, nowpos)
    player.pop(len(player) - 1)

    # ------------------------------繪製物件------------------------------
    # 畫出白色背景
    windowSurface.fill(BG)  

    # 畫出玩家物件
    for i in range(len(player)):
        pygame.draw.rect(windowSurface, SNAKE, snake[i])  

    # 畫出果實物件
    for i in range(len(point)):
        pygame.draw.rect(windowSurface, FRUIT, point[i])  

    # 畫出軌道
    for i in range(len(wall)):  
        pygame.draw.rect(windowSurface, WALL, wall[i])
        
    # 繪製分數
    drawText('Score: %s' % (score), font, windowSurface, 150, 18)

    # 繪製難度
    drawText('Level: %s' % (level), font, windowSurface, 10, 18)  

    # ------------------------------碰撞偵測------------------------------
    # 當玩家撞到軌道,遊戲結束
    for line in lines[:]:  
        if snake[0].colliderect(line):
            time.sleep(1)
            failed_message()
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

    # 當玩家撞到自身,遊戲結束
    for body in snake[1:]:  
        if snake[0].colliderect(body):
            time.sleep(1)
            failed_message()
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

    # 當玩家吃到果實,得分
    # 且當分數為五的倍數時，難度+1，速度+0.5
    for p in point[:]:
        if snake[0].colliderect(point[0]):
            l = len(player)
            Xgap = player[l - 1][0] - player[l - 2][0]
            Ygap = player[l - 1][1] - player[l - 2][1]
            addback = player[l - 1][0] + Xgap, player[l - 1][1] + Ygap
            player.append(addback)
            eat_fruit_message()

            score += 1
            if score%5 == 0:
                level += 1
                FPS += 0.5
                 
            pygame.display.update()

    pygame.display.update()
    mainClock.tick(FPS)
