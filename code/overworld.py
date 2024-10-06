import pygame 
from game_data import levels
from support import import_folder
from decoration import Sky
from menu import Button
from menu import BGImage

class Node(pygame.sprite.Sprite):
	def __init__(self,pos,status,icon_speed,path):
		super().__init__()
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		if status == 'available':
			self.status = 'available'
		else:
			self.status = 'locked'
		self.rect = self.image.get_rect(center = pos)

		self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self):
		if self.status == 'available':
			self.animate()
		else:
			tint_surf = self.image.copy()
			tint_surf.fill('black',None,pygame.BLEND_RGBA_MULT)
			self.image.blit(tint_surf,(0,0))

class Icon(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.pos = pos
		self.image = pygame.image.load('./graphics/overworld/hat.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self):
		self.rect.center = self.pos

class Overworld:
	def __init__(self,start_level,max_level,surface,create_level):

		# setup 
		self.display_surface = surface 
		self.max_level = max_level
		self.current_level = start_level
		self.create_level = create_level
		# mainmenu
		menu_image = pygame.image.load("./graphics/ui/LFFHMM.png")
		self.mi = Button(-60, -10, menu_image)
  
		play_image = pygame.image.load("./graphics/ui/PLAY.png")
		self.play = Button(350, 200, play_image)
  
		# level one
		bg_image = pygame.image.load("./graphics/ui/bg.png")
		self.bg = Button(-60, -10, bg_image)
		level_1 = pygame.image.load("./graphics/ui/level1.png")
		self.level1 = BGImage(325, 180, level_1)
		RA_image = pygame.image.load("./graphics/ui/ArrowRight.png")
		self.RA = BGImage (775, 225, RA_image)
  
		#level two
		bg2_image = pygame.image.load("./graphics/ui/bg_2.jpg")
		self.bg2 = Button (0,-320, bg2_image)
		level_2 = pygame.image.load("./graphics/ui/level2.png")
		self.level2 = BGImage(325, 180, level_2)
		LA_image = pygame.image.load("./graphics/ui/ArrowLeft.png")
		self.LA = BGImage (20, 225, LA_image)
  
		# movement logic
		self.moving = False
		self.move_direction = pygame.math.Vector2(0,0)
		self.speed = 8

		# sprites 
		self.setup_nodes()
		self.setup_icon()
		self.sky = Sky(8,'overworld')

		# time 
		self.start_time = pygame.time.get_ticks()
		self.allow_input = False
		self.timer_length = 300


		self.oneyes = False
		self.twoyes = False

		# options
		opt_image = pygame.image.load("./graphics/ui/HTP.png")
		self.opt = Button(260, 300, opt_image)
		instruct_image = pygame.image.load("./graphics/ui/instructions.png")
		self.instruct = Button(40, 200, instruct_image)
		arrows_image = pygame.image.load("./graphics/ui/ARROWS.png")
		self.arrows = Button(210, 175, arrows_image)
		back_image = pygame.image.load("./graphics/ui/BACK.png")
		self.back = Button(360, 400, back_image)
  
		#adfs
		self.show_buttons = True
		self.options_menu = False
		self.main_menu = True

	def setup_nodes(self):
		self.nodes = pygame.sprite.Group()

		for index, node_data in enumerate(levels.values()):
			if index <= self.max_level:
				node_sprite = Node(node_data['node_pos'],'available',self.speed,node_data['node_graphics'])
			else:
				node_sprite = Node(node_data['node_pos'],'locked',self.speed,node_data['node_graphics'])
			self.nodes.add(node_sprite)

	def draw_paths(self):
		if self.max_level > 0:
			points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
			pygame.draw.lines(self.display_surface,'#a04f45',False,points,6)

	def setup_icon(self):
		self.icon = pygame.sprite.GroupSingle()
		icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
		self.icon.add(icon_sprite)

	def input(self):
		keys = pygame.key.get_pressed()

		if not self.moving and self.allow_input and self.main_menu == False:
			if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
				self.move_direction = self.get_movement_data('next')
				self.current_level += 1
				self.moving = True
				self.twoyes = True
				self.oneyes = False
			elif keys[pygame.K_LEFT] and self.current_level > 0:
				self.move_direction = self.get_movement_data('previous')
				self.current_level -= 1
				self.moving = True
				self.oneyes = True
				self.twoyes = False
			elif keys[pygame.K_SPACE]:
				self.create_level(self.current_level)

	def get_movement_data(self,target):
		start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
		
		if target == 'next': 
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
		else:
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

		return (end - start).normalize()

	def update_icon_pos(self):
		if self.moving and self.move_direction:
			self.icon.sprite.pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_level]
			if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
				self.moving = False
				self.move_direction = pygame.math.Vector2(0,0)

	def input_timer(self):
		if not self.allow_input:
			current_time = pygame.time.get_ticks()
			if current_time - self.start_time >= self.timer_length:
				self.allow_input = True

	def check_press(self):
		if self.back.check_pressed() and self.main_menu and self.options_menu == True:
			self.options_menu = False
			self.show_buttons = True
     
		if self.opt.check_pressed() and self.main_menu and self.options_menu == False:
			self.options_menu = True
			self.show_buttons = False
     
     
		if self.play.check_pressed() and self.main_menu:
			self.main_menu = False
			if self.current_level == 0:
				self.oneyes = True
				self.twoyes = False
			elif self.current_level == 1:
				self.oneyes = False
				self.twoyes = True
   


	def run(self):
		self.input_timer()
		self.input()
		self.update_icon_pos()
		self.icon.update()
		self.nodes.update()

		self.draw_paths()
		self.icon.draw(self.display_surface)

		if self.main_menu:
			self.mi.draw(self.display_surface)
			if self.show_buttons:
				self.play.draw(self.display_surface)
				self.opt.draw(self.display_surface)

		self.check_press()
		if self.oneyes:
			self.bg.draw(self.display_surface)
			self.level1.draw(self.display_surface)
			if self.max_level == 1:
				self.RA.draw(self.display_surface)

		if self.twoyes:
			self.bg2.draw(self.display_surface)
			self.level2.draw(self.display_surface)
			self.LA.draw(self.display_surface)
   
		if self.options_menu:
			self.instruct.draw(self.display_surface)
			self.arrows.draw(self.display_surface)
			self.back.draw(self.display_surface)