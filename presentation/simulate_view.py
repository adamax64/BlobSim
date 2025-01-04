from rich.live import Live
from rich.progress import Progress

from domain.blob_service import update_blobs
from domain.sim_data_service import progress_simulation


def show_simulation_progress(live: Live):
    progress = Progress()

    task = progress.add_task("Updating blobs...", total=100)

    for percent in update_blobs():
        progress.update(task, progress=percent)
        live.update(progress, refresh=True)

    progress_simulation()
