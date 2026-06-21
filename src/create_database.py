import pandas as pd
import sqlite3

df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

conn = sqlite3.connect("fintech.db")

df_users.to_sql(
    "users",
    conn,
    if_exists="replace",
    index=False
)

df_events.to_sql(
    "events",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Database created")