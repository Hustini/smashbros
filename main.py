import pygame

pygame.init()
pygame.font.init()
SCREEN_WIGHT, SCREEN_HEIGHT = 1150, 750
WIN = pygame.display.set_mode((SCREEN_WIGHT, SCREEN_HEIGHT))
BG = pygame.transform.scale(pygame.image.load('pics/background.png'), (SCREEN_WIGHT, SCREEN_HEIGHT))
pygame.display.set_caption('Smashbros on wish')

plattform_img = pygame.image.load('pics/plattform.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        self.sprites.append(pygame.image.load('player/run/0.png'))
        self.sprites.append(pygame.image.load('player/run/1.png'))
        self.sprites.append(pygame.image.load('player/run/2.png'))
        self.sprites.append(pygame.image.load('player/run/3.png'))
        self.sprites.append(pygame.image.load('player/run/4.png'))
        self.sprites.append(pygame.image.load('player/run/5.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating is True:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]


moving_sprites = pygame.sprite.Group()
player = Player(100, 100)
moving_sprites.add(player)


def draw_window(background, plattform):
    WIN.blit(BG, (background.x, background.y))
    WIN.blit(plattform_img, (plattform.x, plattform.y))
    moving_sprites.draw(WIN)
    moving_sprites.update()
    pygame.display.flip()


def main():
    background = pygame.Rect(0, 0, SCREEN_WIGHT, SCREEN_HEIGHT)
    plattform = pygame.Rect(150, 500, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.animate()

        draw_window(background, plattform)


if __name__ == '__main__':
    main()
