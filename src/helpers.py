from random import randint
from typing import Callable


def roll_multiple_dice(iterations: int, lmax: int, lmin: int = 1):
    return sum([randint(lmin, lmax) for i in range(0, iterations)])


def roll_dice_as_regex(expr: str):
    return roll_multiple_dice(*[int(x) for x in expr.split('d')])


roll_dice = roll_dice_as_regex


def make_cantrip_roller(attack_handler: Callable[[], int], boss_armor_class: int = 0):
    can_hit = roll_dice_as_regex('1d20') > boss_armor_class
    return lambda: attack_handler() if can_hit else 0
