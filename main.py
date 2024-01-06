import pygame

pygame.init()
pygame.font.init()
SCREEN_WIGHT, SCREEN_HEIGHT = 1150, 750
WIN = pygame.display.set_mode((SCREEN_WIGHT, SCREEN_HEIGHT))
BG = pygame.transform.scale(pygame.image.load('pics/background.png'), (SCREEN_WIGHT, SCREEN_HEIGHT))
pygame.display.set_caption('Smashbros on wish')

"""race_track_img = pygame.image.load('pics/race_track.png')
race_track = pygame.transform.scale(race_track_img, (SCREEN_WIGHT, SCREEN_HEIGHT))
race_track_mask = pygame.mask.from_surface(race_track)
finish_line_img = pygame.image.load('pics/finish_line.png')
finish_line = pygame.transform.scale(finish_line_img, (135, 14))
finish_mask = pygame.mask.from_surface(finish_line)
mask = finish_mask.to_surface()"""


def draw_window(background):
    WIN.blit(BG, (background.x, background.y))
    pygame.display.flip()


def main():
    background = pygame.Rect(0, 0, SCREEN_WIGHT, SCREEN_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_window(background)


if __name__ == '__main__':
    main()
