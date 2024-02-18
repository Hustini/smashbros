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


class HealthBar:
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    def reduce_hp(self):
        self.hp -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((175, 155, 96))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIGHT or self.rect.x < 0:  # works but if performance issue then probably here
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, x_health, animation_dir='player/run/', frames=6):
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
        self.direction = 'right'
        self.health = HealthBar(x_health, 25, 200, 30, 5)

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

    def gravity(self):
        self.y += self.velocity
        self.velocity = min(self.velocity + GRAVITY, TERMINAL_VELOCITY)
        self.rect.y = self.y

    def jump(self):
        if self.is_jump:
            self.velocity = JUMP
            self.is_jump = False

    def left(self):
        self.x -= 1
        if self.direction != "left":
            self.sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]
            self.direction = "left"

    def right(self):
        self.x += 1
        if self.direction != "right":
            self.sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]
            self.direction = "right"

    def pos_x(self):
        return self.x

    def pos_y(self):
        return self.y

    def facing(self):
        return self.direction

    def check_exit(self):
        if self.y > 500:
            sys.exit()

    def bullet(self, speed, distance):
        self.reload += 0.05
        if self.reload >= 5:
            bullet = Bullet(self.rect.right + distance, self.rect.centery, speed)
            bullet_group.add(bullet)
            self.reload = 0

    def reduce_health(self):
        if self.health.hp == 0:
            self.kill()
        self.health.reduce_hp()


moving_sprites = pygame.sprite.Group()
player = Player(200, 100, 25)
player_2 = Player(500, 100, 925, 'enemy/run/')
moving_sprites.add(player)
moving_sprites.add(player_2)
bullet_group = pygame.sprite.Group()


def draw_window(background, plattform):
    WIN.blit(BG, (background.x, background.y))
    WIN.blit(plattform_img, (plattform.x, plattform.y))
    moving_sprites.draw(WIN)
    moving_sprites.update()
    bullet_group.draw(WIN)
    bullet_group.update()
    for entity in moving_sprites:
        entity.health.draw(WIN)
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
        player_2.update()

        player.gravity()
        player_2.gravity()
        player.check_exit()
        player_2.check_exit()
        while player.pos_y() > 480 and 156 < player.pos_x() < 990:
            player.y = 480
            player.velocity = 0
            player.is_jump = True

        while player_2.pos_y() > 480 and 156 < player_2.pos_x() < 990:
            player_2.y = 480
            player_2.velocity = 0
            player_2.is_jump = True

        bullet_player_collision = pygame.sprite.groupcollide(bullet_group, moving_sprites, True, False)
        for bullet, players in bullet_player_collision.items():
            for hit_player in players:
                hit_player.reduce_health()
                print('Collision')

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
            if player.facing() == 'right':
                player.bullet(1, 20)
            if player.facing() == 'left':
                player.bullet(-1, -48)

        if keys_pressed[pygame.K_UP]:
            player_2.jump()
        if keys_pressed[pygame.K_LEFT]:
            player_2.animate()
            player_2.left()
        if keys_pressed[pygame.K_RIGHT]:
            player_2.animate()
            player_2.right()
        if keys_pressed[pygame.K_p]:
            if player_2.facing() == 'right':
                player_2.bullet(1, 20)
            if player_2.facing() == 'left':
                player_2.bullet(-1, -48)


if __name__ == '__main__':
    main()
