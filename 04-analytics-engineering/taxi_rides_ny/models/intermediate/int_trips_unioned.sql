with green_trip_data as (
    select *
    from {{ ref('stg_green_tripdata') }}
),
yellow_trip_data as (
    select *
    from {{ ref('stg_yellow_tripdata') }}
),

trips_unioned as (
    select * from green_trip_data
    union all
    select * from yellow_trip_data
)
SELECT * FROM trips_unioned