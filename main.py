import pygame
import sys
import math

from ammo import TestAmmo, HeavyShot

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
        self.turretAngle = 90  # straight up
        self.turretLength = 40


    @property
    def rect(self):
        return pygame.Rect(self.x - tankW // 2, self.y, tankW, tankH)

    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(tankW // 2, min(screenW - tankW // 2, self.x))

    #SHOOT method
    def shoot(self):
        # get turret direction (unit vector)
        dx, dy = self.getTurretDirection()
        # turret base (top center of tank)
        baseX = self.x
        baseY = self.y
        # tip of the turret
        tipX = baseX + dx * self.turretLength
        tipY = baseY + dy * self.turretLength


        # create bullet at the tip
        #bullet = TestAmmo(tipX, tipY, (dx, dy))
        bullet = HeavyShot(tipX, tipY, (dx, dy))


        print(f"{self.name} fired from ({round(tipX)}, {round(tipY)})")

        return bullet


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

    def showTurretAngle(self):
        print(f"Turret angle: {self.turretAngle}")

    #adjust turret angle
    def adjustTurret(self, direction):
        self.turretAngle += direction
        self.turretAngle = max(0, min(180, self.turretAngle))

    def getTurretDirection(self):
        rad = math.radians(self.turretAngle)
        dx = math.cos(rad)
        dy = -math.sin(rad)  # negative because pygame y goes down
        return dx, dy


# ──────── Terrain collision helper ─────────────────────────────────────────────────────────────────

def handleBulletTerrainCollision(bullet, terrain):
    x = int(bullet.x)
    y = int(bullet.y)

    if 0 <= x < terrain.get_width() and 0 <= y < terrain.get_height():
        if terrain.get_at((x, y)) == (0, 0, 0):  # black = ground
            createExplosion(x, y, terrain, 25)
            bullet.alive = False
            bullet.onImpact()
            return True

    return False

# ──────── Tank and ammo collision helper ────────────────────────

def handleBulletTankCollision(bullet, tanks, terrain):
    bulletRect = pygame.Rect(
        bullet.x - bullet.collisionRadius,
        bullet.y - bullet.collisionRadius,
        bullet.collisionRadius * 2,
        bullet.collisionRadius * 2
    )

    for tank in tanks:
        if bulletRect.colliderect(tank.rect):
            # explosion at tank hit
            createExplosion(bullet.x, bullet.y, terrain, 25)
            bullet.alive = False
            bullet.onTankHit(tank)
            return True

    return False

# ── Explosion logic ──────────────────

def createExplosion(x, y, terrain, radius):
    # destroy terrain
    pygame.draw.circle(
        terrain,
        (255, 255, 255),  # white = air
        (int(x), int(y)),
        radius
    )




# ── Rendering ─────────────────────────────────────────────────────────────────

def renderBackground(surface, terrain):
    surface.fill(white)  # sky
    surface.blit(terrain, (0, 0))

def renderTank(surface, tank):

    # tank body
    pygame.draw.rect(surface, tank.colour, tank.rect)
    pygame.draw.rect(surface, black, tank.rect, 2)

    # turret base (top center of tank)
    baseX = tank.x
    baseY = tank.y
    dx, dy = tank.getTurretDirection()
    endX = baseX + dx * tank.turretLength
    endY = baseY + dy * tank.turretLength
    pygame.draw.line(surface, black, (baseX, baseY), (endX, endY), 4)


# ── Input handling ────────────────────────────────────────────────────────────
def handleInput(event, tanks, currentTurn,bullets):
    if event.type == pygame.KEYDOWN:
        activeTank = tanks[currentTurn]

        if event.key == pygame.K_s:
            bullet = activeTank.shoot()
            bullets.append(bullet)
            currentTurn = (currentTurn + 1) % len(tanks)

        if event.key == pygame.K_f:
            activeTank.showFuelLevel()

        if event.key == pygame.K_n:
            activeTank.showName()

        if event.key == pygame.K_v:
            activeTank.showTurretAngle()

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

        if keys[pygame.K_q]:
            activeTank.adjustTurret(-1)
        if keys[pygame.K_e]:
            activeTank.adjustTurret(1)



# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption("Tank Game")
    clock = pygame.time.Clock()

 # ── Terrain setup ─────────────────────
    terrain = pygame.Surface((screenW, screenH))
    terrain.fill(white)  # sky
    pygame.draw.rect(terrain, black, (0, groundY, screenW, screenH - groundY))

# ── Tanks ────────────────────────────

    tanks = [
        Tank(x=150,         colour=red,  speed=5, name ="Tank1(Red)"), #tank1
        Tank(x=screenW-150, colour=blue, speed=5, name ="Tank2(Blue)"), #tank2

    ]

    bullets = []

    currentTurn = 0

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            currentTurn = handleInput(event, tanks, currentTurn, bullets)

        handleMovement(tanks, currentTurn)

        renderBackground(screen, terrain)
        for tank in tanks:
            renderTank(screen, tank)

        for bullet in bullets:
            bullet.update()

            #bullet collision handling
            hitTank = handleBulletTankCollision(bullet, tanks, terrain)
            if not hitTank:
                handleBulletTerrainCollision(bullet, terrain)


            bullet.draw(screen)


        bullets = [b for b in bullets if b.alive]
        #removes bullets that are not alive (collided)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()