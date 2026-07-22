import sys
sys.path.insert(0, '.')
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ── Sample DE pipeline data
data = {
    "trip_id":       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "pickup_city":   ["Mysore", "Bangalore", "Mysore", "Hyderabad",
                      "Bangalore", "Mysore", "Hyderabad", "Bangalore",
                      "Mysore", "Hyderabad"],
    "distance_km":   [5.2, 3.1, 8.4, 2.0, 6.5, 4.1, 9.2, 1.5, 7.3, 3.8],
    "fare":          [150, 90, 240, 60, 190, 120, 270, 45, 210, 110],
    "driver_rating": [4.5, 3.8, 4.9, None, 4.2, 3.5, None, 4.8, 4.1, 3.9],
    "status":        ["completed", "completed", "cancelled", "completed",
                      "completed", "cancelled", "completed", "completed",
                      "cancelled", "completed"],
}

df = pd.DataFrame(data)

print("=" * 60)
print("PANDAS BASICS — TRIP DATA ANALYSIS")
print("=" * 60)

# ── TASK 1: Basic exploration ──
print("\n--- Task 1: Explore the DataFrame ---")
print(f"Shape: {df.shape}")           # rows, columns
print(f"Columns: {list(df.columns)}")
print(f"Data types:\n{df.dtypes}")
print(f"\nFirst 3 rows:\n{df.head(3)}")
print(f"\nBasic stats:\n{df.describe()}")

# ── TASK 2: Selecting columns and rows ──
print("\n--- Task 2: Selecting ---")

# Select single column
print(f"\nAll fares:\n{df['fare']}")

# Select multiple columns
print(f"\nTrip summary:\n{df[['trip_id', 'pickup_city', 'fare']]}")

# loc — select by label
print(f"\nloc row 0, fare column: {df.loc[0, 'fare']}")
print(f"\nloc rows 0-2, city and fare:\n{df.loc[0:2, ['pickup_city','fare']]}")

# iloc — select by position
print(f"\niloc row 0, column 1: {df.iloc[0, 1]}")
print(f"\niloc first 3 rows, first 3 cols:\n{df.iloc[0:3, 0:3]}")

# ── TASK 3: Filtering rows ──
print("\n--- Task 3: Filtering ---")

# Completed trips only
completed = df[df['status'] == 'completed']
print(f"\nCompleted trips: {len(completed)}")

# High fare trips
high_fare = df[df['fare'] > 150]
print(f"High fare trips (>150): {len(high_fare)}")
print(high_fare[['trip_id', 'pickup_city', 'fare']])

# Multiple conditions
mysore_completed = df[
    (df['pickup_city'] == 'Mysore') &
    (df['status'] == 'completed')
]
print(f"\nMysore completed trips: {len(mysore_completed)}")

# ── TASK 4: Adding new columns ──
print("\n--- Task 4: New columns ---")

# Fare per km
df['fare_per_km'] = df['fare'] / df['distance_km']
df['fare_per_km'] = df['fare_per_km'].round(2)
print(f"\nFare per km added:\n{df[['trip_id','fare','distance_km','fare_per_km']]}")

# Category column using conditions
df['trip_category'] = df['distance_km'].apply(
    lambda x: 'short' if x < 4 else ('medium' if x < 7 else 'long')
)
print(f"\nTrip categories:\n{df[['trip_id','distance_km','trip_category']]}")

# ── TASK 5: Handling nulls ──
print("\n--- Task 5: Null handling ---")
print(f"\nNull counts:\n{df.isnull().sum()}")

# Fill nulls with mean
mean_rating = df['driver_rating'].mean()
df['driver_rating'] = df['driver_rating'].fillna(mean_rating)
print(f"\nAfter filling nulls with mean ({mean_rating:.2f}):")
print(df[['trip_id', 'driver_rating']])

# ── TASK 6: Export ──
df.to_csv('trips_cleaned.csv', index=False)
logging.info("Cleaned data exported to trips_cleaned.csv")

print("\n✅ All tasks complete")