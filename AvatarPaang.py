#MUSIC FILE USAGE: https://www.pygame.org/docs/ref/music.html
import sys

import pygame
import pygame.locals
import random

import math

import time


WIDTH, HEIGHT = 822, 549

# background = pygame.image.load("avatar-map.jpeg")
# pygame.transform.scale(background, (WIDTH, HEIGHT))

img = pygame.image.load("avatar-map.jpeg")


class Player1:

    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() * (9 / 10)
        self.y = screen.get_height() * (9 / 10)
        self.vy = 0
        self.ay = 0
        self.screen = screen
        self.score = 0
        self.wind = False
        self.fast = False
        self.speedtime = -1

    def update(self, keys_held: set[int], ice1: bool) -> None:
        self.ax, self.ay = 0, 0
        if ice1:
            if pygame.K_UP in keys_held and self.y > 0:
                self.ay -= 0.3
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - 70:
                self.ay += 0.3
            if self.y <= 0 or self.y >= HEIGHT - 70:
                self.vy = 0
            self.vy += self.ay
            self.y += self.vy
            self.vy *= 0.97
            pygame.draw.line(
                self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + 70), 10
            )
        elif self.speedtime>time.monotonic():
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -11
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - 70:
                self.vy = 11
            self.y += self.vy
            self.vy = 0
        else:
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - 70:
                self.vy = 7
            self.y += self.vy
            self.vy = 0
        #speedtime
        if self.fast==True and pygame.K_RSHIFT in keys_held:
            self.speedtime = time.monotonic() + 3
            self.fast=False


        pygame.draw.line(
            self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + 70), 10
        )


class Player2:

    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() // 10
        self.y = screen.get_height() // 10
        self.vy = 0
        self.ay = 0
        self.radius = 30
        self.screen = screen
        self.score = 0
        self.wind = False
        self.fast = False
        self.speedtime = -1

    def update(self, keys_held: set[int], ice2: bool) -> None:
        self.ax, self.ay = 0, 0
        if ice2:
            if pygame.K_w in keys_held and self.y > 0:
                self.ay -= 0.3
            if pygame.K_s in keys_held and self.y < HEIGHT - 70:
                self.ay += 0.3
            if self.y < 0 or self.y > HEIGHT - 70:
                self.vy = 0
            self.vy += self.ay
            self.y += self.vy
            self.vy *= 0.97
            pygame.draw.line(
                self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + 70), 10
            )
        elif self.speedtime>time.monotonic():
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -11
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - 70:
                self.vy = 11
            self.y += self.vy
            self.vy = 0
        else:
            if pygame.K_w in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_s in keys_held and self.y < HEIGHT - 70:
                self.vy = 7
            self.y += self.vy
            self.vy = 0

        if self.fast==True and pygame.K_RSHIFT in keys_held:
            self.speedtime = time.monotonic() + 3
            self.fast=False

        pygame.draw.line(
            self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + 70), 10
        )


