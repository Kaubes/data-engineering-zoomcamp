"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append
  connection: duckdb-default

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"

@bruin"""

import os
import json
from io import BytesIO
from datetime import datetime

import requests
import pandas as pd
def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ.get("BRUIN_VARS", "{}")).get("taxi_types", ["yellow"])

    # parse start/end timestamps
    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date)

    # generate list of month start dates between start and end (inclusive)
    start_month = start_ts.replace(day=1)
    end_month = end_ts.replace(day=1)
    months = pd.date_range(start=start_month, end=end_month, freq="MS")

    frames = []

    for taxi in taxi_types:
        for dt in months:
            year = dt.year
            month = dt.month
            url = (
                f"https://d37ci6vzurychx.cloudfront.net/trip-data/"
                f"{taxi}_tripdata_{year}-{month:02d}.parquet"
            )
            try:
                resp = requests.get(url, timeout=30)
                if resp.status_code != 200:
                    print(f"warning: unable to fetch {url} -> status {resp.status_code}")
                    continue
                buf = BytesIO(resp.content)
                try:
                    df = pd.read_parquet(buf)
                except Exception as e:
                    print(f"warning: failed to read parquet from {url}: {e}")
                    continue

                # Normalize pickup/dropoff datetime column names
                pickup_candidates = [
                    "tpep_pickup_datetime",
                    "lpep_pickup_datetime",
                    "pickup_datetime",
                ]
                dropoff_candidates = [
                    "tpep_dropoff_datetime",
                    "lpep_dropoff_datetime",
                    "dropoff_datetime",
                ]
                for c in pickup_candidates:
                    if c in df.columns:
                        df = df.rename(columns={c: "pickup_datetime"})
                        break
                for c in dropoff_candidates:
                    if c in df.columns:
                        df = df.rename(columns={c: "dropoff_datetime"})
                        break

                # Coerce datetimes
                if "pickup_datetime" in df.columns:
                    df["pickup_datetime"] = pd.to_datetime(
                        df["pickup_datetime"], errors="coerce"
                    )
                if "dropoff_datetime" in df.columns:
                    df["dropoff_datetime"] = pd.to_datetime(
                        df["dropoff_datetime"], errors="coerce"
                    )

                # Keep rows that fall within the requested window (by pickup time)
                if "pickup_datetime" in df.columns:
                    df = df[(df["pickup_datetime"] >= start_ts) & (df["pickup_datetime"] <= end_ts)]

                if not df.empty:
                    frames.append(df)

            except requests.RequestException as e:
                print(f"warning: request error for {url}: {e}")
                continue

    if frames:
        final_dataframe = pd.concat(frames, ignore_index=True)
    else:
        final_dataframe = pd.DataFrame(columns=["pickup_datetime", "dropoff_datetime"])

    return final_dataframe
  