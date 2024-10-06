import pygame 
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles,change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # ... (keep the existing initialization code)

        # Attack
        self.attacking = False
        self.attack_cooldown = 500  # milliseconds
        self.attack_time = 0
        self.attack_duration = 200  # milliseconds
        self.attack_frame_index = 0

        # ... (keep the rest of the __init__ method)

    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_input(self):
        keys = pygame.key.get_pressed()

        # ... (keep the existing input handling)

        if keys[pygame.K_LSHIFT] and not self.attacking:
            self.attack()

    def attack(self):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        self.attack_frame_index = 0

    def get_status(self):
        if self.attacking:
            self.status = 'attack'
        elif self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]

        # Handle attack animation separately
        if self.status == 'attack':
            self.attack_frame_index += self.animation_speed
            if self.attack_frame_index >= len(animation):
                self.attack_frame_index = 0
                self.attacking = False
            frame_index = int(self.attack_frame_index)
        else:
            # Normal animation for other states
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
            frame_index = int(self.frame_index)

        image = animation[frame_index]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        self.wave_value()

        # Check if attack is finished
        if self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_duration:
                self.attacking = False

    def get_attack_rect(self):
        if not self.attacking:
            return None
        
        if self.facing_right:
            return pygame.Rect(self.rect.right - 10, self.rect.y, 60, self.rect.height)
        else:
            return pygame.Rect(self.rect.left - 50, self.rect.y, 60, self.rect.height)