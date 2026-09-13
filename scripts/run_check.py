import src.config  # noqa: F401

from src.orchestrate import run_check, prune_old_snapshots

if __name__ == "__main__":
    run_check()
    prune_old_snapshots()