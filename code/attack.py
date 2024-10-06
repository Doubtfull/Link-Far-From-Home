import pygame

class Attack(pygame.sprite.Sprite):
    def __init__(self, rect, flipped, damage):
        super().__init__()
        self.lifetime = 0.1
        self.rect = pygame.Rect(rect)
        self.damage = damage
        if flipped:
            self.rect.right = self.rect.left

    def update(self):
        self.lifetime -= 1 / 60
        if self.lifetime <= 0:
            self.kill()