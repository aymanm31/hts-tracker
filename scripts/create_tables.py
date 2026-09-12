from src.db.connection import engine
from src.db.models import Base

Base.metadata.create_all(engine)
print("Tables created (or already existed).")