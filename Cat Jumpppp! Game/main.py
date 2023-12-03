import sys
from random import randint
import pygame
from pygame import *
from pygame.ftfont import Font
from pygame.locals import *
from pygame.sprite import *

class Cat(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("cat2.png")
        self.rect = self.image.get_rect()
        self.is_jumping = False
        self.jump_speed = -20
        self.gravity = 1
        self.rect.bottom = 700
        self.ground_y = self.rect.bottom
        self.mask = mask.from_surface(self.image)


    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = -20

    def update(self):
        if self.is_jumping:
            self.rect.y += self.jump_speed
            self.jump_speed += self.gravity
            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y
                self.is_jumping = False


class Block(Sprite):
    def __init__(self, speed = 5):
        Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.bottom = 700
        self.speed = speed
        self.mask = mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.speed



def main():
    pygame.init()
    screen = display.set_mode((1200, 768), FULLSCREEN)
    display.set_caption("Cat Jumppp!")
    my_cat = Cat()
    all_sprites = Group(my_cat)

    block = Block()
    blocks = Group()
    block_speed = 5
    block.rect.x = 1200
    all_sprites.add(block)
    blocks.add(block)

    clock = pygame.time.Clock()
    spawn_block_timer = 0

    while True:
        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                break
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif ev.key == K_UP or K_SPACE:
                    my_cat.jump()

        all_sprites.update()

        spawn_block_timer += 1
        if spawn_block_timer > 120:  # Adjust as needed
            spawn_block_timer = 0
            new_block = Block(block_speed)
            new_block.rect.x = 1200  # Start new blocks at the right edge
            all_sprites.add(new_block)
            blocks.add(new_block)

            block_speed += 1.25

        collision = spritecollide(my_cat, blocks, False, sprite.collide_mask)
        if collision:
            print("Collision detected")
            break

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (0, 700), (1400, 700), 5)  # Ground line
        all_sprites.draw(screen)
        display.update()

        clock.tick(60)


main()