#MUSIC FILE USAGE: https://www.pygame.org/docs/ref/music.html
import sys

import pygame
import pygame.locals
import random

import math

import time


WIDTH, HEIGHT = 960 , 639

img = pygame.image.load("avatar-map.jpeg")
img = pygame.transform.scale(img, (WIDTH, HEIGHT))

#earth_img = pygame.image.load("earth_img.jpg")
#water_img = pygame.image.load("water.png.webp")
#air_img = pygame.image.load("")
#fire_img = pygame.image.load()

#img = pygame.image.load("avatar-map.jpeg")

def draw_start_screen(screen):
    screen.blit(img, (0, 0))
    font = pygame.font.SysFont("Arial", 60)
    title_text = font.render("Press SPACE to Start", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height()//2))
    pygame.display.flip()


class Player1:

    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() * (9 / 10)
        self.y = HEIGHT //2
        self.vy = 0
        self.ay = 0
        self.screen = screen
        self.score = 0
        self.wind = False
        self.fast = False
        self.speedtime = -1
        self.ice = False
        self.color=(255,255,255)
        self.length = 70
        self.earth = False
        self.bigtime = -1

    def update(self, keys_held: set[int]) -> None:
        self.ax, self.ay = 0, 0
        if self.ice:
            if pygame.K_UP in keys_held and self.y > 0:
                self.ay -= 0.3
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - self.length:
                self.ay += 0.3
            if self.y <= 0 or self.y >= HEIGHT - self.length:
                self.vy = 0
            if self.y <= 0 or self.y >= HEIGHT - self.length:
                self.vy = 0
            self.vy += self.ay
            self.y += self.vy
            self.vy *= 0.97
            pygame.draw.line(
                self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + self.length), 10
            )
        
        elif self.speedtime>time.monotonic():
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -11
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - self.length:
                self.vy = 11
            self.y += self.vy
            self.vy = 0
        
        else:
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - self.length:
                self.vy = 7
            self.y += self.vy
            self.vy = 0

        if self.earth == True and pygame.K_RSHIFT in keys_held:
            self.bigtime = time.monotonic() + 3

        #Earth effect
        if self.bigtime>time.monotonic():
            self.length = 150
        if self.bigtime<time.monotonic():
            self.length = 70

        #speedtime
        if self.fast==True and pygame.K_RSHIFT in keys_held:
            self.speedtime = time.monotonic() + 3
            self.fast=False

        #color for element
        if self.ice: self.color=(50,50,255)
        if self.wind: self.color=(255,150,150)
        if self.fast: self.color=(255,50,50)
        if self.earth: self.color = (50,255,50)



        pygame.draw.line(
            self.screen, self.color, (self.x, self.y), (self.x, self.y + 70), 10
        )


class Player2:

    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() // 10
        self.y = HEIGHT //2 
        self.vy = 0
        self.ay = 0
        self.radius = 30
        self.screen = screen
        self.score = 0
        self.wind = False
        self.fast = False
        self.speedtime = -1
        self.ice = False
        self.color=(255,255,255)
        self.length = 70
        self.earth = False
        self.bigtime = -1

    def update(self, keys_held: set[int],) -> None:
        self.ax, self.ay = 0, 0
        if self.ice:
            if pygame.K_w in keys_held and self.y > 0:
                self.ay -= 0.3
            if pygame.K_s in keys_held and self.y < HEIGHT - self.length:
                self.ay += 0.3
            if self.y < 0 or self.y > HEIGHT - self.length:
                self.vy = 0
            if self.y < 0 or self.y > HEIGHT - self.length:
                self.vy = 0
            self.vy += self.ay
            self.y += self.vy
            self.vy *= 0.97
            pygame.draw.line(
                self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + self.length), 10
            )
        elif self.speedtime>time.monotonic():
            if pygame.K_w in keys_held and self.y > 0:
                self.vy = -11
            if pygame.K_s in keys_held and self.y < HEIGHT - self.length:
                self.vy = 11
            self.y += self.vy
            self.vy = 0

        else:
            if pygame.K_w in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_s in keys_held and self.y < HEIGHT - self.length:
                self.vy = 7
            self.y += self.vy
            self.vy = 0

        if self.earth == True and pygame.K_LSHIFT in keys_held:
            self.bigtime = time.monotonic() + 3

         #Earth effect
        if self.bigtime>time.monotonic():
            self.length = 150
        if self.bigtime<time.monotonic():
            self.length = 70

        else:
            if pygame.K_w in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_s in keys_held and self.y < HEIGHT - self.length:
                self.vy = 7
            self.y += self.vy
            self.vy = 0

        if self.fast==True and pygame.K_RSHIFT in keys_held:
            self.speedtime = time.monotonic() + 3
            self.fast=False

        #color for element
        if self.ice: self.color=(50,50,255)
        if self.wind: self.color=(255,150,150)
        if self.fast: self.color=(255,50,50)

        pygame.draw.line(
            self.screen, self.color, (self.x, self.y), (self.x, self.y + self.length), 10
        )
        if self.earth: self.color = (50,255,50)

