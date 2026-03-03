"""
Renames version_ids in bible.db to the user's preferred names.
This runs AFTER all downloads are complete.

Mapping:
  WEB -> NIV   (Modern English alternative)
  FBV -> NLT   (Easy-reading alternative)
  LSV -> AMP   (Literal/Amplified alternative)
  RV  -> NKJV  (Classic English alternative)
  DRA -> NASB  (Serious study alternative)
"""
import sqlite3

DB_PATH = "app/src/main/assets/bible.db"

RENAME_MAP = {
    "WEB": "NIV",
    "FBV": "NLT",
    "LSV": "AMP",
    "RV":  "NKJV",
    "DRA": "NASB",
}

def rename_versions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for old_id, new_id in RENAME_MAP.items():
        # Check if old version exists
        c.execute("SELECT COUNT(*) FROM verses WHERE version_id=?", (old_id,))
        count = c.fetchone()[0]
        if count == 0:
            print(f"  [SKIP] {old_id} not found in database")
            continue

        # Check if new ID already exists (avoid conflicts)
        c.execute("SELECT COUNT(*) FROM verses WHERE version_id=?", (new_id,))
        existing = c.fetchone()[0]
        if existing > 0:
            print(f"  [SKIP] {new_id} already exists ({existing} verses)")
            continue

        # Rename
        c.execute("UPDATE verses SET version_id=? WHERE version_id=?", (new_id, old_id))
        print(f"  [OK] {old_id} -> {new_id} ({count} verses renamed)")

    # Also update the versions table if it exists
    try:
        for old_id, new_id in RENAME_MAP.items():
            c.execute("UPDATE versions SET id=? WHERE id=?", (new_id, old_id))
    except:
        pass  # versions table might not exist

    conn.commit()
    conn.close()
    print("\nRenaming complete!")

if __name__ == "__main__":
    print("Renaming Bible versions...")
    rename_versions()
