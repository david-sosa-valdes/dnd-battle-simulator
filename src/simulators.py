from typing import Optional, Tuple

from .bosses import BaseBoss


class BaseSimulation:

    def __init__(self, boss: BaseBoss, players: list, bonuses: Optional[dict] = None):
        self.boss = boss
        self.players = players.copy()
        self.best_actions = {}
        self.missed_attacks = 0
        self.total_attacks = 0
        self.__set_player_bonuses(bonuses)

    def __set_player_bonuses(self, bonuses: Optional[dict] = None):
        for player in self.players:
            for attr_name, attr_value in bonuses.items():
                current_value = getattr(player, attr_name, None)
                if current_value:
                    setattr(player, attr_name, current_value + attr_value)

    def __log_action(self, action_name: str, attack_name: str, attack_dmg: int, player_index: int):
        last_dmg = self.best_actions.get(action_name, [None, 0])

        if attack_dmg > last_dmg[1]:
            self.best_actions[action_name] = (attack_name, attack_dmg, f"P{player_index}")

    def summary(self) -> Tuple[dict, int, int]:
        return self.best_actions, self.missed_attacks, self.total_attacks

    def run_player_actions(self, player, player_index):
        for action in player.action_sequence:
            action_name, attack_name, attack_roll = player.choice_action(action)
            attack_dmg = attack_roll(self.boss)

            if attack_dmg > 0:
                self.boss.life -= attack_dmg
                self.total_attacks += 1
            else:
                self.missed_attacks += 1

            self.__log_action(action_name, attack_name, attack_dmg, player_index)

    def run(self):
        current_turn = 1

        while self.boss.life > 0:
            for index, player in enumerate(self.players):
                self.run_player_actions(player, index + 1)
            current_turn += 1

        return current_turn, self.summary()
