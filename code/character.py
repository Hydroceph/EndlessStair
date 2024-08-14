
""" Character super class for enemies and player """

import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.blocked = False

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

    def block(self):
        self.blocked = True
        self.direction = pygame.math.Vector2(0,0)

    def unblock(self):
        self.blocked = False