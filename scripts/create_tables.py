import src.config  # noqa: F401 — loads .env, must be imported first
from src.db.connection import engine
from src.db.models import Base

Base.metadata.create_all(engine)
print("Tables created (or already existed).")