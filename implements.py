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
    def __init__(self, color: tuple, pos: tuple = (0, 0), alive=True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

    def collide(self, items: list):
        self.rect.centerx = -self.rect.centerx  # Mark the block as destroyed
        self.alive = False
        
        # 20% chance to drop an item
        if random.random() < 0.2:  # 20% chance
            item_color = random.choice([config.add_score_color, config.paddle_long_color])  # Red or Blue
            item_pos = self.rect.center
            item = Item(item_color, item_pos)
            items.append(item)  # Add the item to the items list




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
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list, items: list):  # Accept items as argument
        for block in blocks:
            if self.rect.colliderect(block.rect):
                block.collide(items)  # Pass items to block's collide method

                if -block.rect.left > self.rect.centerx > -block.rect.right:
                    self.dir *= -1
                else:
                    self.dir = 180 - self.dir

    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        if self.rect.centerx < 0 or self.rect.centerx > config.display_dimension[0]:    
            self.dir = 180 - self.dir
        elif self.rect.centery < 0:
            self.dir = -self.dir

    def alive(self):
        if self.rect.centery > config.display_dimension[1]: 
            return False
        else:
            return True


class Item(Basic):
    def __init__(self, color: tuple, pos: tuple):
        super().__init__(color, 0, pos, config.item_size)
        self.alive = True

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide(self, paddle: Paddle):
        if self.rect.colliderect(paddle.rect):
            self.alive = False
            if self.color == config.paddle_long_color:  # Blue ball item
                return "blue"  # Return blue to signal the effect
            return "red"
        return None
