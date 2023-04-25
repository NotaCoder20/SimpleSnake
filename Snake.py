import random
import sys
import time
import numpy as np
import pygame

white, black = (255, 255, 255), (0, 0, 0)
x, y = 0, 0
score = 0
gameOver = False
grid = np.zeros((10, 16), dtype=np.int8)
prevTime, Autorun, timeset = 0, 0, 0.21
snake = [[[5, 8], 1], [[4, 8], 1], [[3, 8], 1], [[2, 8], 1]]

movements = {1: (-1, 0), 2: (0, -1), 3: (1, 0), 4: (0, 1)}
HeadDic = {1: 'Graphics/snakeHD.png', 2: 'Graphics/snakeHR.png', 3: 'Graphics/snakeHU.png', 4: 'Graphics/snakeHL.png'}
TailDic = {1: 'Graphics/snakeTD.png', 2: 'Graphics/snakeTR.png', 3: 'Graphics/snakeTU.png', 4: 'Graphics/snakeTL.png'}
bodyDic = {1: 'Graphics/snakeBU.png', 2: 'Graphics/snakeBR.png', 3: 'Graphics/snakeBU.png', 4: 'Graphics/snakeBR.png'}

pygame.init()
scr = pygame.display.set_mode((900, 700))
font = pygame.font.Font('freesansbold.ttf', 20)
directions = {pygame.K_DOWN: 1, pygame.K_RIGHT: 2, pygame.K_UP: 3, pygame.K_LEFT: 4}
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (45, 45))


def Initialize():
    global score, snake, gameOver, grid
    grid = np.zeros((10, 16), dtype=np.int8)
    scr.fill(white)
    font2 = pygame.font.SysFont('georgia', 50)
    text = font2.render("SNAKE!", True, black)
    scr.blit(text, (50, 50))
    score = 0
    snake = [[[5, 8], 1], [[4, 8], 1], [[3, 8], 1], [[2, 8], 1]]
    drawGrid()
    putText(f"Score:", (500, 50), black)
    generateApple()
    drawSnake()
    gameOver = False


def checkCollision():
    head = snake[0][0]
    for i in range(1, len(snake)):
        if head == snake[i][0]:
            return True


def putText(mgs: str, pos, col):
    text = font.render(mgs, True, col)
    scr.blit(text, pos)


def drawGrid():
    for i in range(50, 900, 50):
        pygame.draw.line(scr, black, (i, 100), (i, 600), 2)
    for i in range(100, 650, 50):
        pygame.draw.line(scr, black, (50, i), (850, i), 2)


def drawSnake():
    head_img = pygame.image.load(HeadDic[snake[0][1]])
    tail_img = pygame.image.load(TailDic[snake[-2][1]])
    count = 0
    n = len(snake) - 1
    for posDir in snake:
        gridDir = grid[posDir[0][0]][posDir[0][1]]
        if count == 0:
            snakeImg = head_img
        elif count == n:
            snakeImg = tail_img
        elif gridDir == 0:
            snakeImg = pygame.image.load(bodyDic[posDir[1]])
        else:
            snakeImg = pygame.image.load('Graphics/' + str(gridDir) + str(posDir[1]) + '.png')
        scaled_image = pygame.transform.scale(snakeImg, (50, 50))
        scr.blit(scaled_image, (posDir[0][1] * 50 + 50, posDir[0][0] * 50 + 100))
        count += 1
    pygame.display.update()


def updateSnake():
    for posDir in snake:
        xDir = grid[posDir[0][0]][posDir[0][1]]
        pygame.draw.rect(scr, white, (posDir[0][1] * 50 + 52, posDir[0][0] * 50 + 102, 48, 48))
        posDir[1] = xDir if xDir else posDir[1]
        if posDir == snake[-1]:
            grid[snake[-1][0][0]][snake[-1][0][1]] = 0
        dx1, dy1 = movements[posDir[1]]
        posDir[0] = [(posDir[0][0] - dx1) % 10, (posDir[0][1] - dy1) % 16]
        if posDir[0][0] == 10 or posDir[0][1] == 16:
            print(posDir[0])


def generateApple():
    global x, y
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 15)
        if not any(block[0] == [x, y] for block in snake):
            break
    scr.blit(apple, (y * 50 + 55, x * 50 + 105))


Initialize()
pygame.time.Clock().tick(60)
print(pygame.font.get_fonts())
while True:
    if (time.time() - prevTime >= timeset) and not gameOver:
        if snake[0][0] == [x, y]:
            mov = snake[-1][1]
            dx, dy = movements[mov]
            x1 = snake[-1][0][0] + dx
            y1 = snake[-1][0][1] + dy
            snake.append([[x1, y1], mov])
            pygame.draw.rect(scr, white, (568, 48, 50, 50))
            score += 1
            putText(str(score).zfill(3), (570, 50), black)
            generateApple()
        updateSnake()
        drawSnake()
        if checkCollision():
            gameOver = True
            putText("GameOver!", (400, 620), black)
            putText("To Retry click here or press 'R'", (300, 650), black)
            pygame.display.update()
        prevTime = time.time()
    for event in pygame.event.get():
        pygame.display.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            Key = event.key
            head_pos, head_dir = snake[0]
            if Key == 27:
                pygame.quit()
                sys.exit()
            if (not gameOver) and (Key in directions) and (head_dir % 2 != directions[Key] % 2):
                grid[head_pos[0]][head_pos[1]] = directions[Key]
        xmos, ymos = pygame.mouse.get_pos()
        if gameOver:
            pygame.draw.rect(scr, white, (300, 650, 300, 48))
            if 600 > xmos > 300 and 670 > ymos > 650:
                putText("To Retry click here or press 'R'", (300, 650), (255, 0, 0))
                if pygame.mouse.get_pressed()[0]:
                    Initialize()
            else:
                putText("To Retry click here or press 'R'", (300, 650), black)
            if event.type == pygame.KEYDOWN:
                Key = event.key
                if Key == 114:
                    Initialize()
