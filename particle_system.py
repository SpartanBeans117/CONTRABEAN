# particle_system.py
import pygame, random

class ParticleSystem:
    def __init__(self, x, y, count=20, lifetime=30, speed=3, color=(200,200,200)):
        self.particles = []
        self.color = color

        # Crear todas las partículas de golpe
        for _ in range(count):
            vx = random.uniform(-speed, speed)
            vy = random.uniform(-speed, 0)
            self.particles.append([x, y, vx, vy, lifetime])

    def update(self):
        for p in self.particles:
            p[0] += p[2]   # mover en X
            p[1] += p[3]   # mover en Y
            p[3] += 0.2    # gravedad ligera
            p[4] -= 1      # reducir vida

        # eliminar las que ya murieron
        self.particles = [p for p in self.particles if p[4] > 0]

    def draw(self, pantalla):
        for p in self.particles:
            pygame.draw.circle(pantalla, self.color, (int(p[0]), int(p[1])), 3)

    def is_alive(self):
        return len(self.particles) > 0
