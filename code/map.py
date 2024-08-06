
""" Game Window and Map setup """

import pygame
from csv import reader
from os import walk


WIDTH = 1280	
HEIGHT = 720
FPS = 60
tileset_tilesize = 16
TILESIZE = 64


def read_map_csv(path):
    room_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            room_map.append(list(row))
        return room_map

def cut_tileset(path):
    surface = pygame.image.load(path)#.convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tileset_tilesize)
    tile_num_y = int(surface.get_size()[1] / tileset_tilesize)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tileset_tilesize
            y = row * tileset_tilesize
            new_surf = pygame.Surface((tileset_tilesize, tileset_tilesize),flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tileset_tilesize, tileset_tilesize))
            new_surf = pygame.transform.scale_by(new_surf, 4)
            cut_tiles.append(new_surf)
    
    return cut_tiles


dung_room_0_layout = {
    'floor': read_map_csv('./map/dungeon/room_0/dung_room_0_floor.csv'),
    'pillars': read_map_csv('./map/dungeon/room_0/dung_room_0_pillars.csv'),
    'invis_walls': read_map_csv('./map/dungeon/room_0/dung_room_0_invis_walls.csv'),
    'back_props_des': read_map_csv('./map/dungeon/room_0/dung_room_0_back_props_des.csv'),
    'back_props_1': read_map_csv('./map/dungeon/room_0/dung_room_0_back_props_1.csv'),
    'back_props_2': read_map_csv('./map/dungeon/room_0/dung_room_0_back_props_2.csv'),
    'interact': read_map_csv('./map/dungeon/room_0/dung_room_0_interact.csv'),
    'player': read_map_csv('./map/dungeon/room_0/dung_room_0_player.csv'),
    'mob': read_map_csv('./map/dungeon/room_0/dung_room_0_mob.csv'),
    'constraints': read_map_csv('./map/dungeon/room_0/dung_room_0_constraints.csv'),
    'exit_1': read_map_csv('./map/dungeon/room_0/dung_room_0_exit_1.csv'),
    'exit_2': read_map_csv('./map/dungeon/room_0/dung_room_0_exit_2.csv')
}

dung_room_0_graphics = {
    'dung_tiles': cut_tileset('./graphics/underworld/Environment/Dungeon Prison/Assets/Tiles.png'),
    'dung_props': cut_tileset('./graphics/underworld/Environment/Dungeon Prison/Assets/Props.png'),
    'spawns': cut_tileset('./map/universal/graphics/red-stop.png')
}