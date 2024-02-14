import pygame

from game.actors.player import Player
from game.actors.enemy import Enemy1, Enemy2, Enemy3, Enemy4
from game.waves.wave import Wave
from game.game_objects.melee.axe import generate_single_edged_axe, generate_double_edged_axe
from game.game_objects.melee.sword import generate_prime_sword, generate_wooden_sword
from game.game_objects.ranged.bow import generate_bow


def generate_waves(display, player: Player):
    # dictionary: key = Enemy class, value = tupel (num_enemies, Weapon)

    enemies_to_spawn_wave_1 = {
        Enemy1: (1, generate_wooden_sword),
        Enemy2: (1, generate_prime_sword)
    }
    wave_1 = Wave(display=display, target=player, enemies_to_spawn=enemies_to_spawn_wave_1)

    enemies_to_spawn_wave_2 = {
        Enemy1: (1, generate_wooden_sword),
        Enemy2: (1, generate_prime_sword)
    }
    wave_2 = Wave(display=display, target=player, enemies_to_spawn=enemies_to_spawn_wave_2)

    enemies_to_spawn_wave_3 = {
        Enemy1: (1, generate_bow),
        Enemy2: (1, generate_prime_sword),
        Enemy3: (1, generate_single_edged_axe)
    }
    wave_3 = Wave(display=display, target=player, enemies_to_spawn=enemies_to_spawn_wave_3)

    enemies_to_spawn_wave_4 = {
        Enemy4: (1, generate_double_edged_axe),
    }
    wave_4 = Wave(display=display, target=player, enemies_to_spawn=enemies_to_spawn_wave_4)
    return [wave_1, wave_2, wave_3, wave_4]

