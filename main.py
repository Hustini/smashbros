import pygame

pygame.init()
pygame.font.init()
SCREEN_WIGHT, SCREEN_HEIGHT = 1150, 750
WIN = pygame.display.set_mode((SCREEN_WIGHT, SCREEN_HEIGHT))
BG = pygame.transform.scale(pygame.image.load('pics/background.png'), (SCREEN_WIGHT, SCREEN_HEIGHT))
pygame.display.set_caption('Smashbros on wish')

plattform_img = pygame.image.load('pics/plattform.png')


def draw_window(background, plattform):
    WIN.blit(BG, (background.x, background.y))
    WIN.blit(plattform_img, (plattform.x, plattform.y))
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


if __name__ == '__main__':
    main()
