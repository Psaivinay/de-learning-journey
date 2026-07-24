import sys
sys.path.insert(0, '.')
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ── Raw Bronze layer data — simulating what comes from API
bronze_data = {
    "trip_id":      [1,2,3,4,5,6,7,8,9,10,11,12],
    "pickup_city":  ["Mysore","Bangalore","Mysore","Hyderabad",
                     "Bangalore","Mysore","Hyderabad","Bangalore",
                     "Mysore","Hyderabad","Bangalore","Mysore"],
    "driver_id":    [101,102,101,103,102,104,103,102,101,103,104,104],
    "distance_km":  [5.2,3.1,8.4,2.0,6.5,4.1,9.2,1.5,7.3,3.8,5.5,6.2],
    "fare":         [150,90,240,60,190,120,270,45,210,110,165,185],
    "rating":       [4.5,3.8,4.9,None,4.2,3.5,None,4.8,4.1,3.9,4.6,4.3],
    "status":       ["completed","completed","cancelled","completed",
                     "completed","cancelled","completed","completed",
                     "cancelled","completed","completed","completed"],
    "trip_date":    ["2026-01-01","2026-01-01","2026-01-01","2026-01-01",
                     "2026-01-02","2026-01-02","2026-01-02","2026-01-02",
                     "2026-01-03","2026-01-03","2026-01-03","2026-01-03"],
}

df_bronze=pd.DataFrame(bronze_data)
logging.info(f"Bronze layer loaded :{df_bronze.shape[0]} rows")

print("Silver Layer-Cleaning and Transformation")

# SILVER LAYER

df_silver=df_bronze[df_bronze['status']=='completed'].copy()
logging.info(f"After removing cancelled rows {df_silver.shape[0]} rows")

#Filling null values with mean
mean_rating=df_silver['rating'].mean()
df_silver['rating']=df_silver['rating'].fillna(round(mean_rating,2))
logging.info(f"Null ratings filled with mean :{mean_rating:.2f} ")

# add calculated columns

df_silver['fare_per_km']=(df_silver['fare']/df_silver['distance_km']).round(2)

df_silver['trip_category']=df_silver['distance_km'].apply(
    lambda x: 'short' if x<4 else ('medium' if x<7 else 'long')
)

df_silver['trip_date']=pd.to_datetime(df_silver['trip_date'])

df_silver = df_silver.rename(columns={
    'pickup_city': 'city',
    'driver_id':   'driver_id',
    'distance_km': 'distance',
})

print(f"\nSilver layer — {df_silver.shape[0]} clean rows:")
print(df_silver[['trip_id','city','fare','fare_per_km',
                  'trip_category','rating']].to_string())

# Export silver

df_silver.to_csv('silver_trips.csv,index=False')
logging.info("Silver layer exported to silver_trips.csv")

#Gold Layer

revenue_by_city = (df_silver
    .groupby('city').fare
    .agg(['sum', 'mean', 'count'])
    .round(2)
    .rename(columns={
        'sum':   'total_revenue',
        'mean':  'avg_fare',
        'count': 'total_trips'
    })
    .sort_values('total_revenue', ascending=False)
    .reset_index()
)
print("\nKPI 1 — Revenue by City:")
print(revenue_by_city.to_string())

driver_performance = (df_silver
    .groupby('driver_id')
    .agg(
        total_trips    = ('trip_id',   'count'),
        total_revenue  = ('fare',      'sum'),
        avg_rating     = ('rating',    'mean'),
        avg_distance   = ('distance',  'mean'),
    )
    .round(2)
    .sort_values('total_revenue', ascending=False)
    .reset_index()
)
print("\nKPI 2 — Driver Performance:")
print(driver_performance.to_string())


# Gold KPI 3: Daily summary
daily_summary = (df_silver
    .groupby('trip_date')
    .agg(
        total_trips   = ('trip_id', 'count'),
        total_revenue = ('fare',    'sum'),
        avg_fare      = ('fare',    'mean'),
        avg_rating    = ('rating',  'mean'),
    )
    .round(2)
    .reset_index()
)
print("\nKPI 3 — Daily Summary:")
print(daily_summary.to_string())

# Gold KPI 4: Trip category breakdown
category_breakdown = (df_silver
    .groupby('trip_category')['fare']
    .agg(['count', 'sum', 'mean'])
    .round(2)
    .rename(columns={
        'count': 'trips',
        'sum':   'revenue',
        'mean':  'avg_fare'
    })
    .reset_index()
)
print("\nKPI 4 — Trip Category Breakdown:")
print(category_breakdown.to_string())

# Export Gold KPIs
revenue_by_city.to_csv('gold_revenue_by_city.csv', index=False)
driver_performance.to_csv('gold_driver_performance.csv', index=False)
daily_summary.to_csv('gold_daily_summary.csv', index=False)
logging.info("Gold KPIs exported to CSV files")

print("\n Bronze → Silver → Gold pipeline complete")
print("Files created:")
print("  silver_trips.csv")
print("  gold_revenue_by_city.csv")
print("  gold_driver_performance.csv")
print("  gold_daily_summary.csv")