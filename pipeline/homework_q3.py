import pandas as pd
from sqlalchemy import create_engine

url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
url_zones = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "ehail_fee": "float64",
    "trip_type": "Int64",
    "cbd_congestion_fee": "float64"
}

parse_dates = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

dtype_zones = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}

df = pd.read_parquet(
    url
)

df_zones = pd.read_csv(
    url_zones,
    dtype=dtype_zones
)

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')
df.to_sql(name='green_taxi_data', con=engine, if_exists='append')

df_zones.head(n=0).to_sql(name='zones', con=engine, if_exists='replace')
df_zones.to_sql(name='zones', con=engine, if_exists='append')

