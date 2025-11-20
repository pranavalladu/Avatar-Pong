import sys

import pygame
import pygame.locals
import random

import math

import time


WIDTH, HEIGHT = 960 , 639

img = pygame.image.load("avatar-map.jpeg")
img = pygame.transform.scale(img, (WIDTH, HEIGHT))

earth_img = pygame.image.load("earth_img.jpg")
water_img = pygame.image.load()
air_img = pygame.image.load()
fire_img = pygame.image.load()

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
        self.y = screen.get_height() * (9 / 10)
        self.vy = 0
        self.ay = 0
        self.screen = screen
        self.score = 0

    def update(self, keys_held: set[int], ice1: bool, earth1: bool) -> None:
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
        if earth1:
            paddle_height = 150
            if self.y < 0:
                self.y = 0
            elif self.y > HEIGHT - paddle_height:
                self.y = HEIGHT - paddle_height
            pygame.draw.line(
                self.screen,
                "#00FF00",
                (self.x, self.y),
                (self.x, self.y + paddle_height),
                10,
            )
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - 70:
                self.vy = 7
            self.y += self.vy
            self.vy = 0
        else:
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_DOWN in keys_held and self.y < HEIGHT - 70:
                self.vy = 7
            self.y += self.vy
            self.vy = 0

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

    def update(self, keys_held: set[int], ice2: bool, earth2: bool) -> None:
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
        if earth2:
            paddle_height = 150
            if self.y < 0:
                self.y = 0
            elif self.y > HEIGHT - paddle_height:
                self.y = HEIGHT - paddle_height
            pygame.draw.line(
                self.screen,
                "#00FF00",
                (self.x, self.y),
                (self.x, self.y + paddle_height),
                10,
            )
            if pygame.K_w in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_s in keys_held and self.y < HEIGHT - 70:
                self.vy = 7
            self.y += self.vy
            self.vy = 0
        else:
            if pygame.K_w in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_s in keys_held and self.y < HEIGHT - 70:
                self.vy = 7
            self.y += self.vy
            self.vy = 0

            pygame.draw.line(
                self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + 70), 10
            )

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
        self.radius = 10
        self.wind_angle = 0
        self.wind_speed = 5
        self.pausetime = -1
        self.in_wind = False
        self.ax = 0
        self.ay = 0

    def update(
        self,
        keys_held,
        screen: pygame.Surface,
        player1: Player1,
        player2: Player2,
        fastball1: bool,
        wind1: bool,
        fastball2: bool,
        wind2: bool,
        earth1: bool, 
        earth2: bool
    ) -> None:
        self.screen = screen
        # If hit top, then bounce
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.vy *= -1
        # if hit side, then teleport to center
        if self.x <= (self.radius) * -1 or self.x >= WIDTH + self.radius:
            self.vx *= -1
            self.x = WIDTH // 2
        # if hit paddle, then bounce
        player1_height = 150 if earth1 else 70
        player2_height = 150 if earth2 else 70
        if (
            (self.vy / self.vx) * (player1.x - self.x) + self.y > player1.y
            and (self.vy / self.vx) * (player1.x - self.x) + self.y < (player1.y + player1_height)
            and self.x < player1.x + 10
            and self.x > player1.x - 10
        ):
            self.vx *= -1
        if (
            (self.vy / self.vx) * (player2.x - self.x) + self.y > player2.y
            and (self.vy / self.vx) * (player2.x - self.x) + self.y < (player2.y + player2_height)
            and self.x < player2.x + 10
            and self.x > player2.x - 10
        ):
            self.vx *= -1
        # if wind right, left
        if wind1 and self.x > WIDTH // 2:
            self.wind_angle += 5
            self.in_wind = True
            self.ax = ...
            self.ay = ...
        if wind2 and self.x < WIDTH // 2:
            self.wind_angle += 5
            self.in_wind = True
        # if not wind, set everything back to normal
        if not wind1 and self.x > WIDTH // 2 and self.in_wind == True:
            self.in_wind = False
            self.vx = 5
            if self.vy >= 0:
                self.vy = 5
            elif self.vy < 0:
                self.vy = -5
        if not wind2 and self.x < WIDTH // 2 and self.in_wind == True:
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
        if wind1 == True and pygame.K_RSHIFT in keys_held:
            self.vx *= -1
        if wind2 == True and pygame.K_LSHIFT in keys_held:
            self.vx *= -1
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

    earth_balls = []


    ice1 = False
    ice2 = False
    earth1 = False
    earth2 = False
    fastball1 = False
    fastball2 = False
    wind1 = False
    wind2 = False

    p1_effects = [ice1, earth1, fastball1, wind1]
    p2_effects = [ice2, earth2, fastball2, wind2]

    resume_time1 = -1
    resume_time1 = -1

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

        player1.update(keys_held, ice1, earth1)
        player2.update(keys_held, ice2, earth2)
    
        if earth1: 
            screen.blit(earth_img, (0, 0))
            if len(earth_balls) == 0:
                num_balls = random.randint(5, 20)
                for _ in range(num_balls):
                    x = random.randint(0, int(WIDTH // 2 - 50))
                    y = random.randint(0, int(HEIGHT - 10))
                    earth_balls.append(Earth_ball(x, y))
        if earth2:
            if len(earth_balls) == 0:
                num_balls = random.randint(5, 20)
                for _ in range(num_balls):
                    x = random.randint(int(WIDTH // 2 + 50), int(WIDTH - 10))
                    y = random.randint(0, int(HEIGHT - 10))
                    earth_balls.append(Earth_ball(x, y))

        earth_balls = [b for b in earth_balls if b.update(screen)]

        if not earth1 and not earth2:
            earth_balls.clear()

        # when ability is used: after 3 seconds, give new element
        if ice1 == False and earth1 == False and fastball1 == False and wind1 == False:
            resume_time1 = time.monotonic() + 3
            if time.monotonic() > resume_time1:
                p1_effects[random.randint(0, 3)] = True

        if ice2 == False and earth2 == False and fastball2 == False and wind2 == False:
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

        ball.update(
            keys_held, screen, player1, player2, fastball1, wind1, fastball2, wind2, earth1, earth2
        )

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
