import pygame
from circleshape import CircleShape
from constants import (PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS,
                       INITIAL_PLAYER_X, INITIAL_PLAYER_Y, ASTEROID_MIN_RADIUS, ASTEROID_MAX_REWARD, ASTEROID_REWARD_DIFF)
from shot import Shot
from triangle import triangle

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.score:int = 0
        self.num_lives = 3

    # in the Player class
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", triangle(self.position, self.rotation, self.radius), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shoot_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt: float) -> None:
        shift = pygame.Vector2(0, 1).rotate(self.rotation)
        shift *= PLAYER_SPEED * dt
        self.position += shift

    def shoot(self) -> None:
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_position = self.position + forward * self.radius
        shot = Shot(shot_position[0], shot_position[1])
        shot.velocity = forward * PLAYER_SHOOT_SPEED

    def loose_life(self) -> None:
        self.num_lives -= 1
        self.position = pygame.Vector2(INITIAL_PLAYER_X, INITIAL_PLAYER_Y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0

    def add_score(self, asteroid_radius: float) -> None:
        asteroid_kind = int(asteroid_radius / ASTEROID_MIN_RADIUS)
        reward = ASTEROID_MAX_REWARD - ASTEROID_REWARD_DIFF * asteroid_kind
        self.score += reward