import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Connect to the database
conn = sqlite3.connect('languages.db')

# Define the languages we want to track
target_languages = ['JavaScript', 'Python', 'Java', 'C++', 'PHP', 'Ruby', 'C']

# Languages to label first and last data points
languages_to_label = ['JavaScript', 'Python', 'Java']

# Query to get pushes for each target language by quarter
query = """
SELECT 
    year, 
    quarter, 
    language, 
    SUM(num_pushers) as pushers
FROM 
    languages 
WHERE 
    language_type = 'programming' AND
    year BETWEEN 2013 AND 2024 AND
    language IN ('JavaScript', 'Python', 'Java', 'C++', 'PHP', 'Ruby', 'C')
GROUP BY 
    year, quarter, language
ORDER BY 
    year, quarter, language
"""

# Load the data into a DataFrame
df = pd.read_sql_query(query, conn)

# Query to get total programming pushes by quarter
total_query = """
SELECT 
    year, 
    quarter, 
    SUM(num_pushers) as total_pushers
FROM 
    languages 
WHERE 
    language_type = 'programming' AND
    year BETWEEN 2013 AND 2024
GROUP BY 
    year, quarter
ORDER BY 
    year, quarter
"""

# Load the total pushes into a DataFrame
total_df = pd.read_sql_query(total_query, conn)

# Close the connection
conn.close()

# Merge the two dataframes
merged_df = pd.merge(df, total_df, on=['year', 'quarter'])

# Calculate percentage
merged_df['percentage'] = (merged_df['pushers'] / merged_df['total_pushers']) * 100

# Create a date column for proper time series plotting
merged_df['date'] = merged_df.apply(
    lambda row: datetime(int(row['year']), int(row['quarter']) * 3, 15), 
    axis=1
)

# Determine the first and last quarters in our data
min_date = merged_df['date'].min()
max_date = merged_df['date'].max()
first_quarter = f"{min_date.year} Q{(min_date.month + 2) // 3}"
last_quarter = f"{max_date.year} Q{(max_date.month + 2) // 3}"

# Create the plot
plt.figure(figsize=(14, 8))

# Define locator for consistent x-axis ticks and grid
quarter_locator = mdates.MonthLocator(bymonth=[1, 4, 7, 10], bymonthday=15)

# Plot each language as a separate line
colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6', '#f39c12', '#1abc9c', '#34495e']
for i, language in enumerate(target_languages):
    language_data = merged_df[merged_df['language'] == language]
    # Sort by date
    language_data = language_data.sort_values('date')
    
    line, = plt.plot(
        language_data['date'], 
        language_data['percentage'], 
        label=language, 
        linewidth=2,
        color=colors[i]
    )
    
    # Add labels for first and last data points for specific languages
    if language in languages_to_label:
        # First point
        first_point = language_data.iloc[0]
        plt.annotate(
            f"{int(round(first_point['percentage']))}%",
            xy=(first_point['date'], first_point['percentage']),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=9,
            fontweight='bold',
            color=colors[i]
        )
        
        # Middle point for language name
        middle_idx = len(language_data) // 2
        middle_point = language_data.iloc[middle_idx]
        plt.annotate(
            language,
            xy=(middle_point['date'], middle_point['percentage']),
            xytext=(0, 7),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold',
            color=colors[i],
            ha='center',
            backgroundcolor='white',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.7)
        )
        
        # Last point
        last_point = language_data.iloc[-1]
        plt.annotate(
            f"{int(round(last_point['percentage']))}%",
            xy=(last_point['date'], last_point['percentage']),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=9,
            fontweight='bold',
            color=colors[i]
        )

# Add labels and title
plt.xlabel('Year-Quarter')
plt.ylabel('Percentage of Total Programming Language Pushes (%)')
plt.title(f'Programming Language Trends ({first_quarter} - {last_quarter})')

# Set grid with alignment to quarter marks
plt.grid(True, linestyle='--', alpha=0.7)
plt.gca().xaxis.grid(True, which='major')

# Generate dates for all quarters from min_date to max_date
all_quarters = pd.date_range(start=min_date, end=max_date, freq='3ME')

# Set tick positions for every quarter
plt.gca().xaxis.set_major_locator(quarter_locator)

# Custom formatter to only show labels for Q1 of each year
def quarter_formatter(x, pos=None):
    date = mdates.num2date(x)
    month = date.month
    quarter = (month + 2) // 3
    if month == 1:  # Q1
        return f"{date.year} Q1"
    elif quarter in [2, 3, 4]:
        return f"Q{quarter}"
    return ''

plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(quarter_formatter))
plt.xticks(rotation=45)

# Add legend at the bottom
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=len(target_languages))

# Ensure labels aren't cut off
plt.tight_layout()

# Save the chart
plt.savefig('language_trends.png', dpi=300, bbox_inches='tight')
print("Chart saved as 'language_trends.png'")

# Display the chart
plt.show() 