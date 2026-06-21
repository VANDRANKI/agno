"""One-off maintenance script for resetting the local SQLite trace store.

Drops the ``agno_spans`` table from the trace database so that a fresh
tracing session can begin.  This script is intentionally **not** imported
by any other module — it is meant to be run directly::

    python -m agno.table

WARNING: Running this script deletes all existing span data in the
database at the path configured below.  There is no confirmation prompt.
"""

import sqlite3

db_path = "tmp/traces.db"
table_name = "agno_spans"

if __name__ == "__main__":
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()
    print(f"Dropped table '{table_name}' from '{db_path}'.")
