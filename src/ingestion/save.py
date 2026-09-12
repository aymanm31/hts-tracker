from datetime import datetime
from src.db.connection import SessionLocal
from src.db.models import Snapshot, LineItem
from src.ingestion.transform import transform_row


def save_snapshot(raw_data: list) -> int:
    session = SessionLocal()
    try:
        snapshot = Snapshot(fetched_at=datetime.utcnow(), row_count=len(raw_data))
        session.add(snapshot)
        session.flush()

        line_items = [
            LineItem(snapshot_id=snapshot.id, **transform_row(row, i))
            for i, row in enumerate(raw_data)
        ]
        session.bulk_save_objects(line_items)

        session.commit()
        return snapshot.id
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()