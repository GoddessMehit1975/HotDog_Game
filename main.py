import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
# create the screen
screen = pygame.display.set_mode((800, 600))

# Background music
mixer.music.load('arcade_music.wav')
mixer.music.play(-1)

# Background
background = pygame.image.load('skyline.jpg')

# Caption and Icon
pygame.display.set_caption("Hot Dog Invaders")
icon = pygame.image.load('hotdog.png')
pygame.display.set_icon(icon)

# Player
pygame.display.set_caption("Hot Dog Invaders")
playerImg = pygame.image.load('hotdogship.png')
playerX = 370
playerY = 480
playerX_change = 40

# Mustard
# Ready state - can't see on screen
# Fire state - mustard is moving
mustardImg = pygame.image.load('mustard.png')
mustardX = 0
mustardY = 480
mustardX_change = 4
mustardY_change = 0.3
mustard_state = "ready"

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('peanut-butter.png'))
    enemyImg.append(pygame.image.load('pigeon.png'))
    enemyImg.append(pygame.image.load('teeth.png'))
    enemyImg.append(pygame.image.load('dog.png'))
    enemyImg.append(pygame.image.load('hamburger.png'))
    enemyImg.append(pygame.image.load('rat.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.1)
    enemyY_change.append(40)

# Score
score_value = 0
font = pygame.font.Font('ARCADE.ttf', 96)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('ARCADE.ttf', 64)


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (180, 150))


def showScore(x, y):
    score = over_font.render("Score :" + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def fire_mustard(x, y):
    global mustard_state
    mustard_state = "fire"
    screen.blit(mustardImg, (x + 16, y + 10))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, mustardX, mustardY):
    distance = math.sqrt((math.pow(enemyX - mustardX, 2)) + (math.pow(enemyY - mustardY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB - Red, Green, and Blue
    screen.fill((0, 102, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if a keystroke is pressed check if it's right or left
        if event.type == pygame.KEYDOWN:
            print("A keystroke has been pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -0.15
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.15
            if event.key == pygame.K_SPACE:
                if mustard_state is "ready":
                    mustard_Sound = mixer.Sound('squirt.wav')
                    mustard_Sound.play()
                    mustardX = playerX
                    fire_mustard(mustardX, mustardY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Player movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Mustard movement
    if mustardY <= 0:
        mustardY = 480
        mustard_state = "ready"

    if mustard_state is "fire":
        fire_mustard(mustardX, mustardY)
        mustardY -= mustardY_change

    # Enemy movement
    enemyX += enemyX_change
    for i in range(num_of_enemies):

        # Game Over

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.15
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.15
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], mustardX, mustardY)
        if collision:
            mustard_Sound = mixer.Sound('dead_enemy.wav')
            mustard_Sound.play()
            mustardY = 480
            mustard_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
