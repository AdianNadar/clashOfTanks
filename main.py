import pygame
import sys
import math

from ammo import TestAmmo, HeavyShot, LongShot

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
    def __init__(self, x, imageFile, colour, speed, name):
        self.x      = x
        self.y      = groundY - tankH
        self.colour = colour
        self.speed  = speed
        self.fuelLevel = 100
        self.name = name
        self.turretAngle = 90  # straight up
        self.turretLength = 40

        #tank sprite two copies since rotation from original always
        self.original_image = pygame.image.load(imageFile).convert_alpha()
        self.image = self.original_image


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
        #bullet = HeavyShot(tipX, tipY, (dx, dy))
        bullet = LongShot(tipX, tipY, (dx, dy))


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
    x = int(bullet.x / SCALE)
    y = int(bullet.y / SCALE)

    if 0 <= x < terrain.get_width() and 0 <= y < terrain.get_height():
        if terrain.get_at((x, y)) == (0, 0, 0):  # black = ground
            createExplosion(x, y, terrain, bullet.impactStrength)
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
            createExplosion(bullet.x / SCALE, bullet.y / SCALE, terrain, bullet.impactStrength)
            bullet.alive = False
            bullet.onTankHit(tank)
            return True

    return False


# ── Apply gravity to terrain (fall logic) ──────────────────

def applyTerrainGravity(terrain):
    width = terrain.get_width()
    height = terrain.get_height()

    for x in range(width):
        for y in range(height - 2, -1, -1):  # from bottom up

            current = terrain.get_at((x, y))
            below = terrain.get_at((x, y + 1))

            # if ground pixel with empty below → fall
            if current == (0, 0, 0) and below == (255, 255, 255):
                terrain.set_at((x, y), (255, 255, 255))   # remove
                terrain.set_at((x, y + 1), (0, 0, 0))     # move down







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
    scaledTerrain = pygame.transform.scale(terrain, (screenW, screenH))
    surface.blit(scaledTerrain, (0, 0))

def renderTank(surface, tank):

    # draw sprite for tank body
    rotated = pygame.transform.rotate(tank.original_image, 0)  # 0 for now, slope angle later
    rect = rotated.get_rect(center=(tank.x, tank.y + tankH // 2))
    surface.blit(rotated, rect.topleft)


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

global SCALE

def main():

    # KEY VARIABLES

    global SCALE
    SCALE = 5
    terrainW = screenW // SCALE
    terrainH = screenH // SCALE
    terrainFallTimer = 0
    terrainFallDelay = 250  # milliseconds

#── Pygame init start ─────────────────────

    pygame.init()
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption("Tank Game")
    clock = pygame.time.Clock()

 # ── Terrain setup ─────────────────────

    terrain = pygame.Surface((terrainW, terrainH))
    terrain.fill(white)

    pygame.draw.rect(
        terrain,
        black,
        (0, groundY // SCALE, terrainW, (screenH - groundY) // SCALE)
    )

# ── Tanks ────────────────────────────

    tanks = [
        Tank(x=150,         imageFile = "tankBodyImages/tankRed.png", colour=red,  speed=5, name ="Tank1(Red)"), #tank1
        Tank(x=screenW-150, imageFile = "tankBodyImages/tankBlue.png", colour=blue, speed=5, name ="Tank2(Blue)"), #tank2

    ]

    bullets = []

    currentTurn = 0

    # ──── Running Loop ─────────────

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

        #terrain falling logic
        terrainFallTimer += clock.get_time()

        if terrainFallTimer > terrainFallDelay:
            for i in range(3):
                applyTerrainGravity(terrain)
            terrainFallTimer = 0


        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()