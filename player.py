import circle_shape
import constants
from circle_shape import CircleShape
import pygame
from shot import Shot

from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y,constants.PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown_timer = 0.3


    # in the Player class
# in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self,dt):
        self.rotation += dt * constants.PLAYER_TURN_SPEED

    def update(self, dt):
        if self.shoot_cooldown_timer > 0:
            self.shoot_cooldown_timer = max(0, self.shoot_cooldown_timer - dt)

        keys = pygame.key.get_pressed()

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

    def move(self,dt):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * dt * constants.PLAYER_SPEED
        self.position += rotated_with_speed_vector

    # Add the draw method here
    def draw(self, screen):
        pygame.draw.polygon(
            screen,               # 1. The screen object
            "white",              # 2. A color
            self.triangle(),      # 3. A list of points
            constants.LINE_WIDTH  # 4. A line width
        )

    def shoot(self):

        if self.shoot_cooldown_timer > 0:
            return

        self.shoot_cooldown_timer = constants.PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y, self.radius)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * constants.PLAYER_SHOOT_SPEED