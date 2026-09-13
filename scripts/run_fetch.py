import src.config  # noqa: F401 — loads .env, must be imported first
from src.ingestion.fetch import fetch_hts
from src.ingestion.save import save_snapshot

print("Fetching HTS data...")
data = fetch_hts(from_code="0101", to_code="0105")  # small range for testing
print(f"Fetched {len(data)} rows.")

snapshot_id = save_snapshot(data)
print(f"Saved as snapshot #{snapshot_id}.")