import sqlite3
import pandas as pd

# Option 1: raw string (recommended)
db_path = r"C:/Users/20232726/Desktop/me/datachallenge2_addressingcrime/Addressing-real-world-crime-and-security-problems-with-data-science/data/BIGDATA.db"

# Option 2: escaped backslashes
# db_path = "C:\\Users\\20232726\\Desktop\\me\\datachallenge2_addressingcrime\\Addressing-real-world-crime-and-security-problems-with-data-science\\data\\BIGDATA.db"

# Option 3: forward slashes
# db_path = "C:/Users/20232726/Desktop/me/datachallenge2_addressingcrime/Addressing-real-world-crime-and-security-problems-with-data-science/data/BIGDATA.db"

conn = sqlite3.connect(db_path)

# Get list of columns
cols = [row[1] for row in conn.execute("PRAGMA table_info(burglary_data)")]

# Total rows
total = conn.execute("SELECT COUNT(*) FROM burglary_data").fetchone()[0]

# Compute null stats
stats = []
for c in cols:
    non_null = conn.execute(f"SELECT COUNT([{c}]) FROM burglary_data").fetchone()[0]
    nulls    = total - non_null
    stats.append((c, nulls, round(nulls/total*100,2)))

# Display
df = pd.DataFrame(stats, columns=["column","null_count","null_pct"]) \
       .sort_values("null_pct", ascending=False)
print(df)
