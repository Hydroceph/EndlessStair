
""" NPC sprites: props, weapons and enemies """

import pygame
from graphics import TILESIZE, WIDTH, HEIGHT, bone_weapon_data, png_collection, enemy_data
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

# magic weapon, always held behind player
class StaticWeapon(Weapon):
    def __init__(self, player, groups, weapontype):
        super().__init__(player, groups, weapontype)

        self.distance_from_player = 30

    def update(self):

        if 'right' in self.player.status:
            self.rect.center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * (self.distance_from_player * - 1)
        else:
            self.rect.center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * self.distance_from_player

# melee weapon, always held pointing towards mouse
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




# player magic attack
class Projectile(pygame.sprite.Sprite):
    def __init__(self,player,groups, obstacle_sprites, destructable_sprites, damageable_sprites):
        super().__init__(groups)
        direction = (pygame.math.Vector2(pygame.mouse.get_pos()) - pygame.math.Vector2(WIDTH / 2, HEIGHT / 2))
        self.direction = direction.normalize()
        self.speed = 5
        
        self.image = pygame.Surface((40,40))
        self.image.fill((0,0,0))

        self.rect = self.image.get_rect(center = player.rect.center + self.direction * 50)
        self.rect_collision = self.rect.inflate(-4, -4)

        self.obstacle_sprites = obstacle_sprites
        self.destructable_sprites = destructable_sprites
        self.damageable_sprites = damageable_sprites

    def update(self):
        # Move the weapon in the direction of the mouse
        self.rect_collision.center += self.direction * self.speed
        self.rect.center = self.rect_collision.center

        for sprite in self.obstacle_sprites:
            if sprite.rect_collision.colliderect(self.rect_collision):
                self.kill()

        for sprite in self.damageable_sprites:
            print('hello')
            if sprite.rect_collision.colliderect(self.rect_collision):
                self.kill()

        for sprite in self.destructable_sprites:
            if sprite.rect_collision.colliderect(self.rect_collision):
                sprite.kill()
                self.kill()




# enemy sprites, with character super class (which is also the superclass for the player)
class Character(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self,speed):
            # diagonal movement
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # movement with collision check
            self.rect_collision.y += self.direction.y * speed
            self.collision('vertical')
            self.rect_collision.x += self.direction.x * speed
            self.collision('horizontal')
            self.rect.center = self.rect_collision.center

    def collision(self,direction):
            # up/down collision
            if direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.rect_collision.colliderect(self.rect_collision):
                        # moving down
                        if self.direction.y > 0:
                            self.rect_collision.bottom = sprite.rect_collision.top
                        # moving up
                        if self.direction.y < 0:
                            self.rect_collision.top = sprite.rect_collision.bottom

            # left/right collision
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.rect_collision.colliderect(self.rect_collision):
                        # moving right
                        if self.direction.x > 0:
                            self.rect_collision.right = sprite.rect_collision.left
                        # moving left
                        if self.direction.x < 0:
                            self.rect_collision.left = sprite.rect_collision.right


class Enemy(Character):
    def __init__(self, groups, obstacle_sprites, enemy_type, pos):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        self.image_list = png_collection(enemy_data[enemy_type]['graphics'])
        self.image = self.image_list[self.frame_index]
        self.image = pygame.transform.scale_by(self.image, 3)

        self.rect = self.image.get_rect(topleft = pos)
        self.rect_collision = self.rect.inflate(-8, -16)
        self.obstacle_sprites = obstacle_sprites
        self.status = 'slow_move'

        # stats
        self.enemy_type = enemy_type
        enemy_info = enemy_data[self.enemy_type]
        self.speed = enemy_info['speed']
        self.animation_direction = 'right'
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.attack_type = enemy_info['attack_type']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.can_attack = True
        self.last_attack_time = None
        self.enemy_cooldown_time = 400
    


    def direction_check(self, player):
        player_position = pygame.math.Vector2(player.rect.center)
        enemy_position = pygame.math.Vector2(self.rect.center)
        distance = (player_position - enemy_position).magnitude()
        if distance > 0:
            direction = (player_position - enemy_position).normalize()
        else:
            direction = pygame.math.Vector2()

        if distance <= self.attack_radius:
            self.speed = 3
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.speed = 3
            self.status = 'move'
        else:
            self.speed = 1
            self.status = 'slow_move'

        if direction.x >= 0:
            self.animation_direction = 'right'
        else:
            self.animation_direction = 'left'
        

        return direction

    def get_damage(self, player, attack_type):
        if attack_type == 'magic':
            self.health -= player.get_weapon_damage()[0]

    def check_heatlh(self):
        if self.health <= 0:
            self.kill()

    def enemy_update(self, player):
        self.direction_check(player)
        self.chase(player)

    def chase(self,player):
        if self.status == 'attack' and self.can_attack == True:
            print('attack')
            self.can_attack = False
            self.last_attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.direction_check(player)
        else: # slow move, (lower self.speed)
            self.direction = self.direction_check(player)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.image_list):
            self.frame_index = 0
        self.image = self.image_list[int(self.frame_index)]
        self.image = pygame.transform.scale_by(self.image, 3)
        if self.animation_direction == 'left':
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = self.rect_collision.center)

    def enemy_attack_cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.can_attack == False:
            if current_time - self.last_attack_time >= self.enemy_cooldown_time:
                self.can_attack = True

    def update(self):
        self.move(self.speed)
        self.animate()
        self.enemy_attack_cooldown()
        self.check_heatlh()