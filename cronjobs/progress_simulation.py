from domain import sim_data_service, progression_service
from domain.blob_services.blob_service import update_blobs


def run_progress_simulation():
    try:
        if sim_data_service.is_unconcluded_event_today():
            print("[INFO] Skipping simulation: unconcluded event today")
            return
        if sim_data_service.is_blob_created():
            print("[INFO] Skipping simulation: blob created but not named")
            return
        update_blobs()
        sim_time = progression_service.progress_simulation()
        print(f"[INFO] Simulation progressed. Current time: {sim_time}")
    except Exception as e:
        print(f"[ERROR] Error in simulation: {e.with_traceback(None)}")
