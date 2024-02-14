from abc import ABC
import math
from os import path

import pygame

from game.utilities.helper_functions import read_image, rotate_image
from game.utilities.gamestate import GameState


class Projectile(pygame.sprite.Sprite, ABC):
    image_path: str or list[str] = path.join("resources", "weapons", "arrow.png")
    current_image_idx = None
    size: tuple[int, int] = (90, 90)
    angle_offset = 0
    attack_range = 10_000.0
    damage_points = 20
    speed = 10

    def __init__(self, start_pos, angle, display):
        super().__init__()
        if isinstance(self.image_path, str):
            self.image = read_image(self.image_path, self.size)
            self.images = None
        elif isinstance(self.image_path, list):
            self.images = [read_image(file_path, self.size) for file_path in self.image_path]
            self.current_image_idx = 0
        self.points = 10
        self.start_pos = start_pos
        self.angle = angle
        self.current_pos = start_pos.copy()
        self.rect = None
        self.rotated = False
        self.aim()
        self.display = display

    def draw(self):
        self.display.blit(self.image, (self.current_pos[0] - int(self.image.get_width() / 2),
                                       self.current_pos[1] - int(self.image.get_height() / 2)))

    def aim(self):
        angle = (360 - self.angle - self.angle_offset) % 360
        if self.images:
            img = self.images[self.current_image_idx].copy()
            self.image = rotate_image(img, angle)
        elif self.rotated is False:
            img = self.image.copy()
            self.image = rotate_image(img, angle)
            self.rotated = True

        self.rect = self.image.get_rect(center=(self.current_pos[0], self.current_pos[1]))

    def move(self):
        self.current_pos[0] += self.speed * math.cos(math.radians(self.angle))
        self.current_pos[1] += self.speed * math.sin(math.radians(self.angle))
        self.rect = self.image.get_rect(center=(self.current_pos[0], self.current_pos[1]))

    def update(self, game_state: GameState):
        # Punkt P: current pos
        # Punkt O: start pos
        # OP = P - O
        # |OP| -> length

        travelled_distance = (self.current_pos - self.start_pos).length()
        if self.images:
            num_images = len(self.images)
            dist_per_img = travelled_distance / num_images
            if travelled_distance > self.current_image_idx * dist_per_img and self.current_image_idx < num_images -1:
                self.current_image_idx += 1

        if travelled_distance >= self.attack_range:
            self.kill()
        if game_state == GameState.RUNNING:
            self.aim()
            self.move()
        self.draw()


class MeleeProjectile(Projectile):
    attack_range = 30.0
    angle_offset = -135
    speed = 3

    def is_enemy_hit(self, enemy):
        distance_to_enemy = math.hypot(enemy.x - self.start_pos[0], enemy.y - self.start_pos[1])
        return distance_to_enemy <= self.attack_range


class PrimeSwordProjectile(MeleeProjectile):
    image_path: str = [path.join("resources", "weapons", "prime_sword", "PS_2_19.png"),
                       path.join("resources", "weapons", "prime_sword", "PS_2_20.png"),
                       path.join("resources", "weapons", "prime_sword", "PS_2_21.png"),
                       path.join("resources", "weapons", "prime_sword", "PS_2_22.png")]
    attack_range = 60.0
    damage_points = 40


class WoodenSwordProjectile(MeleeProjectile):
    image_path: str = [path.join("resources", "weapons", "wooden_sword", "Alternative_3_25.png"),
                       path.join("resources", "weapons", "wooden_sword", "Alternative_3_26.png"),
                       path.join("resources", "weapons", "wooden_sword", "Alternative_3_27.png"),
                       path.join("resources", "weapons", "wooden_sword", "Alternative_3_28.png"),
                       path.join("resources", "weapons", "wooden_sword", "Alternative_3_29.png"),
                       path.join("resources", "weapons", "wooden_sword", "Alternative_3_30.png")]


class AxeProjectile(MeleeProjectile):
    image_path: str = path.join("resources", "weapons", "DoubAxe_1_03.png")
    angle_offset = 0


class DoubleAxeProjectile(MeleeProjectile):
    image_path: str = path.join("resources", "weapons", "DoubAxe_1_03.png")
    angle_offset = 0


class DoubleAxeProjectileEndboss(MeleeProjectile):
    image_path: str = path.join("resources", "weapons", "DoubAxe_1_03.png")
    attack_range = 200


class RangedProjectile(Projectile):
    size: tuple[int, int] = (50, 50)
    angle_offset = 90

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WandProjectile(RangedProjectile):
    image_path: str = [path.join("resources", "weapons", "wand", "Pure_06.png"),
                       path.join("resources", "weapons", "wand", "Pure_07.png"),
                       path.join("resources", "weapons", "wand", "Pure_08.png"),
                       path.join("resources", "weapons", "wand", "Pure_09.png"),
                       path.join("resources", "weapons", "wand", "Pure_10.png"),]
    angle_offset = 0
