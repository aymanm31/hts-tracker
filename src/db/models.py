from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True)
    fetched_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    source_version_label = Column(String, nullable=True)
    row_count = Column(Integer, nullable=True)


class LineItem(Base):
    __tablename__ = "line_items"

    id = Column(Integer, primary_key=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)

    # Raw fields straight from USITC
    htsno = Column(String, nullable=True)
    indent = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    superior = Column(Boolean, nullable=True)
    units = Column(JSON, nullable=True)
    general_rate = Column(String, nullable=True)
    special_rate = Column(String, nullable=True)
    other_rate = Column(String, nullable=True)
    footnotes = Column(JSON, nullable=True)
    quota_quantity = Column(String, nullable=True)
    additional_duties = Column(String, nullable=True)

    # fields derived (not in the raw api)
    chapter = Column(String, nullable=True)
    section = Column(String, nullable=True)
    is_heading = Column(Boolean, nullable=False, default=False)

    # for diffing
    sequence_index = Column(Integer, nullable=False)
    raw_json = Column(JSON, nullable=True)


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True)
    run_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=True)
    changes_found = Column(Boolean, nullable=False, default=False)
    email_sent = Column(Boolean, nullable=False, default=False)
    notes = Column(String, nullable=True)

class Change(Base):
    __tablename__ = "changes"

    id = Column(Integer, primary_key=True)
    old_snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=True)
    new_snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)

    htsno = Column(String, nullable=True)
    chapter = Column(String, nullable=True)
    section = Column(String, nullable=True)
    description = Column(String, nullable=True)

    change_type = Column(String, nullable=False)
    field_changed = Column(String, nullable=True)
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)

    detected_at = Column(DateTime, nullable=False, default=datetime.utcnow)