import pygame, sys
import pygame.locals as gameLocals
import random
import time

pygame.init()
pygame.mixer.init()
pygame.font.init()
music = ["superhero.ogg", "2.ogg"]

main_surface = pygame.display.set_mode((1400, 800))
surface_rect = main_surface.get_rect()
clock = pygame.time.Clock()

UPLEFT = 0
DOWNLEFT = 1
UPRIGHT = 2
DOWNRIGHT = 3

human = 0
ai = 0

UP1 = False
DOWN1 = False
NO_MOVEMENT1 = True

scoredOn = False


def musicPlayer():
    x = random.randint(0,1)
    size = len(music)
    pygame.mixer.music.load(music[x])
    pygame.mixer.music.play()
    pos = pygame.mixer.music.get_pos()
    while pos == -1:
        if x <= size:
            x += 1
            pygame.mixer.music.load(music[x])
            pygame.mixer.music.play()


musicPlayer()


class Player(pygame.sprite.Sprite):
    def __init__(self, player_number):
        pygame.sprite.Sprite.__init__(self)
        self.player_number = player_number
        self.image = pygame.Surface([10, 150])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.speed = 8

        if self.player_number == 1:
            self.rect.centerx = main_surface.get_rect().left
            self.rect.centerx += 50
        elif self.player_number == 2:
            self.rect.centerx = main_surface.get_rect().right
            self.rect.centerx -= 50
        self.rect.centery = main_surface.get_rect().centery

    def move(self):
        if self.player_number == 1:
            if (UP1 == True) and (self.rect.y > 5):
                self.rect.y -= self.speed
            elif (DOWN1 == True) and (self.rect.bottom < 795):
                self.rect.y += self.speed

    def getY(self):
        return self.rect.y

    def AI(self):
        ballLocation = ball.getY()
        # direction = ball.getDirection()

        if ballLocation != cpu.getY():
            if ballLocation > cpu.getY():
                if cpu.getY() < 649:
                    self.rect.y += self.speed + 4
            if ballLocation < cpu.getY():
                if cpu.getY() > 0:
                    self.rect.y -= self.speed + 4


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = surface_rect.centerx
        self.rect.centery = surface_rect.centery
        self.speed = 4
        self.direction = random.randint(0, 3)

    def move(self):
        if self.direction == UPLEFT:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        elif self.direction == UPRIGHT:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        elif self.direction == DOWNLEFT:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        elif self.direction == DOWNRIGHT:
            self.rect.x += self.speed
            self.rect.y += self.speed

    def change_direction(self):
        if self.rect.y < 0 and self.direction == UPLEFT:
            self.direction = DOWNLEFT
        if self.rect.y < 0 and self.direction == UPRIGHT:
            self.direction = DOWNRIGHT
        if self.rect.y > 790 and self.direction == DOWNLEFT:
            self.direction = UPLEFT
        if self.rect.y > 790 and self.direction == DOWNRIGHT:
            self.direction = UPRIGHT

    def getY(self):
        return self.rect.y

    def getDirection(self):
        if self.direction == UPRIGHT:
            return UPRIGHT
        elif self.direction == DOWNRIGHT:
            return DOWNRIGHT


player1 = Player(1)
cpu = Player(2)
ball = Ball()

theScore = pygame.font.SysFont("Arial", 80)


def paddleAIHit():
    if pygame.sprite.collide_rect(ball, cpu):
        if (ball.direction == UPRIGHT):
            ball.direction = UPLEFT
        elif (ball.direction == DOWNRIGHT):
            ball.direction = DOWNLEFT
        ball.speed += 1


def paddlePlayerHit():
    if pygame.sprite.collide_rect(ball, player1):
        if (ball.direction == UPLEFT):
            ball.direction = UPRIGHT
        elif (ball.direction == DOWNLEFT):
            ball.direction = DOWNRIGHT
        ball.speed += 1


WHITE = (0, 0, 0)
all_render = pygame.sprite.RenderPlain(player1, cpu, ball)

while True:
    clock.tick(60)

    if (ball.rect.x > 1400):
        ball.rect.centerx = surface_rect.centerx
        ball.rect.centery = surface_rect.centery
        ball.direction = random.randint(0, 1)
        ball.speed = 4
        human += 1
    elif (ball.rect.x < 0):
        ball.rect.centerx = surface_rect.centerx
        ball.rect.centery = surface_rect.centery
        ball.direction = random.randint(2, 3)
        ball.speed = 4
        ai += 1
    for event in pygame.event.get():
        if event.type == gameLocals.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == gameLocals.KEYDOWN:

            if event.key == pygame.K_UP:
                UP1 = True
                DOWN1 = False
                NO_MOVEMENT1 = False
            elif event.key == pygame.K_DOWN:
                UP1 = False
                DOWN1 = True
                NO_MOVEMENT1 = False

        elif event.type == gameLocals.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                NO_MOVEMENT1 = True
                DOWN1 = False
                UP1 = False


    score = theScore.render("Player: " + str(human) + "      CPU: " + str(ai), True, (255,255,255), (0,0,0))
    scorerect = score.get_rect()
    scorerect.centerx = surface_rect.centerx
    scorerect.y = 15

    main_surface.fill((0, 0, 0))
    main_surface.blit(score, scorerect)


    all_render.draw(main_surface)

    player1.move()
    cpu.AI()
    ball.move()
    ball.change_direction()

    paddleAIHit()
    paddlePlayerHit()

    pygame.display.update()
