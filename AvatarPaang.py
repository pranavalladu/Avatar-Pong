import sys

import pygame
import pygame.locals
import random

import math

import time


WIDTH, HEIGHT = 1280, 720


class Player1:

    def __init__(self, screen: pygame.Surface):
        self.x = screen.get_width() * (9 / 10)
        self.y = screen.get_height() * (9 / 10)
        self.vy = 0
        self.ay = 0
        self.radius = 30
        self.screen = screen
        self.score = 0

    def update(self, keys_held: set[int], ice1: bool) -> None:
        self.ax, self.ay = 0, 0
        if ice1:
            if pygame.K_UP in keys_held and self.y > 0:
                self.ay -= 0.3
            if pygame.K_DOWN in keys_held and self.y < 650:
                self.ay += 0.3
            if self.y<0 or self.y>650:
                self.vy=0
            self.vy += self.ay
            self.y += self.vy
            self.vy *= 0.97
            pygame.draw.line(
                self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + 70), 10
            )
        else:
            if pygame.K_UP in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_DOWN in keys_held and self.y < 650:
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

    def update(self, keys_held: set[int], ice2: bool) -> None:
        self.ax, self.ay = 0, 0
        while ice2:
            if pygame.K_w in keys_held and self.y > 0:
                self.ay -= 0.3
            if pygame.K_s in keys_held and self.y < 650:
                self.ay += 0.3
            if self.y<0 or self.y>650:
                self.vy=0
            self.vy += self.ay
            self.y += self.vy
            self.vy *= 0.97
            pygame.draw.line(
                self.screen, "#FFFFFF", (self.x, self.y), (self.x, self.y + 70), 10
            )
        else:
            if pygame.K_w in keys_held and self.y > 0:
                self.vy = -7
            if pygame.K_s in keys_held and self.y < 650:
                self.vy = 7
            self.y += self.vy
            self.vy = 0

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

    def update(self, keys_held, screen: pygame.Surface, player1: Player1, player2: Player2, fastball1:bool, wind1:bool, fastball2:bool, wind2:bool) -> None:
        self.screen = screen
        if self.y <= self.radius or self.y >= screen.get_height() - self.radius:
            self.vy *= -1
            self.y = screen.get_width // 2

        if self.x <= (self.radius) * -1 or self.x >= screen.get_width() + self.radius:
            self.vx *= -1
            self.pausetime=time.monotonic+2
            # pygame.draw.circle(screen, "#FFFFFF", (screen.get_width()//2, self.y), self.radius)
            # time.sleep(3)
            self.x = screen.get_width() // 2
        
        if (self.vy/self.vx)*(player1.x-self.x)+self.y > player1.y and (self.vy/self.vx)*(player1.x-self.x)+self.y < (player1.y+70) and self.x<player1.x+10 and self.x>player1.x-10:
            self.vx*=-1
        if (self.vy/self.vx)*(player2.x-self.x)+self.y > player2.y and (self.vy/self.vx)*(player2.x-self.x)+self.y < (player2.y+70) and self.x<player2.x+10 and self.x>player2.x-10:
            self.vx*=-1

        if wind1 and self.x>WIDTH//2:
            self.wind_angle+=5
        if wind2 and self.x<WIDTH//2:
            ...
        if not wind1 and self.x>WIDTH//2:
            ...
            #self.vx=5
            #self.vy=5
            #self.ax=0
            #self.ay=0
        if not wind2 and self.x<WIDTH//2:
            ...
            #self.vx=5
            #self.vy=5
            #self.ax=0
            #self.ay=0
        if self.vx>10:
            self.vx=10
        if self.vy>10:
            self.vy=10
        if self.vx<-10:
            self.vx=-10
        if self.vy<-10:
            self.vy=-10
        if wind1 == True and pygame.K_LSHIFT in keys_held:
        self.x += self.vx
        self.y += self.vy
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


# class Coin:

# def __init__(self,screen:pygame.Surface)-> None:
# self.screen=screen
# self.radius=10
# self.x=random.uniform(0,screen.get_width())
# self.y=random.uniform(0,screen.get_height())

# def update(self, player: Player1)->None:
# d=math.dist((self.x,self.y),(player.x,player.y))
# if d<self.radius+player.radius:
# self.x=random.uniform(0,self.screen.get_width())
# self.y=random.uniform(0,self.screen.get_height())
# pygame.draw.circle(self.screen,"#FFFFFF", (self.x,self.y),self.radius)


def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player1 = Player1(screen)
    player2 = Player2(screen)
    keys_held = set()

    # coins=[Coin(screen) for _ in range(10)]

    ball = Ball(screen.get_width() / 2, screen.get_height() / 2)
    
    ice1 = False 
    ice2 = False
    toomanyballs1 = False
    toomanyballs2 = False
    fastball1 = False
    fastball2 = False
    wind1 = False
    wind2 = False

    p1_effects=[ice1,toomanyballs1,fastball1,wind1]
    p2_effects=[ice2,toomanyballs2,fastball2,wind2]

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
        
        if ice1 == False and toomanyballs1 == False and fastball1 == False and wind1 == False:
            resume_time1=time.monotonic()+3
            if time.monotonic()>resume_time1:
                p1_effects[random.randint(0,3)] = True

        if ice2 == False and toomanyballs2 == False and fastball2 == False and wind2 == False:
            resume_time2=time.monotonic()+3
            if time.monotonic()>resume_time2:
                p1_effects[random.randint(0,3)] = True



        if ball.x < 0:
            player2.score += 1
        elif ball.x > WIDTH:
            player1.score += 1

        font = pygame.font.SysFont("Arial", 20)
        text_color = (255, 255, 255)
        score_left = font.render(str(player1.score), True, text_color)
        score_right = font.render(str(player2.score), True, text_color)
        screen.blit(score_left, (WIDTH//4, 20))
        screen.blit(score_right, (WIDTH*3//4, 20))


        # for coin in coins:
        # coin.update(player1)

        ball.update(screen, keys_held, player1, player2, fastball1, wind1, fastball2, wind2)

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
