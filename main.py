import sys

import pygame
import constants
from logger import log_state
from logger import log_event
import player
import asteroid
import asteroidfield
from shot import Shot
def main():
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    asteroid.Asteroid.containers = (asteroids, updatable, drawable)
    player.Player.containers = (updatable, drawable)
    asteroidfield.AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)


    field = asteroidfield.AsteroidField()

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    player.Player.containers = (updatable, drawable)
    main_char = player.Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    # Frame updating
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update dt
        dt = clock.tick(60) / 1000

        # 1. Update everything in the updatable group
        updatable.update(dt)

        # 2. Fill the screen with black
        screen.fill("black")

        # 3. Draw everything in the drawable group
        for entity in drawable:
            entity.draw(screen)

        for asteroid_object in asteroids:
            if asteroid_object.collides_with(main_char):
                log_event("player_hit")
                print("Game over")
                sys.exit()

        for asteroid_object in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid_object):
                    log_event("asteroid_shot")
                    asteroid_object.split()
                    shot.kill()

        pygame.display.flip()

if __name__ == "__main__":
    main()
