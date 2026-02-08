SELECT 
    dispatching_base_num AS dispatching_base_number,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
    CAST(PUlocationID AS INT) AS pickup_location_id,
    CAST(DOlocationID AS INT) AS dropoff_location_id,
    CAST(SR_Flag AS INT) AS shared_ride_flag,
    CAST(Affiliated_base_number AS STRING) AS affiliated_base_number
FROM {{ source('raw_data', 'fhv_tripdata') }}
WHERE dispatching_base_num IS NOT NULL