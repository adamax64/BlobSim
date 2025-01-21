from rich.live import Live
from tkinter import Tk, ttk, Label

from domain.blob_service import update_blobs
from domain.sim_data_service import progress_simulation


def show_simulation_progress(live: Live):
    root = Tk()
    root.title("Simulation Progress")

    live.update("Updating blobs...", refresh=True)

    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=5)

    percent_label = Label(root, text="0%")
    percent_label.pack(pady=5)

    def update_progress():
        for percent in update_blobs():
            progress['value'] = percent
            percent_label.config(text=f"{percent}%")
            root.update_idletasks()

        live.update("Updating simulation data...", refresh=True)

        progress_simulation()
        root.destroy()

    root.after(100, update_progress)
    root.mainloop()
