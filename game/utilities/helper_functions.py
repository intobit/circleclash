from typing import Optional

import pygame


def read_image(filepath: str, size: Optional[tuple[int, int]] = None) -> pygame.Surface:
    """
    Reads, transforms and coverts images

    :param filepath: path to image
    :param size: target size (width, height)
    :return: pygame.Surface created from image
    """
    img = pygame.image.load(filepath)
    if size:
        img = pygame.transform.scale(img, size)
    return img.convert() if img.get_alpha() is None else img.convert_alpha()


def rotate_image(img: pygame.Surface, angle: float) -> pygame.Surface:
    """
    Rotates a Surface around its center by a certain angle

    Source: https://www.pygame.org/wiki/RotateCenter

    :param img: pygame Surface to rotate
    :param angle: rotation angle
    :return: rotated pygame Surface
    """
    rot_image = pygame.transform.rotate(img, angle)
    rot_rect = img.get_rect()
    rot_rect.center = rot_image.get_rect().center
    return rot_image.subsurface(rot_rect)
