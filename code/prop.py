
""" NPC sprites: props, weapons and enemies """

import pygame
from graphics import TILESIZE, WIDTH, HEIGHT, bone_weapon_data
from math import atan2, degrees

# static background props

class Prop(pygame.sprite.Sprite):
	def __init__(self,pos,groups,surface = pygame.Surface((TILESIZE,TILESIZE)), inflatex = 0, inflatey = 0):
		super().__init__(groups)
		self.image = surface
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(inflatex, inflatey)





# player weapons

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, weapontype, offset_fix_x = 16, offset_fix_y = 0):
        super().__init__(groups)

        self.player = player
        self.distance_from_player = 60
        self.distance_from_player_offset = pygame.math.Vector2(offset_fix_x, offset_fix_y)
        self.player_direction = pygame.Vector2(1,0)
        

        self.weapon = bone_weapon_data[weapontype]['png']
        self.weapon_surface = pygame.image.load(self.weapon).convert_alpha()
        self.weapon_surface = pygame.transform.scale_by(self.weapon_surface, 2)
        self.image = self.weapon_surface
        self.rect = self.image.get_rect(center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * self.distance_from_player)

class StaticWeapon(Weapon):
    def __init__(self, player, groups, weapontype):
        super().__init__(player, groups, weapontype)

        self.distance_from_player = 30

    def update(self):

        if 'right' in self.player.status:
            self.rect.center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * (self.distance_from_player * - 1)
        else:
            self.rect.center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * self.distance_from_player

class CQCWeapon(Weapon):
    def __init__(self, player, groups, weapontype):
        super().__init__(player, groups, weapontype)

        self.distance_from_player = 80
        self.cqc_distance_from_player_offset = pygame.math.Vector2(32,0)
        
    def update(self):
        self.weapon_direction()
        self.rotate_weapon()
        self.rect.center = self.player.rect.center + self.distance_from_player_offset - self.cqc_distance_from_player_offset + self.player_direction * self.distance_from_player

    def weapon_direction(self):
        direction = (pygame.math.Vector2(pygame.mouse.get_pos()) - pygame.math.Vector2(WIDTH / 2, HEIGHT / 2))
        self.player_direction = direction.normalize()
        
    def rotate_weapon(self):
        mouse_angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 180
        self.image = pygame.transform.rotozoom(self.weapon_surface, mouse_angle, 1)
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.weapon_surface, mouse_angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.weapon_surface, (mouse_angle * -1), 1)
            self.image = pygame.transform.flip(self.image, True, False)





class Projectile(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction = (pygame.math.Vector2(pygame.mouse.get_pos()) - pygame.math.Vector2(WIDTH / 2, HEIGHT / 2))
        self.direction = direction.normalize()
        self.speed = 5
        
        self.image = pygame.Surface((40,40))
        self.image.fill((0,0,0))

        self.rect = self.image.get_rect(center = player.rect.center + self.direction * 50)

    def update(self):
        # Move the weapon in the direction of the mouse
        self.rect.center += self.direction * self.speed