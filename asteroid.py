import pygame, random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_SPLITTING_SPEED_MULT
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")
        spawn_angle = random.uniform(20, 50)
        new_velocity_pos = self.velocity.rotate(spawn_angle)
        new_velocity_neg = self.velocity.rotate(-spawn_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position[0], self.position[1], new_radius)
        asteroid_2 = Asteroid(self.position[0], self.position[1], new_radius)
        asteroid_1.velocity = new_velocity_pos * ASTEROID_SPLITTING_SPEED_MULT
        asteroid_2.velocity = new_velocity_neg * ASTEROID_SPLITTING_SPEED_MULT