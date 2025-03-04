
""" Game Window, Graphical elements setup and dictionary data (weapon damage dict, enemy health dict etc.) """

import pygame
from csv import reader
from os import walk

# Screen and map
WIDTH = 1280	
HEIGHT = 720
FPS = 60
TILESET_TILESIZE = 16
TILESIZE = 64

# GUI
FOG_COLOUR = (20,20,20)

BAR_HEIGHT = 10
HP_BAR_WIDTH = 100
EXP_BAR_WIDTH = 100
FONT = './graphics/underworld/Font/Pixeltype.ttf'
FONT_SIZE = 32

HEALTH_COLOUR = 'red'
EXP_FONT_COLOUR = 'yellow'
BAR_BACKGROUND_COLOUR = '#444444'
BAR_BORDER_COLOUR = '#333333'

# functions to import tilesets/image collections for grahpical elements
def read_map_csv(path):
    room_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            room_map.append(list(row))
        return room_map

def cut_tileset(path, TILESET_TILESIZE = 16):
    surface = pygame.image.load(path)#.convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILESET_TILESIZE)
    tile_num_y = int(surface.get_size()[1] / TILESET_TILESIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESET_TILESIZE
            y = row * TILESET_TILESIZE
            new_surf = pygame.Surface((TILESET_TILESIZE, TILESET_TILESIZE),flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, TILESET_TILESIZE, TILESET_TILESIZE))
            new_surf = pygame.transform.scale_by(new_surf, 4)
            cut_tiles.append(new_surf)
    
    return cut_tiles

