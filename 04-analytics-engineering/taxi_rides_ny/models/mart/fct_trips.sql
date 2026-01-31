with trips as (
    select *
    from {{ ref('int_trips_unioned') }}
),

trips_enriched as (
    select
        t.*,
        ROW_NUMBER() over (
            partition by 
                pickup_location_id, 
                dropoff_location_id, 
                pickup_datetime, 
                dropoff_datetime, 
                vendor_id
            order by 
                t.pickup_datetime
        ) as rn
    from trips t)

select * from trips_enriched where rn > 1