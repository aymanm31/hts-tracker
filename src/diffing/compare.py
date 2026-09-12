from src.db.connection import SessionLocal
from src.db.models import LineItem, Change
from src.diffing.keys import get_match_key

FIELDS_TO_COMPARE = ["description", "general_rate", "special_rate", "other_rate"]


def compare_snapshots(old_snapshot_id: int, new_snapshot_id: int) -> list[dict]:
    session = SessionLocal()
    try:
        old_items = session.query(LineItem).filter_by(snapshot_id=old_snapshot_id).all() if old_snapshot_id else []
        new_items = session.query(LineItem).filter_by(snapshot_id=new_snapshot_id).all()

        old_by_key = {get_match_key(item): item for item in old_items}
        new_by_key = {get_match_key(item): item for item in new_items}

        changes = []

        # Added rows: in new, not in old
        for key, new_item in new_by_key.items():
            if key not in old_by_key:
                changes.append({
                    "change_type": "added",
                    "htsno": new_item.htsno,
                    "chapter": new_item.chapter,
                    "section": new_item.section,
                    "description": new_item.description,
                    "field_changed": None,
                    "old_value": None,
                    "new_value": None,
                })

        # Removed rows: in old, not in new
        for key, old_item in old_by_key.items():
            if key not in new_by_key:
                changes.append({
                    "change_type": "removed",
                    "htsno": old_item.htsno,
                    "chapter": old_item.chapter,
                    "section": old_item.section,
                    "description": old_item.description,
                    "field_changed": None,
                    "old_value": None,
                    "new_value": None,
                })

        # Field changes: present in both, but values differ
        for key in old_by_key.keys() & new_by_key.keys():
            old_item = old_by_key[key]
            new_item = new_by_key[key]
            for field in FIELDS_TO_COMPARE:
                old_val = getattr(old_item, field)
                new_val = getattr(new_item, field)
                if old_val != new_val:
                    changes.append({
                        "change_type": "field_changed",
                        "htsno": new_item.htsno,
                        "chapter": new_item.chapter,
                        "section": new_item.section,
                        "description": new_item.description,
                        "field_changed": field,
                        "old_value": old_val,
                        "new_value": new_val,
                    })

        return changes
    finally:
        session.close()