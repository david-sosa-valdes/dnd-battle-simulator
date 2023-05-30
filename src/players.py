import random
from typing import Callable, Union, Tuple

from .helpers import roll_dice


def select_attack_roll(action_choice: str, attack_choices: dict):
    if action_choice == 'random':
        action_key = random.choice(list(attack_choices.keys()))
    else:
        action_key = action_choice
    return action_key, attack_choices[action_key]


def select_spell_roll(action_choice: str, attack_choices: dict):
    if action_choice == 'random':
        action_key = random.choice(list(attack_choices.keys()))
    else:
        action_key = action_choice
    return action_key, attack_choices[action_key]


Action = Tuple[str, str]


class CharacterClass:
    weapons = {}
    actions = []
    bonus_actions = {}
    spells = {}
    spell_slots = {}
    cantrips = {}

    def __init__(self, action_sequence: list, proficiency_bonus: int = 2, attack_bonus: int = 2,
                 out_of_spell_slots_action: Action = None):
        self.proficiency_bonus = proficiency_bonus
        self.attack_bonus = attack_bonus
        self.action_sequence = action_sequence

        if not out_of_spell_slots_action:
            self.__out_of_spell_slots_action = ['attack', 'random']
        else:
            self.__out_of_spell_slots_action = out_of_spell_slots_action

    def __make_action_handler(self, attack_roll: Union[Callable[[int], int], Callable[[], int]], action_type: str):
        def wrapper(boss):
            can_hit = (roll_dice('1d20') + self.proficiency_bonus) > boss.armor_class
            args = [self.attack_bonus] if action_type != 'bonus_action' else []
            return attack_roll(*args) if can_hit else 0

        return wrapper

    def choice_action(self, action: Action):
        attack_name, attack_roll = (None, None)
        action_type, action_choice = action

        if action_type not in self.actions:
            raise Exception(f'Cannot choice action: {action_type}')

        if action_type == 'attack':
            attack_name, attack_roll = select_attack_roll(action_choice, self.weapons)

        if action_type == 'bonus_action':
            attack_name, attack_roll = select_attack_roll(action_choice, self.bonus_actions)

        if action_type == 'cast_spell':
            attack_name, selected_spell = select_attack_roll(action_choice, self.spells)
            spell_level = selected_spell['level']

            if self.spell_slots[spell_level] <= 0:
                return self.choice_action(self.__out_of_spell_slots_action)

            attack_roll = selected_spell['attack_roll']
            self.spell_slots[spell_level] -= 1

        if not (attack_name and attack_roll):
            raise Exception('Cannot choice action type')

        return action_type, attack_name, self.__make_action_handler(attack_roll, action_type)


class Barbaric(CharacterClass):
    actions = [
        'attack',
        'bonus_action',
    ]
    weapons = {
        'great-battle-axe': lambda attack_bonus: roll_dice('1d12') + attack_bonus,
        'short_sword': lambda attack_bonus: roll_dice('1d8') + attack_bonus
    }
    bonus_actions = {
        'additional-attack': lambda: roll_dice('1d12')
    }


class Wizard(CharacterClass):
    actions = [
        'attack',
        'cast_spell',
        'cantrip',
    ]
    spells = {
        'fireball': {
            'level': 3,
            'attack_roll': lambda attack_bonus: roll_dice("6d8") + attack_bonus,
        },
        'lightning-bolt': {
            'level': 3,
            'attack_roll': lambda attack_bonus: roll_dice("3d6") + attack_bonus,
        },
    }
    weapons = {
        'dagger': lambda attack_bonus: roll_dice("1d4") + attack_bonus,
        'short_sword': lambda attack_bonus: roll_dice("1d6") + attack_bonus
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spell_slots = {
            1: 4 + 40,
            2: 3 + 40,
            3: 2 + 100,
        }