def png_collection(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list




# map graphical data

dung_room_0_layout = {
    'floor': read_map_csv('./map/dungeon/room_0/dung_room_0_floor.csv'),
    'pillars': read_map_csv('./map/dungeon/room_0/dung_room_0_pillars.csv'),
    'invis_walls': read_map_csv('./map/dungeon/room_0/dung_room_0_invis_walls.csv'),
    'back_props_des': read_map_csv('./map/dungeon/room_0/dung_room_0_back_props_des.csv'),
    'back_props_1': read_map_csv('./map/dungeon/room_0/dung_room_0_back_props_1.csv'),
    'back_props_2': read_map_csv('./map/dungeon/room_0/dung_room_0_back_props_2.csv'),
    'interact': read_map_csv('./map/dungeon/room_0/dung_room_0_interact.csv'),
    'constraints': read_map_csv('./map/dungeon/room_0/dung_room_0_constraints.csv'),
    'exit_1': read_map_csv('./map/dungeon/room_0/dung_room_0_exit_1.csv'),
    'exit_2': read_map_csv('./map/dungeon/room_0/dung_room_0_exit_2.csv'),
    'player': read_map_csv('./map/dungeon/room_0/dung_room_0_player.csv'),
    'mob': read_map_csv('./map/dungeon/room_0/dung_room_0_mob.csv')
}

dung_room_0_graphics = {
    'dung_tiles': cut_tileset('./graphics/underworld/Environment/Dungeon Prison/Assets/Tiles.png'),
    'dung_props': cut_tileset('./graphics/underworld/Environment/Dungeon Prison/Assets/Props.png'),
    'spawns': cut_tileset('./map/universal/graphics/red-stop.png')
}

dung_room_1_layout = {
    'floor': read_map_csv('./map/dungeon/room_1/dung_room_1_floor.csv'),
    'pillars': read_map_csv('./map/dungeon/room_1/dung_room_1_pillars.csv'),
    'invis_walls': read_map_csv('./map/dungeon/room_1/dung_room_1_invis_walls.csv'),
    'back_props_des': read_map_csv('./map/dungeon/room_1/dung_room_1_back_props_des.csv'),
    'back_props_1': read_map_csv('./map/dungeon/room_1/dung_room_1_back_props_1.csv'),
    'back_props_2': read_map_csv('./map/dungeon/room_1/dung_room_1_back_props_2.csv'),
    'interact': read_map_csv('./map/dungeon/room_1/dung_room_1_interact.csv'),
    'constraints': read_map_csv('./map/dungeon/room_1/dung_room_1_constraints.csv'),
    'exit_1': read_map_csv('./map/dungeon/room_1/dung_room_1_exit_1.csv'),
    'exit_2': read_map_csv('./map/dungeon/room_1/dung_room_1_exit_2.csv'),
    'player': read_map_csv('./map/dungeon/room_1/dung_room_1_player.csv'),
    'mob': read_map_csv('./map/dungeon/room_1/dung_room_1_mob.csv')
}

dung_room_2_layout = {
    'floor': read_map_csv('./map/dungeon/room_2/dung_room_2_floor.csv'),
    'pillars': read_map_csv('./map/dungeon/room_2/dung_room_2_pillars.csv'),
    'invis_walls': read_map_csv('./map/dungeon/room_2/dung_room_2_invis_walls.csv'),
    'back_props_des': read_map_csv('./map/dungeon/room_2/dung_room_2_back_props_des.csv'),
    'back_props_1': read_map_csv('./map/dungeon/room_2/dung_room_2_back_props_1.csv'),
    'back_props_2': read_map_csv('./map/dungeon/room_2/dung_room_2_back_props_2.csv'),
    'interact': read_map_csv('./map/dungeon/room_2/dung_room_2_interact.csv'),
    'constraints': read_map_csv('./map/dungeon/room_2/dung_room_2_constraints.csv'),
    'exit_1': read_map_csv('./map/dungeon/room_2/dung_room_2_exit_1.csv'),
    'exit_2': read_map_csv('./map/dungeon/room_2/dung_room_2_exit_2.csv'),
    'player': read_map_csv('./map/dungeon/room_2/dung_room_2_player.csv'),
    'mob': read_map_csv('./map/dungeon/room_2/dung_room_2_mob.csv')
}

dung_room_3_layout = {
    'floor': read_map_csv('./map/dungeon/room_3/dung_room_3_floor.csv'),
    'pillars': read_map_csv('./map/dungeon/room_3/dung_room_3_pillars.csv'),
    'invis_walls': read_map_csv('./map/dungeon/room_3/dung_room_3_invis_walls.csv'),
    'back_props_des': read_map_csv('./map/dungeon/room_3/dung_room_3_back_props_des.csv'),
    'back_props_1': read_map_csv('./map/dungeon/room_3/dung_room_3_back_props_1.csv'),
    'back_props_2': read_map_csv('./map/dungeon/room_3/dung_room_3_back_props_2.csv'),
    'interact': read_map_csv('./map/dungeon/room_3/dung_room_3_interact.csv'),
    'constraints': read_map_csv('./map/dungeon/room_3/dung_room_3_constraints.csv'),
    'exit_1': read_map_csv('./map/dungeon/room_3/dung_room_3_exit_1.csv'),
    'exit_2': read_map_csv('./map/dungeon/room_3/dung_room_3_exit_2.csv'),
    'player': read_map_csv('./map/dungeon/room_3/dung_room_3_player.csv'),
    'mob': read_map_csv('./map/dungeon/room_3/dung_room_3_mob.csv')
}

dung_room_spawn_layout = {
    'floor': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_floor.csv'),
    'pillars': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_pillars.csv'),
    'invis_walls': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_invis_walls.csv'),
    'back_props_des': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_back_props_des.csv'),
    'back_props_1': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_back_props_1.csv'),
    'back_props_2': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_back_props_2.csv'),
    'interact': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_interact.csv'),
    'constraints': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_constraints.csv'),
    'exit_1': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_exit_1.csv'),
    'exit_2': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_exit_2.csv'),
    'player': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_player.csv'),
    'mob': read_map_csv('./map/dungeon/spawn_room/dung_room_spawn_mob.csv')
}


# weapon data

bone_weapon_data = {
    'book': {'cooldown': 400, 'damage': 30, 'png': './graphics/underworld/Weapons/Bone/collection/Bone-Book.png'},
    'knife': {'cooldown': 100, 'damage': 10, 'png': './graphics/underworld/Weapons/Bone/collection/Bone-Knife.png'},
    'spear': {'cooldown': 300, 'damage': 25, 'png': './graphics/underworld/Weapons/Bone/collection/Bone-Spear.png'},
    'staff': {'cooldown': 400, 'damage': 30, 'png': './graphics/underworld/Weapons/Bone/collection/Bone-Staff.png'},
    'sword': {'cooldown': 400, 'damage': 30, 'png': './graphics/underworld/Weapons/Bone/collection/Bone-Sword.png'},
    'wand': {'cooldown': 100, 'damage': 10, 'png': './graphics/underworld/Weapons/Bone/collection/Bone-Wand.png'}
}

attack_animation_data = {
    'nova_ball': './graphics/underworld/Particles/nova',
    'stab': './graphics/underworld/Particles/slash'
}



# enemy data
enemy_data = {
	'orc': {'health': 100,'exp': 50,'damage': 20,'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360, 'graphics': './graphics/underworld/Enemy/Orc Crew/Orc/Run/collection', 'hit_graphics': './graphics/underworld/Enemy/Orc Crew/Orc/Death/collection'},
    'skel_mage': {'health': 10,'exp': 50,'damage': 10,'attack_type': 'fireball', 'speed': 3, 'resistance': 1, 'attack_radius': 80, 'notice_radius': 360, 'graphics': './graphics/underworld/Enemy/Skeleton Crew/Skeleton - Mage/Run/collection', 'hit_graphics': './graphics/underworld/Enemy/Skeleton Crew/Skeleton - Mage/Death/collection'},
    'rogue': {'health': 300,'exp': 50,'damage': 30,'attack_type': 'slash', 'speed': 3, 'resistance': 1, 'attack_radius': 80, 'notice_radius': 360, 'graphics': './graphics/underworld/Heroes/Rogue/Run/collection', 'hit_graphics': './graphics/underworld/Heroes/Rogue/Death/collection'}
}



# player data

player_stats = {'health': 100, 'attack': 10, 'speed': 6}