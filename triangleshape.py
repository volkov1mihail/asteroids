import pygame
from constants import LINE_WIDTH

# def triangle(position:pygame.Vector2, rotation: float, radius: float) -> list[pygame.Vector2]:
#     forward = pygame.Vector2(0, 1).rotate(rotation)
#     right = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 1.5
#     a = position + forward * radius
#     b = position - forward * radius - right
#     c = position - forward * radius + right
#     return [a, b, c]

class TriangleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, rotation: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.rotation = rotation
        self.radius = radius

    def get_points(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.get_points(), LINE_WIDTH)

    # def collides_with_circle(self, circle: CircleShape) -> bool:
    #     pass