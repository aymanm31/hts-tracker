import src.config  # noqa: F401

from src.db.connection import SessionLocal
from src.db.models import Snapshot, Run
from src.ingestion.fetch import fetch_hts
from src.ingestion.save import save_snapshot
from src.diffing.compare import compare_snapshots
from src.diffing.save_changes import save_changes
from src.summarize.summarize import build_report
from src.notify.email_sender import send_email


def get_latest_snapshot_id():
    session = SessionLocal()
    try:
        latest = session.query(Snapshot).order_by(Snapshot.fetched_at.desc()).first()
        return latest.id if latest else None
    finally:
        session.close()


def log_run(snapshot_id, changes_found, email_sent, notes):
    session = SessionLocal()
    try:
        run = Run(
            snapshot_id=snapshot_id,
            changes_found=changes_found,
            email_sent=email_sent,
            notes=notes,
        )
        session.add(run)
        session.commit()
    finally:
        session.close()


def run_check(from_code="0101", to_code="9999"):
    old_snapshot_id = get_latest_snapshot_id()

    try:
        data = fetch_hts(from_code=from_code, to_code=to_code)
    except Exception as e:
        log_run(None, False, False, f"Fetch failed: {e}")
        print(f"Fetch failed: {e}")
        return

    new_snapshot_id = save_snapshot(data)
    print(f"Saved snapshot #{new_snapshot_id}")

    if old_snapshot_id is None:
        log_run(new_snapshot_id, False, False, "First run — no prior snapshot to compare against")
        print("First run, nothing to compare against yet.")
        return

    changes = compare_snapshots(old_snapshot_id, new_snapshot_id)

    if not changes:
        log_run(new_snapshot_id, False, False, "No changes detected")
        print("No changes detected.")
        return

    save_changes(changes, old_snapshot_id, new_snapshot_id)
    report = build_report(changes)

    email_sent = False
    try:
        send_email(
            subject=f"HTS Change Report — {len(changes)} change(s) detected",
            body=report,
        )
        email_sent = True
    except Exception as e:
        print(f"Email failed to send: {e}")

    log_run(new_snapshot_id, True, email_sent, f"{len(changes)} changes detected")
    print(f"Done. {len(changes)} changes found. Email sent: {email_sent}")