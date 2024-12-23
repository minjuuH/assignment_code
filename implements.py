import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        # ============================================
        # TODO: Implement an event when block collides with a ball
        self.rect.centerx = -self.rect.centerx  #블록 삭제
        self.alive = False
        pass


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, color = config.ball_color, pos: tuple = config.ball_pos):
        super().__init__(color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list, balls: list):
        # ============================================
        # TODO: Implement an event when the ball hits a block
        import random       #random한 공 색상 지정을 위한 random 모듈 import

        for block in blocks:
            if self.rect.colliderect(block.rect):
                block.collide()
            
                #블록 가로면에 대한 충돌 계산
                if -block.rect.left > self.rect.centerx > -block.rect.right:
                    self.dir *= -1
                #블록 세로면에 대한 충돌 계산
                else:
                    self.dir = 180-self.dir

                if random.random() < 0.2:   # 20% 확률로 item 생성
                    new_color = random.randint(0,1)         #둘 중 하나를 고르기 위한 random 값

                    #새로운 ball 객체 생성
                    new_ball = BallItem(config.ball_item_colors[new_color], pos=self.rect.center)

                    balls.append(new_ball)  #ball 리스트에 새 공 추가
        pass

    def collide_paddle(self, paddle: Paddle, balls: list) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        # ============================================
        # TODO: Implement a service that bounces off when the ball hits the wall
        # 좌우 벽 충돌
        if self.rect.centerx < 0 or self.rect.centerx > 600:    #config.py display_dimension 값 참조하여 600으로 범위 지정
            self.dir = 180 - self.dir
        
        # 상단 벽 충돌
        elif self.rect.centery < 0:
            self.dir = -self.dir
    
    def alive(self):
        # ============================================
        # TODO: Implement a service that returns whether the ball is alive or not
        if self.rect.centery > 800:     #공의 위치가 display y값보다 커질 경우 false 반환
            return False
        else:
            return True
        pass


class BallItem(Ball):   #Ball을 상속받은 아이템 클래스
    def __init__(self, color: tuple, pos: tuple = config.ball_pos):
        super().__init__(color, pos)
        self.dir = 270              #아이템이 아래로만 떨어지도록 설정

    def collide_block(self, blocks: list, balls:list):
        pass    #블록과 충돌 시 아무 동작 x

    def collide_paddle(self, paddle: Paddle, balls: list) -> None:
        # 아이템이 패들과 부딪힐 경우 삭제되도록 설정
        if self.rect.colliderect(paddle.rect):
            balls.remove(self)