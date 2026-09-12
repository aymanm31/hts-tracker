from src.db.connection import SessionLocal
from src.db.models import Snapshot
from src.diffing.compare import compare_snapshots
from src.diffing.save_changes import save_changes
from src.summarize.summarize import build_report

session = SessionLocal()
snapshots = session.query(Snapshot).order_by(Snapshot.fetched_at.desc()).limit(2).all()
session.close()

if len(snapshots) < 2:
    print("Need at least 2 snapshots to diff. Run scripts.run_fetch twice first.")
else:
    newer, older = snapshots[0], snapshots[1]
    print(f"Comparing snapshot #{older.id} -> snapshot #{newer.id}")

    changes = compare_snapshots(older.id, newer.id)
    print(f"Found {len(changes)} changes.")
    for c in changes:
        print(c)

    if changes:
        saved_count = save_changes(changes, older.id, newer.id)
        print(f"Saved {saved_count} changes to the database.")


if changes:
    report = build_report(changes)
    print("\n--- REPORT ---\n")
    print(report)