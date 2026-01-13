# data-engineering-zoomcamp
Repository for the 2026 data engineering zoomcamp


## Homework non-code questions:

### Module 1: docker & Terraform

#### Question 1:
--> docker run -it --rm --entrypoint=bash python:3.13
--> pip -V
--> answer = 25.3

#### Question 2:
--> postgres application mapped to port 5432
--> pgadmin needs to point to the container name of the postgres application = postgres
--> answer = postgres:5432

#### Question 3:
--> python code that load the data provided in pipeline/homework_q3/py
--> SQL Query:
```sql
        select count(*)
        from public.green_taxi_data
        where lpep_pickup_datetime between '2025-11-01' and '2025-12-01'
        and trip_distance <= 1
```
--> answer = 8007

#### Question 4:
--> python code that load the data provided in pipeline/homework_q3/py
--> SQL Query:
```sql
        select cast(lpep_pickup_datetime AS date)
        from public.green_taxi_data
        where trip_distance = 
            (
            select MAX(trip_distance) 
            from public.green_taxi_data 
            where trip_distance < 100
            )
```
--> answer = 2025-11-14



#### Question 5:
--> python code that load the data provided in pipeline/homework_q3/py
--> SQL Query:
```sql
        select z."Zone", sum(total_amount) as summed_amount
        from public.green_taxi_data f
        left join public.zones z on f."PULocationID" = z."LocationID"
        where cast(lpep_pickup_datetime as date) = '2025-11-18'
        group by z."Zone"
        order by 2 desc
```
--> answer = East Harlem North

#### Question 6:
--> python code that load the data provided in pipeline/homework_q3/py
--> SQL Query:
```sql
        select do_z."Zone", max(tip_amount) as max_tip
        from public.green_taxi_data f
        left join public.zones pu_z on f."PULocationID" = pu_z."LocationID"
        left join public.zones do_z on f."DOLocationID" = do_z."LocationID"
        where pu_z."Zone" = 'East Harlem North'
            AND CAST(f."lpep_pickup_datetime" AS date) between '2025-11-01' and '2025-12-01'
        group by do_z."Zone"
        order by 2 desc
```
--> answer = Yorkville West

#### Question 7:
--> terraform code: see terraform_training file
--> we start with init to initialize terraform, then we do an apply to apply it in GCP and finaly a destroy to delete the created objects
--> answer = 4

