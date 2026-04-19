import pygame
import sys

# ── Constants ─────────────────────────────────────────────────────────────────
screenW, screenH = 900, 500
fps = 60
groundY = screenH - 80
tankW, tankH = 60, 30

# Colours
white     = (255, 255, 255)
black     = (0,   0,   0)
darkGrey  = (30,  30,  30)
midGrey   = (120, 120, 120)
lightGrey = (200, 200, 200)
red       = (210, 40,  40)
blue      = (40,  80,  210)


# ── Tank class ────────────────────────────────────────────────────────────────
class Tank:
    def __init__(self, x, colour, speed):
        self.x      = x
        self.y      = groundY - tankH
        self.colour = colour
        self.speed  = speed

    @property
    def rect(self):
        return pygame.Rect(self.x - tankW // 2, self.y, tankW, tankH)

    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(tankW // 2, min(screenW - tankW // 2, self.x))

    def shoot(self):
        print("SHOOT (not yet implemented)")


# ── Rendering ─────────────────────────────────────────────────────────────────
def renderBackground(surface):
    surface.fill(lightGrey)
    pygame.draw.rect(surface, darkGrey, pygame.Rect(0, groundY, screenW, screenH - groundY))
    pygame.draw.line(surface, midGrey, (0, groundY), (screenW, groundY), 3)


def renderTank(surface, tank):
    pygame.draw.rect(surface, tank.colour, tank.rect)
    pygame.draw.rect(surface, black, tank.rect, 2)


# ── Input handling ────────────────────────────────────────────────────────────
def handleInput(event, tanks, currentTurn):
    if event.type == pygame.KEYDOWN:
        activeTank = tanks[currentTurn]

        if event.key == pygame.K_s:
            activeTank.shoot()
            currentTurn = (currentTurn + 1) % len(tanks)

    return currentTurn


def handleMovement(tanks, currentTurn):
    #called every frame
    keys = pygame.key.get_pressed()
    activeTank = tanks[currentTurn]

    if keys[pygame.K_LEFT]:
        activeTank.move(-1)
    if keys[pygame.K_RIGHT]:
        activeTank.move(1)


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption("Tank Game")
    clock = pygame.time.Clock()

    tanks = [
        Tank(x=150,         colour=red,  speed=5), #tank1
        Tank(x=screenW-150, colour=blue, speed=5), #tank2
    ]

    currentTurn = 0

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            currentTurn = handleInput(event, tanks, currentTurn)

        handleMovement(tanks, currentTurn)

        renderBackground(screen)
        for tank in tanks:
            renderTank(screen, tank)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()