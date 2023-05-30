from rich.console import Console
from rich.table import Table
from rich import box


def print_table(rows, columns):
    table = Table(box=box.SQUARE, show_lines=True)

    for column in columns:
        table.add_column(column)

    for row in rows:
        table.add_row(*row)

    console = Console()
    console.print(table)
