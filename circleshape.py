import pygame
from triangleshape import TriangleShape


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass

    def collides_with_circle(self, circle: "CircleShape") -> bool:
        distance = self.position.distance_to(circle.position)
        return distance <= self.radius + circle.radius

    def collides_with_triangle(self, triangle: TriangleShape) -> bool:
        a, b, c = triangle.get_points()
        sides = ((a, b), (b, c), (c, a))
        for side in sides:
            if self.collides_with_line_segment(side[0], side[1]):
                return True
        return False

    def distance_to_line(self, a: pygame.Vector2, b: pygame.Vector2) -> float:
        ab = b - a
        normal = pygame.Vector2(-ab[1], ab[0]).normalize()
        ao = self.position - a
        return abs(normal.dot(ao))

    def collides_with_line_segment(self, a: pygame.Vector2, b: pygame.Vector2) -> bool:
        if (self.position.distance_to(a) <= self.radius
           or self.position.distance_to(b) <= self.radius):
            return True
        if self.distance_to_line(a, b) > self.radius:
            return False
        
        ab = b - a
        ao = self.position - a
        bo = self.position - b
        if ao.dot(ab) * bo.dot(ab) < 0:
            return True