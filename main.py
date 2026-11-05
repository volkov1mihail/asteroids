import pygame, sys
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_X_LEFT, SCORE_Y_TOP, SCORE_FONT_SIZE, SCORE_FONT_PATH,
                       INITIAL_PLAYER_X, INITIAL_PLAYER_Y, LIVES_FONT_PATH, LIVES_FONT_SIZE, LIVES_CENTER_X_COORD,
                       LIVES_SHIFT_Y, LIVES_COUNTER_Y, LIVES_ROTATION, LIVES_RADIUS)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from triangle import Triangle

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids alpha version")
    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(INITIAL_PLAYER_X, INITIAL_PLAYER_Y)
    Shot.containers = (shots, updatable, drawable)

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    score_font = pygame.font.Font(SCORE_FONT_PATH, SCORE_FONT_SIZE)
    lives_font = pygame.font.Font(LIVES_FONT_PATH, LIVES_FONT_SIZE)
    text_height = score_font.get_height()
    lives_center_y = text_height + LIVES_SHIFT_Y
    Triangle.containers = (updatable, drawable)
    lives_symbol = Triangle(LIVES_CENTER_X_COORD, lives_center_y, LIVES_ROTATION, LIVES_RADIUS)

    while(True):
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        score_text = score_font.render(str(player.score), 1, "white")
        score_rect = score_text.get_rect(left=SCORE_X_LEFT, top=SCORE_Y_TOP)
        screen.blit(score_text, score_rect)


        lives_text = lives_font.render(str(player.num_lives), 1, "white")
        lives_rect = lives_text.get_rect(left=LIVES_CENTER_X_COORD + LIVES_RADIUS, top=LIVES_COUNTER_Y)
        screen.blit(lives_text, lives_rect)

        if player.num_lives <= 0:
            log_event("player_died")
            print("Game over!")
            sys.exit()

        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                player.loose_life()
                asteroid.split()

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    player.add_score(asteroid.radius)
                    asteroid.split()
                    shot.kill()

        for member in drawable:
            member.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