class Earth_ball:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.choice([-4, -3, -2, 2, 3, 4])
        self.vy = random.choice([-4, -3, -2, 2, 3, 4])
        self.radius = 10
        self.color = (0, 255, 0)

    def update(self, screen: pygame.Surface) -> bool:
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.vy *= -1
        self.x += self.vx
        self.y += self.vy

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        if self.x < 0 or self.x > WIDTH:
            return False
        else: 
            return True

class Ball:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 5
        self.color = (255, 255, 255)
        self.radius = 7
        self.wind_angle = 0
        self.wind_speed = 5
        self.pausetime = -1
        self.in_wind = False
        self.ax = 0
        self.ay = 0
        self.windspeed = 0.1
        self.slowtime = -1
        self.slowtime = -1
        self.in_speed = False

    def update(
        self,
        keys_held,
        screen: pygame.Surface,
        player1: Player1,
        player2: Player2,
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
            and (self.vy / self.vx) * (player1.x - self.x) + self.y < (player1.y + player1.length)
            and self.x < player1.x + 10
            and self.x > player1.x - 10
        ):
            self.vx *= -1
            ##pygame.mixer.music.play(pygame.mixer.Sound(bounce_sound))
        if (
            (self.vy / self.vx) * (player2.x - self.x) + self.y > player2.y
            and (self.vy / self.vx) * (player2.x - self.x) + self.y < (player2.y + player2.length)
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

        #slow ball if ice
        if player1.ice and self.x>WIDTH//2 and pygame.K_RSHIFT in keys_held:
            self.vx *= 1/2
            self.vy *= 1/2
            self.slowtime=time.monotonic()+2
            player2.ice = False
        if player2.ice and self.x<WIDTH//2 and pygame.K_LSHIFT in keys_held:
            self.vx *= 1/2
            self.vy *= 1/2
            self.slowtime=time.monotonic()+2
            player2.ice = False

        #normal speed when slowtime is over
        if self.slowtime == time.monotonic():
            if self.vx >= 0:
                self.vx = 5
            elif self.vx < 0:
                self.vx = -5
            if self.vy >= 0:
                self.vy = 5
                self.vy = 5
            elif self.vy < 0:
                self.vy = -5

        if player1.fast and self.x > WIDTH // 2:
            self.in_speed = True
            self.vx *= 1.5
            self.vy *= 1.5
        if player2.fast and self.x < WIDTH // 2:
            self.in_speed = True
            self.vx *= 1.5
            self.vy *= 1.5

        # if not wind, set everything back to normal
        if not player1.fast and self.x > WIDTH // 2 and self.in_speed == True:
            self.in_speed = False
            self.vx = 5
            if self.vy >= 0:
                self.vy = 5
            elif self.vy < 0:
                self.vy = -5
        if not player2.fast and self.x < WIDTH // 2 and self.in_speed == True:
            self.in_speed = False
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

    earth_balls = []



    #importing sounds?????
    ##bounce_sound=pygame.mixer.Sound("jump.wav")
    ##bouncewall_sound=pygame.mixer.Sound("bouncewall.wav")
    ##pygame.mixer.music.load(pygame.mixer.Sound(bounce_sound))
    ##pygame.mixer.music.load(pygame.mixer.Sound(bouncewall_sound))

    p1_effects = [player1.ice, player1.earth, player1.fast, player1.wind]
    p2_effects = [player2.ice, player2.earth, player2.fast, player2.wind]

    resume_time1 = -1
    resume_time1 = -1

    #sozinscomet = random.randint(30,120)

    while True:
        screen.blit(img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.locals.KEYDOWN:
                keys_held.add(event.key)
            if event.type == pygame.locals.KEYUP:
                keys_held.remove(event.key)

        player1.update(keys_held)
        player2.update(keys_held)
    
        #sozin's comet
        #if sozinscomet<time.monotonic():
        #    pygame.quit

        if player1.earth: 
            #screen.blit(earth_img, (0, 0))
            if len(earth_balls) == 0:
                num_balls = random.randint(5, 20)
                for _ in range(num_balls):
                    x = random.randint(0, int(WIDTH // 2 - 50))
                    y = random.randint(0, int(HEIGHT - 10))
                    earth_balls.append(Earth_ball(x, y))
        if player2.earth:
            if len(earth_balls) == 0:
                num_balls = random.randint(5, 20)
                for _ in range(num_balls):
                    x = random.randint(int(WIDTH // 2 + 50), int(WIDTH - 10))
                    y = random.randint(0, int(HEIGHT - 10))
                    earth_balls.append(Earth_ball(x, y))

        earth_balls = [b for b in earth_balls if b.update(screen)]

        if not player1.earth and not player2.earth:
            earth_balls.clear()

        # when ability is used: after 3 seconds, give new element
        if (
            player1.ice == False
            and player1.earth == False
            and player1.fast == False
            and player1.wind == False
        ):
            resume_time1 = time.monotonic() + 5
        if time.monotonic() > resume_time1:
            p1_effects[random.randint(0, 3)] = True

        if (
            player2.ice == False
            and player2.earth == False
            and player2.fast == False
            and player2.wind == False
        ):
            resume_time2 = time.monotonic() + 5
        if time.monotonic() > resume_time2:
            p2_effects[random.randint(0, 3)] = True

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

        ball.update(
            keys_held, screen, player1, player2,
        )

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
