
""" A* pathfinding, and enemy with pathfinding """

import pygame
import numpy as np

from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.finder.a_star import AStarFinder

from enemy import EnemyCharacter

# Create a 3D numpy array with 0s as obstacles and 1s as walkable paths. 
# z, y, x
matrix = np.zeros((2, 30, 30), dtype=np.int8)

# Make ONLY the bottom layer = the Tiled floor CSV, with -1's converted to 0's and anything else converted to 1
# only the bottom layer will therefore be considered, functionally making it 2d pathfinding
bottom_layer = np.array([
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=np.int8)

# Place the 2D grid into the bottom layer of the 3D grid
matrix[0, :, :] = bottom_layer




class Pathfinder:
    def __init__(self, pathfinding_boss, player):
        
        self.grid = Grid(matrix = matrix)

        self.path = []

        self.pathfinding_boss = pathfinding_boss
        self.player = player

    def create_path(self):
        # start
        start_x = self.pathfinding_boss.rect.centerx // 64
        start_y = self.pathfinding_boss.rect.centery // 64
        start = self.grid.node(0, start_y, start_x)

        # end
        end_x = self.player.rect.centerx // 64
        end_y = self.player.rect.centery // 64
        end = self.grid.node(0, end_y, end_x)

        # path
        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)

        self.path = [p.identifier for p in self.path]

        self.grid.cleanup()
        print("path:", self.path)
        return(self.path)

    def draw_path(self, displaysurface, offset):
        if self.path:
            self.offset = offset
            points = []
            for point in self.path:
                point_x = (point[2] * 64) - self.offset.x + 32
                point_y = (point[1] * 64) - self.offset.y + 32
                points.append((point_x, point_y))
            pygame.draw.lines(displaysurface, 'yellow', False, points, 5)

class PathfindingBoss(EnemyCharacter):
    def __init__(self, groups, enemy_type, pos):
        super().__init__(groups, enemy_type, pos)

        self.current_position = self.rect.center

        self.path = []
        self.collision_rects = []
        self.direction = pygame.math.Vector2(0,0)

        # resets the image and rect size so it works with the tilesize
        self.image = self.image_list[self.frame_index]
        self.image = pygame.transform.scale_by(self.image, 2)

        self.rect = self.image.get_rect(topleft = pos)
        self.rect_collision = self.rect.inflate(-8, -16)

        self.node_collision_sprites = pygame.sprite.Group()

    def get_path(self, path, offset):
        self.path = path
        self.create_node_collisions(offset)
        self.get_direction()

    def create_node_collisions(self, offset):
        if self.path:
            self.offset = offset
            self.collision_rects = []
            for point in self.path:
                point_x = (point[2] * 64) + 32
                point_y = (point[1] * 64) + 32
                rect = pygame.Rect((point_x - 4, point_y - 4),(8, 8))
                self.collision_rects.append(rect)
                print(self.collision_rects[0])

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.current_position)
            print(start)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            print(end)
            self.direction = (end - start).normalize()
            print (self.direction)
        else: 
            self.direction = pygame.math.Vector2(0,0)

    def move(self):
        self.current_position += self.direction * self.speed
        self.rect.center = self.current_position
        self.rect_collision.center = self.current_position

    def check_node_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.current_position):
                    print('deleting node')
                    del self.collision_rects[0]
                    self.get_direction()

    def update(self):
        self.check_node_collisions()
        self.move()

        