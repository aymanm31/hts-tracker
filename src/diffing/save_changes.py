from src.db.connection import SessionLocal
from src.db.models import Change


def save_changes(changes: list[dict], old_snapshot_id: int, new_snapshot_id: int) -> int:
    session = SessionLocal()
    try:
        change_objects = [
            Change(
                old_snapshot_id=old_snapshot_id,
                new_snapshot_id=new_snapshot_id,
                **c
            )
            for c in changes
        ]
        session.bulk_save_objects(change_objects)
        session.commit()
        return len(change_objects)
    finally:
        session.close()