class Ball:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 5
        self.color = (255, 255, 255)
        self.radius = 5
        self.wind_angle = 0
        self.wind_speed = 5
        self.pausetime = -1
        self.in_wind = False
        self.ax = 0
        self.ay = 0
        self.windspeed = 0.1

    def update(
        self,
        keys_held,
        screen: pygame.Surface,
        player1: Player1,
        player2: Player2,
        fastball1: bool,
        fastball2: bool,
    ) -> None:
        self.screen = screen

        # If hit top or bottom, then bounce
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.vy *= -1
            ##pygame.mixer.music.play(pygame.mixer.Sound(bouncewall_sound))

        # if hit side, then teleport to center
        if self.x <= (self.radius) * -1 or self.x >= WIDTH + self.radius:
            self.vx *= -1
            self.x = WIDTH // 2
            self.y = HEIGHT // 2

        # if hit paddle, then bounce
        if (
            (self.vy / self.vx) * (player1.x - self.x) + self.y > player1.y
            and (self.vy / self.vx) * (player1.x - self.x) + self.y < (player1.y + 70)
            and self.x < player1.x + 10
            and self.x > player1.x - 10
        ):
            self.vx *= -1
            ##pygame.mixer.music.play(pygame.mixer.Sound(bounce_sound))
        if (
            (self.vy / self.vx) * (player2.x - self.x) + self.y > player2.y
            and (self.vy / self.vx) * (player2.x - self.x) + self.y < (player2.y + 70)
            and self.x < player2.x + 10
            and self.x > player2.x - 10
        ):
            self.vx *= -1
            ##pygame.mixer.music.play(pygame.mixer.Sound(bounce_sound))

        # if wind, do wind things
        if player1.wind and self.x > WIDTH // 2:
            self.wind_angle += 0.01
            self.in_wind = True
            self.ax = (1 / 2) * math.cos(self.wind_angle) * self.windspeed
            self.ay = (2) * math.sin(self.wind_angle) * self.windspeed
        if player2.wind and self.x < WIDTH // 2:
            self.wind_angle += 0.01
            self.in_wind = True

        # if not wind, set everything back to normal
        if not player1.wind and self.x > WIDTH // 2 and self.in_wind == True:
            self.in_wind = False
            self.vx = 5
            if self.vy >= 0:
                self.vy = 5
            elif self.vy < 0:
                self.vy = -5
        if not player2.wind and self.x < WIDTH // 2 and self.in_wind == True:
            self.in_wind = False
            self.vx = -5
            if self.vy >= 0:
                self.vy = 5
            elif self.vy < 0:
                self.vy = -5

        # max speed
        if self.vx > 10:
            self.vx = 10
        if self.vy > 10:
            self.vy = 10
        if self.vx < -10:
            self.vx = -10
        if self.vy < -10:
            self.vy = -10

        # activate ability
        if player1.wind and pygame.K_RSHIFT in keys_held:
            self.vx *= -1
            player1.wind = False
        if player2.wind and pygame.K_LSHIFT in keys_held:
            self.vx *= -1
            player2.wind = False

        # final movement
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        self.ax = 0
        self.ay = 0

        # drawing the ball
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player1 = Player1(screen)
    player2 = Player2(screen)
    keys_held = set()

    ball = Ball(screen.get_width() / 2, screen.get_height() / 2)

    ice1 = False
    ice2 = False
    toomanyballs1 = False
    toomanyballs2 = False
    fastball1 = False
    fastball2 = False

    #importing sounds?????
    ##bounce_sound=pygame.mixer.Sound("jump.wav")
    ##bouncewall_sound=pygame.mixer.Sound("bouncewall.wav")
    ##pygame.mixer.music.load(pygame.mixer.Sound(bounce_sound))
    ##pygame.mixer.music.load(pygame.mixer.Sound(bouncewall_sound))

    p1_effects = [ice1, toomanyballs1, fastball1, player1.wind]
    p2_effects = [ice2, toomanyballs2, fastball2, player2.wind]

    resume_time1 = -1
    resume_time1 = -1

    while True:
        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.locals.KEYDOWN:
                keys_held.add(event.key)
            if event.type == pygame.locals.KEYUP:
                keys_held.remove(event.key)
        player1.update(keys_held, ice1)
        player2.update(keys_held, ice2)

        # when ability is used: after 3 seconds, give new element
        if (
            ice1 == False
            and toomanyballs1 == False
            and player1.fast == False
            and player1.wind == False
        ):
            resume_time1 = time.monotonic() + 3
            if time.monotonic() > resume_time1:
                p1_effects[random.randint(0, 3)] = True

        if (
            ice2 == False
            and toomanyballs2 == False
            and player2.fast == False
            and player2.wind == False
        ):
            resume_time2 = time.monotonic() + 3
            if time.monotonic() > resume_time2:
                p1_effects[random.randint(0, 3)] = True

        # Counting score
        if ball.x < ball.radius * -1:
            player2.score += 1
        elif ball.x > WIDTH + ball.radius:
            player1.score += 1
        font = pygame.font.SysFont("Arial", 20)
        text_color = (255, 255, 255)
        score_left = font.render(str(player1.score), True, text_color)
        score_right = font.render(str(player2.score), True, text_color)
        screen.blit(score_left, (WIDTH // 4, 20))
        screen.blit(score_right, (WIDTH * 3 // 4, 20))

        # for coin in coins:
        # coin.update(player1)

        ball.update(
            keys_held, screen, player1, player2, fastball1, fastball2, 
        )

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
