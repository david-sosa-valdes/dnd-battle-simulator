from typing import Callable
import typer

from src.bosses import BaseBoss
from src.players import Barbaric, Wizard
from src.simulators import BaseSimulation
from src.parsers import table_row_parser, table_columns
from src.printers import print_table

app = typer.Typer()

PlayersCallback = Callable[[], list]


def make_gameboards(players_callback: PlayersCallback):
    rows = []

    for i in range(0, 10):
        bonuses = {
            'proficiency_bonus': 10 + i,
            'attack_bonus': 80 + i
        }
        boss = BaseBoss(armor_class=24 - i, life=2000 - (i * 200))
        current_players = players_callback()
        simulation = BaseSimulation(boss, current_players, bonuses=bonuses)
        final_turn, summary = simulation.run()
        best_actions, missed_attacks, total_attacks = summary
        best_actions_list = []

        for action_name, attack in best_actions.items():
            best_actions_list.append(f"- {attack[2]} | {action_name}: {attack[0]} ({attack[1]})")

        rows.append(table_row_parser(
            boss=boss,
            players=current_players,
            final_turn=final_turn,
            total_attacks=total_attacks,
            missed_attacks=missed_attacks,
            best_actions_list=best_actions_list,
            bonuses=bonuses
        ))

    return rows


def players():
    return [
        Barbaric(
            action_sequence=[
                ('attack', 'random'),
                ('attack', 'random'),
                ('bonus_action', 'random')
            ],
            proficiency_bonus=7,
            attack_bonus=6
        ),
        Barbaric(
            action_sequence=[
                ('attack', 'random'),
                ('attack', 'random'),
                ('bonus_action', 'random')
            ],
            proficiency_bonus=9,
            attack_bonus=7
        ),
        Wizard(
            action_sequence=[
                ('cast_spell', 'random'),
                ('cast_spell', 'random'),
            ],
            proficiency_bonus=7,
            attack_bonus=8
        ),
        Wizard(
            action_sequence=[
                ('cast_spell', 'random'),
                ('cast_spell', 'random'),
            ],
            proficiency_bonus=8,
            attack_bonus=9
        ),
        Wizard(
            action_sequence=[
                ('cast_spell', 'random'),
                ('cast_spell', 'random'),
            ],
            proficiency_bonus=8,
            attack_bonus=9
        )
    ]


def main():
    """
    Running multiple gameboards
    """
    print_table(rows=make_gameboards(players), columns=table_columns)


if __name__ == "__main__":
    typer.run(main)
