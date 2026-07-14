import sys
sys.path.insert(0, '.')
import sqlite3
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ── sqlite3 is built into Python — no installation needed
# ── Creates a local .db file — like a mini database on your PC

DB_NAME = "pipeline_tracker.db"

# ══ STEP 1: Connect and Create Table ══

def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        logging.info(f"Connected to database: {DB_NAME}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Connection failed: {e}")
        return None

def create_tables(conn):
    cursor = conn.cursor()
    try:
        # Create pipeline_runs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                pipeline    TEXT NOT NULL,
                status      TEXT NOT NULL,
                records_in  INTEGER,
                records_out INTEGER,
                run_date    TEXT
            )
        """)

        # Create data_quality_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dq_log (
                log_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id       INTEGER,
                rule_name    TEXT,
                passed       INTEGER,
                failed_rows  INTEGER,
                FOREIGN KEY (run_id) REFERENCES pipeline_runs(run_id)
            )
        """)

        conn.commit()
        logging.info("Tables created successfully")
    except sqlite3.Error as e:
        logging.error(f"Table creation failed: {e}")
    finally:
        cursor.close()

# ══ STEP 2: INSERT ══

def log_pipeline_run(conn, pipeline, status, records_in, records_out):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO pipeline_runs
            (pipeline, status, records_in, records_out, run_date)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (pipeline, status, records_in, records_out))

        conn.commit()
        run_id = cursor.lastrowid
        logging.info(f"Pipeline run logged — run_id: {run_id}")
        return run_id
    except sqlite3.Error as e:
        logging.error(f"Insert failed: {e}")
        return None
    finally:
        cursor.close()

def log_dq_check(conn, run_id, rule_name, passed, failed_rows):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO dq_log
            (run_id, rule_name, passed, failed_rows)
            VALUES (?, ?, ?, ?)
        """, (run_id, rule_name, passed, failed_rows))

        conn.commit()
        logging.info(f"DQ check logged: {rule_name} — passed: {bool(passed)}")
    except sqlite3.Error as e:
        logging.error(f"DQ log insert failed: {e}")
    finally:
        cursor.close()

# ══ STEP 3: SELECT ══

def get_all_runs(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pipeline_runs")
        rows = cursor.fetchall()
        logging.info(f"Fetched {len(rows)} pipeline runs")
        return rows
    except sqlite3.Error as e:
        logging.error(f"Select failed: {e}")
        return []
    finally:
        cursor.close()

def get_run_by_id(conn, run_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM pipeline_runs WHERE run_id = ?",
            (run_id,)
        )
        row = cursor.fetchone()   # fetchone — only one record
        return row
    except sqlite3.Error as e:
        logging.error(f"Select by id failed: {e}")
        return None
    finally:
        cursor.close()

def get_failed_runs(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT pipeline, status, records_in, records_out, run_date
            FROM pipeline_runs
            WHERE status = 'failed'
        """)
        rows = cursor.fetchall()
        logging.info(f"Found {len(rows)} failed runs")
        return rows
    except sqlite3.Error as e:
        logging.error(f"Failed runs query failed: {e}")
        return []
    finally:
        cursor.close()

# ══ STEP 4: UPDATE ══

def update_run_status(conn, run_id, new_status):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE pipeline_runs
            SET status = ?
            WHERE run_id = ?
        """, (new_status, run_id))
        conn.commit()
        logging.info(f"Run {run_id} status updated to: {new_status}")
    except sqlite3.Error as e:
        logging.error(f"Update failed: {e}")
    finally:
        cursor.close()

# ══ STEP 5: DELETE ══

def delete_run(conn, run_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM pipeline_runs WHERE run_id = ?",
            (run_id,)
        )
        conn.commit()
        logging.info(f"Run {run_id} deleted")
    except sqlite3.Error as e:
        logging.error(f"Delete failed: {e}")
    finally:
        cursor.close()

# ══ MAIN EXECUTION ══

print("=" * 60)
print("PIPELINE TRACKER — DATABASE PROGRAMMING DEMO")
print("=" * 60)

# Connect
conn = create_connection()
if not conn:
    exit()

# Create tables
create_tables(conn)

# INSERT — log 3 pipeline runs
print("\n--- Logging pipeline runs ---")
run1 = log_pipeline_run(conn, "NYC Taxi Bronze", "completed", 10000, 10000)
run2 = log_pipeline_run(conn, "NYC Taxi Silver", "failed",    10000, 0)
run3 = log_pipeline_run(conn, "NYC Taxi Gold",   "completed", 9500,  100)

# INSERT — log DQ checks for run1
print("\n--- Logging DQ checks ---")
log_dq_check(conn, run1, "no_nulls_in_id",        passed=1, failed_rows=0)
log_dq_check(conn, run1, "trip_duration_positive", passed=1, failed_rows=0)
log_dq_check(conn, run2, "no_nulls_in_id",        passed=0, failed_rows=500)

# SELECT ALL
print("\n--- All pipeline runs ---")
all_runs = get_all_runs(conn)
for run in all_runs:
    print(run)

# SELECT ONE
print("\n--- Single run by ID ---")
single = get_run_by_id(conn, run1)
print(f"fetchone() result: {single}")

# SELECT with filter
print("\n--- Failed runs only ---")
failed = get_failed_runs(conn)
for f in failed:
    print(f)

# UPDATE
print("\n--- Updating failed run status ---")
update_run_status(conn, run2, "restarted")

# Verify update
updated = get_run_by_id(conn, run2)
print(f"After update: {updated}")

# DELETE
print("\n--- Deleting run 3 ---")
delete_run(conn, run3)

# Verify delete
print("\n--- All runs after delete ---")
remaining = get_all_runs(conn)
for run in remaining:
    print(run)

# Always close connection
conn.close()
logging.info("Database connection closed")