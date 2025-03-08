import time
from typing import List
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

from domain.blob_service import get_all_blobs
from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.sim_data_service import get_sim_time
from domain.utils.sim_time_utils import get_season
from presentation.constants import KEY_DOWN, KEY_ENTER, KEY_ESCAPE, KEY_UP
from presentation.utils import capture_keypress


def show_blobs_view(live: Live):
    blobs: List[BlobStatsDto] = get_all_blobs()
    season = get_season(get_sim_time())
    current_row = 0

    def render():
        table = Table(
            title="Select a blob to view options or press Escape to return",
            min_width=50,
        )

        table.add_column("Name")
        table.add_column("Born")
        table.add_column("Debut", justify="center")
        table.add_column("Contract", justify="center")
        table.add_column("Podiums", justify="center")
        table.add_column("Wins", justify="center")
        table.add_column("Championships", justify="center")
        table.add_column("Grandmasters", justify="center")
        table.add_column("League")

        for i, blob in enumerate(blobs):
            table.add_row(
                (
                    f"[cyan]{str(blob.name)}[/cyan]"
                    if i == current_row
                    else str(blob.name)
                ),
                str(blob.born),
                "-" if blob.debut is None else str(blob.debut),
                _format_contract(blob.contract, season),
                str(blob.podiums),
                str(blob.wins),
                str(blob.championships),
                str(blob.grandmasters),
                blob.league_name,
            )
        return Panel(table, title="Blobs", title_align="left")

    live.update(render(), refresh=True)

    while True:
        key = capture_keypress()

        if key == KEY_UP and current_row > 0:
            current_row -= 1
            live.update(render(), refresh=True)
            time.sleep(0.1)
        elif key == KEY_DOWN and current_row < len(blobs) - 1:
            current_row += 1
            live.update(render(), refresh=True)
            time.sleep(0.1)
        elif key == KEY_ENTER:
            # TODO show_blob_details(blobs[current_row])
            pass
        elif key == KEY_ESCAPE:
            time.sleep(0.1)
            break


def _format_contract(contract, season):
    if contract == season:
        return f"[orange4]{str(contract)}[/orange4]"
    elif contract is None:
        return "-"
    else:
        return str(contract)
