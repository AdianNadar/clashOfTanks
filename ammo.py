import pygame
import math



class Ammo:
    # Shared launch force for all ammo (can tweak later)
    LAUNCH_FORCE = 12
    GRAVITY = 0.4
    GROUND_Y = 420

    def __init__(self, x, y, direction, name, description,
                 velocity, weight, impactStrength, collisionRadius):

        self.x = x
        self.y = y

        # direction = (dx, dy) from turret
        dx, dy = direction

        # initial velocity based on turret direction + launch force
        self.vx = dx * self.LAUNCH_FORCE * velocity
        self.vy = dy * self.LAUNCH_FORCE * velocity

        self.name = name
        self.description = description
        self.velocity = velocity
        self.weight = weight
        self.impactStrength = impactStrength
        self.collisionRadius = collisionRadius

        self.alive = True

    def update(self):
        """Update position with simple physics"""
        # gravity affected by weight
        self.vy += self.GRAVITY * self.weight

        self.x += self.vx
        self.y += self.vy

        self.checkBulletStatus()


    def draw(self, surface):
        """Default draw (circle)"""
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (int(self.x), int(self.y)),
            self.collisionRadius
        )

    def checkCollision(self):
        """Basic ground collision"""
        if self.y >= self.GROUND_Y:
            self.alive = False
            self.onImpact()
            return True
        return False

    def onImpact(self):
        """Override in subclasses"""
        print(f"{self.name} impacted with strength {self.impactStrength}")

    def checkBulletStatus(self):
        self.checkCollision()



# ── Test Ammo ────────────────────────────────────────────────────────────────
class TestAmmo(Ammo):
    def __init__(self, x, y, direction):
        super().__init__(
            x=x,
            y=y,
            direction=direction,
            name="Test Bullet",
            description="Basic test projectile",
            velocity=1.0,          # multiplier
            weight=1.0,            # affects gravity
            impactStrength=10,
            collisionRadius=4
        )
