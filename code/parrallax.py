import pygame
from settings import screen_width, screen_height

class ParallaxBackground:
    def __init__(self, image_paths):
        self.layers = []
        self.parallax_speeds = [0.1, 0.2, 0.3, 0.4, 0.5]  # Adjust these values for desired effect
        
        for path in image_paths:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (screen_width, screen_height))
            self.layers.append(image)
        
        self.layer_width = self.layers[0].get_width()
        self.scroll = [0] * len(self.layers)

    def update(self, world_shift):
        for i in range(len(self.layers)):
            self.scroll[i] += world_shift * self.parallax_speeds[i]
            self.scroll[i] %= self.layer_width

    def draw(self, surface):
        for i, layer in enumerate(self.layers):
            surface.blit(layer, (-self.scroll[i], 0))
            surface.blit(layer, (self.layer_width - self.scroll[i], 0))