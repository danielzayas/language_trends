import sqlite3
import pandas as pd

# Connect to SQLite database (will be created if it doesn't exist)
conn = sqlite3.connect('languages.db')

# Read the CSV file
df = pd.read_csv('languages.csv')

# Write to SQLite database
df.to_sql('languages', conn, index=False, if_exists='replace')

# Close the connection
conn.close()

print('Database created successfully!') 