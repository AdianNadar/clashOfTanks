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
    def __init__(self, x, colour, speed, name):
        self.x      = x
        self.y      = groundY - tankH
        self.colour = colour
        self.speed  = speed
        self.fuelLevel = 100
        self.name = name


    @property
    def rect(self):
        return pygame.Rect(self.x - tankW // 2, self.y, tankW, tankH)

    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(tankW // 2, min(screenW - tankW // 2, self.x))

    def shoot(self):
        print("SHOOT (not yet implemented)")

    def aimTurret(self):
        print("Not implemented")

    def changeAmmo(self): #roll though existing ammo ike caroselle
        print("Not implemented")

    def showName(self):
        print(f"Current Tank: {self.name}")

    def showFuelLevel(self):
        if self.fuelLevel > 0:
            print(f"Fuel level: {self.fuelLevel} ")
        else: print("No fuel!")

    def useFuelUnit(self,unitLevel):
        if self.fuelLevel > 0:
            self.fuelLevel -= unitLevel
        else: pass




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

        if event.key == pygame.K_f:
            activeTank.showFuelLevel()

        if event.key == pygame.K_n:
            activeTank.showName()

    return currentTurn


def handleMovement(tanks, currentTurn):
    #called every frame
    keys = pygame.key.get_pressed()
    activeTank = tanks[currentTurn]

    #movement
    if activeTank.fuelLevel != 0:
        if keys[pygame.K_LEFT]:
            activeTank.move(-1)
            activeTank.useFuelUnit(1)
        if keys[pygame.K_RIGHT]:
            activeTank.move(1)
            activeTank.useFuelUnit(1)



# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption("Tank Game")
    clock = pygame.time.Clock()

    tanks = [
        Tank(x=150,         colour=red,  speed=5, name ="Tank1"), #tank1
        Tank(x=screenW-150, colour=blue, speed=5, name ="Tank2"), #tank2
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