table_columns = [
    "Enemigo",
    "Personajes",
    "# Turnos",
    "# Ataques",
    "# Fallos",
    "Tasa de éxito",
    "Mejores ataques",
    "Tiempo invertido",
]


def player_info_parser(player, player_index, bonuses):
    attack_bonus = player.attack_bonus + bonuses.get("attack_bonus", 0)
    proficiency_bonus = player.proficiency_bonus + bonuses.get("proficiency_bonus", 0)
    return f"P{player_index} | {player.__class__.__name__} (AB: {attack_bonus}, PB: {proficiency_bonus})"


def table_row_parser(boss, players, final_turn, total_attacks, missed_attacks, best_actions_list, bonuses):
    expended_time = (final_turn * 15) / 60
    return [
        f'{boss.__class__.__name__}, HP: {boss.get_initial_life()}, AC: {boss.armor_class}',
        "\n".join(player_info_parser(player, index + 1, bonuses) for index, player in enumerate(players)),
        str(final_turn),
        str(total_attacks),
        str(missed_attacks),
        f"{(100 - (missed_attacks * 100) / (total_attacks + missed_attacks)):.2f}%",
        "\n".join(sorted(best_actions_list, reverse=True)),
        f"{expended_time} {'m' if expended_time < 1 else 'h'}.",
    ]
