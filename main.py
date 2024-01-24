import os
import sys

import pygame

pygame.init()
pygame.font.init()
SCREEN_WIGHT, SCREEN_HEIGHT = 1150, 750
WIN = pygame.display.set_mode((SCREEN_WIGHT, SCREEN_HEIGHT))
BG = pygame.transform.scale(pygame.image.load('pics/background.png'), (SCREEN_WIGHT, SCREEN_HEIGHT))
pygame.display.set_caption('Smashbros on wish')
plattform_img = pygame.image.load('pics/plattform.png')

GRAVITY = 0.25
TERMINAL_VELOCITY = 1
JUMP = -7


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((175, 155, 96))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, animation_dir='player/run/', frames=6):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        self.is_jump = True
        self.current_sprite = 0
        self.load_images(animation_dir, frames)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.velocity = 0
        self.y = y
        self.x = x
        self.reload = 5

    def load_images(self, directory, frames):
        for i in range(frames):
            path = os.path.join(directory, f'{i}.png')
            self.sprites.append(pygame.image.load(path))

    def animate(self):
        self.is_animating = True

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.is_animating is True:
            self.current_sprite += 0.05
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]

    def gravity(self):# needs fixing
        self.y += self.velocity
        self.velocity = min(self.velocity + GRAVITY, TERMINAL_VELOCITY)
        self.rect.y = self.y

    def jump(self):
        if self.is_jump:
            self.velocity = JUMP
            self.is_jump = False

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def pos_x(self):
        return self.x

    def pos_y(self):
        return self.y

    def check_exit(self):
        if self.y > 500:
            sys.exit()

    def bullet(self):
        self.reload += 0.05
        if self.reload >= 5:
            bullet = Bullet(self.rect.right, self.rect.centery)
            bullet_group.add(bullet)
            self.reload = 0


moving_sprites = pygame.sprite.Group()
player = Player(200, 100)
moving_sprites.add(player)
bullet_group = pygame.sprite.Group()


def draw_window(background, plattform):
    WIN.blit(BG, (background.x, background.y))
    WIN.blit(plattform_img, (plattform.x, plattform.y))
    moving_sprites.draw(WIN)
    moving_sprites.update()
    bullet_group.draw(WIN)
    bullet_group.update()
    pygame.display.flip()


def main():
    background = pygame.Rect(0, 0, SCREEN_WIGHT, SCREEN_HEIGHT)
    plattform = pygame.Rect(150, 500, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_window(background, plattform)
        player.update()

        player.gravity()
        player.check_exit()
        while player.pos_y() > 480 and 156 < player.pos_x() < 990:
            player.y = 480
            player.velocity = 0
            player.is_jump = True

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w]:
            player.jump()
        if keys_pressed[pygame.K_a]:
            player.animate()
            player.left()
        if keys_pressed[pygame.K_d]:
            player.animate()
            player.right()
        if keys_pressed[pygame.K_SPACE]:
            player.bullet()


if __name__ == '__main__':
    main()
