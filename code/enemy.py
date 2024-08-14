
""" Enemy sprites and enemy attacks """

import pygame
from character import Character
from game_data import enemy_data, png_collection
import random


class EnemyCharacter(Character):
    def __init__(self, groups, enemy_type, pos):
        super().__init__(groups)

        # stats
        self.enemy_type = enemy_type
        self.enemy_info = enemy_data[self.enemy_type]
        self.speed =  self.enemy_info['speed']
        self.animation_direction = 'right'
        self.health =  self.enemy_info['health']
        self.exp =  self.enemy_info['exp']
        self.attack_type =  self.enemy_info['attack_type']
        self.attack_damage =  self.enemy_info['damage']
        self.resistance =  self.enemy_info['resistance']
        self.attack_radius =  self.enemy_info['attack_radius']
        self.notice_radius =  self.enemy_info['notice_radius']

        self.image_list = png_collection(enemy_data[enemy_type]['graphics'])
        self.image = self.image_list[self.frame_index]
        self.image = pygame.transform.scale_by(self.image, 3)

        self.rect = self.image.get_rect(topleft = pos)
        self.rect_collision = self.rect.inflate(-8, -16)

# orc

class Enemy(EnemyCharacter):
    def __init__(self, groups, obstacle_sprites, enemy_type, pos, damage_player, add_exp):
        super().__init__(groups, enemy_type, pos)


        self.obstacle_sprites = obstacle_sprites
        self.status = 'slow_move'

        # attack player
        self.can_attack = True
        self.last_attack_time = None
        self.enemy_cooldown_time = 400
        self.damage_player = damage_player

        # enemy atacked
        self.can_be_attacked = True
        self.last_hit_time = None
        self.invincible_duration = 300
        self.enemy_hit_image = png_collection(enemy_data[enemy_type]['hit_graphics'])[0]
        self.add_exp = add_exp
    
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
            self.animation_speed = 0.15
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.speed = 3
            self.animation_speed = 0.15
            self.status = 'move'
        else:
            self.speed = 1
            self.animation_speed = 0.05
            self.status = 'slow_move'

        if direction.x >= 0:
            self.animation_direction = 'right'
        else:
            self.animation_direction = 'left'
        

        return direction

    def get_damage(self, player, attack_type):
        if self.can_be_attacked:
            if attack_type == 'magic':
                self.health -= player.get_weapon_damage()[0]
            if attack_type == 'melee':
                self.health -= player.get_weapon_damage()[1]
            self.last_hit_time = pygame.time.get_ticks()
            self.can_be_attacked = False

    def check_heatlh(self):
        if self.health <= 0:
            self.add_exp(self.exp)
            self.kill()

    def knockback(self):
        if self.can_be_attacked == False:
            self.direction *= self.resistance * -1

    def enemy_update(self, player):
        self.direction_check(player)
        self.chase(player)

    def chase(self,player):
        if self.status == 'attack' and self.can_attack == True:
            self.can_attack = False
            self.damage_player(self.attack_damage)
            self.last_attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.direction_check(player)
        else: # slow move, (lower self.speed)
            self.direction = self.direction_check(player)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.image_list) - 1e-6:
            self.frame_index = 0
        print(self.frame_index)
        self.image = self.image_list[int(self.frame_index)]
        self.image = pygame.transform.scale_by(self.image, 3)

        # hit animation when damaged
        if self.can_be_attacked == False:
            self.attacked_image = self.enemy_hit_image
            self.attacked_image = pygame.transform.scale_by(self.attacked_image, 3)
            self.image = self.attacked_image

        if self.animation_direction == 'left':
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = self.rect_collision.center)

    def enemy_attack_cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.can_attack == False:
            if current_time - self.last_attack_time >= self.enemy_cooldown_time:
                self.can_attack = True
            
        if self.can_be_attacked == False:
            if current_time - self.last_hit_time >= self.invincible_duration:
                self.can_be_attacked = True

    def update(self):
        self.knockback()
        self.move(self.speed)
        self.animate()
        self.enemy_attack_cooldown()
        self.check_heatlh()


# skel mage

class PatrolEnemy(Enemy):
    def __init__(self, groups, obstacle_sprites, enemy_type, pos, damage_player, constraints_sprites, patrol_direction, create_enemy_projectile, add_exp):
        super().__init__(groups, obstacle_sprites, enemy_type, pos, damage_player, add_exp)

        self.patrol_direction = patrol_direction
        self.constraints_sprites = constraints_sprites
        self.create_enemy_projectile = create_enemy_projectile # remember the enemy_source parameter
        self.speed = random.randint(3,8)
        if self.patrol_direction == 'vertical':
            self.direction = pygame.math.Vector2(0,1)
        elif self.patrol_direction == 'horizontal':
            self.direction = pygame.math.Vector2(1,0)

        self.duration = random.randint(2000,4000)
        self.last_attack_time = pygame.time.get_ticks()

    def direction_check(self, player):
        player_position = pygame.math.Vector2(player.rect.center)
        enemy_position = pygame.math.Vector2(self.rect.center)
        distance = (player_position - enemy_position).magnitude()
        if distance > 0:
            direction = (player_position - enemy_position).normalize()
        else:
            direction = pygame.math.Vector2()

        if direction.x >= 0:
            self.animation_direction = 'right'
        else:
            self.animation_direction = 'left'
        

        return direction
    
    def shoot_player(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.duration:
            self.create_enemy_projectile(self.rect_collision.center)
            self.last_attack_time = current_time

    def enemy_update(self, player):
        self.direction_check(player)

    def constraints_reverse(self):
        for constraint in self.constraints_sprites:
            if constraint.rect_collision.colliderect(self.rect_collision):
                self.speed *= -1

    def update(self):
        super().update()
        self.constraints_reverse()
        self.shoot_player()





# patrol enemy attack

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, player, groups, obstacle_sprites, destructable_sprites, enemy_source, damage_player, spawn_distance = 75):
        super().__init__(groups)
        direction = pygame.math.Vector2(player.rect_collision.center) - pygame.math.Vector2(enemy_source)
        self.direction = direction.normalize()
        self.speed = 5
        self.enemy_source = enemy_source
        self.player = player
        self.damage_player = damage_player

        self.image_list = png_collection('./graphics/underworld/Particles/flame/frames')
        self.image = self.image_list[0]


        self.rect = self.image.get_rect(center = self.enemy_source + self.direction * spawn_distance)
        self.rect_collision = self.rect.inflate(-4, -4)

        self.frame_index = 0
        self.animation_speed = 0.3

        self.obstacle_sprites = obstacle_sprites
        self.destructable_sprites = destructable_sprites

    def animate(self):
        self.frame_index += self.animation_speed
        animation = self.image_list
        if self.frame_index > len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

        self.rect = self.image.get_rect(center = self.rect_collision.center)

    def update(self):

        self.rect_collision.center += self.direction * self.speed
        self.rect.center = self.rect_collision.center

        self.animate()

        for sprite in self.obstacle_sprites:
            if sprite.rect_collision.colliderect(self.rect_collision):
                self.kill()

        for sprite in self.destructable_sprites:
            if sprite.rect_collision.colliderect(self.rect_collision):
                sprite.kill()
                self.kill()
        
        if self.rect.colliderect(self.player.rect):
            self.damage_player(20)