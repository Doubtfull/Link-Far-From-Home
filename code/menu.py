import pygame


class Button:
  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect(x=x, y=y)

  def check_pressed(self) -> bool:
    return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
      pygame.mouse.get_pos()
    )

  def draw(self, surface):
    surface.blit(self.image, self.rect)
    
    
class BGImage:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(x=x, y=y)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)