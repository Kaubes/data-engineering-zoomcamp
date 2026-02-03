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

### Module 2: Workflow orchestration

#### Question 1: 
I ran a backfill for the data of 2020 for the yellow & green taxi
--> Searched for the csv file in my bucket and identified the file size
--> answer: 134.5 MB

#### Question 2:
I identified the variable in the kestra script which is: "{{inputs.taxi}}_tripdata_{{trigger.date | date('yyyy-MM')}}.csv"
--> filling in the input values in the brackets returns "green_tripdata_2020-04.csv"

#### Question 3:
I ran the following SQL query on the 'yellow_tripdata' table in BigQuery:

```sql
SELECT count(*) 
FROM `kestra-learning-485119.zoomcamp.yellow_tripdata` 
WHERE filename like 'yellow_tripdata_2020%'
```
Result: 24648499

#### Question 4:
I ran the following SQL query on the 'green_tripdata' table in BigQuery:

```sql
SELECT count(*) 
FROM `kestra-learning-485119.zoomcamp.green_tripdata`
WHERE filename like 'green_tripdata_2020%'
```
Result: 1734051

#### Question 5:
I ran a backfill for the data of march 2021 for the Yellow taxi.
I ran the following SQL query on the 'yellow_tripdata' table in BigQuery:

```sql
SELECT count(*) 
FROM `kestra-learning-485119.zoomcamp.yellow_tripdata` 
WHERE filename = 'yellow_tripdata_2021-03.csv'
```
Result: 1925152

#### Question 6:
In the flow code, under triggers, I clicked on the trigger type to pull up the documentation for 'io.kestra.plugin.core.trigger.Schedule'.
Searching through the available properties, I identified the 'timezone' field which contains a link to the wikipedia page. In the second column of the wikipedia page I searched for New York and found the corresponding timezone.

Result:
Property = 'timezone'
Value = 'America/New_York'

### Module 3: data warehouse

#### Question 1:
```sql
CREATE OR REPLACE EXTERNAL TABLE `datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3`
OPTIONS (
  format = 'parquet',
  uris = ['gs://de_zoomcamp_hw3_2026/yellow_tripdata_2024-*.parquet']
);

CREATE OR REPLACE TABLE datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3_non_partioned_table AS
SELECT * FROM datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3;

SELECT COUNT(*) from datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3

```
Result: 20332093

#### Question 2:

Created the below queries and then select them one by one to see the expected amount of data that will be read

```sql
SELECT COUNT(DISTINCT PULocationID) from `datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3`

SELECT COUNT(DISTINCT PULocationID) from `datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3_non_partioned_table`
```
Result: 0 MB and 155.12MB

#### Question 3:

Created the below queries and then select them one by one to see the expected amount of data that will be read

```sql
SELECT PULocationID from datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3_non_partioned_table
SELECT PULocationID, DOLocationID from datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3_non_partioned_table
```
Result: Answer 1

#### Question 4:
```sql
SELECT COUNT(*) FROM datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3_non_partioned_table WHERE fare_amount = 0
```
Result: 8333

#### Question 5:
```sql
CREATE OR REPLACE TABLE datawarehouse-485313.de_zoomcamp_hw3.yellow_tripdata_hw3_partioned
PARTITION BY
  DATE(tpep_dropoff_datetime) 
CLUSTER BY VendorID AS
SELECT * FROM datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3;
```
Result: Partition by tpep_dropoff_datetime and Cluster on VendorID

#### Question 6:
```sql
SELECT DISTINCT VendorID
FROM datawarehouse-485313.de_zoomcamp_hw3.external_yellow_tripdata_hw3_non_partioned_table
WHERE tpep_dropoff_datetime between '2024-03-01' and '2024-03-15'

SELECT DISTINCT VendorID
FROM datawarehouse-485313.de_zoomcamp_hw3.yellow_tripdata_hw3_partioned
WHERE tpep_dropoff_datetime between '2024-03-01' and '2024-03-15'

```
Result: 310.24 MB and 26.84 MB

#### Question 7:
External table is a link to a bucket in a GCP bucket so the data stays stored there.
Result: GCP Bucket

#### Question 8:
No, it's only a best practice if the column has a high cardinality, you filter on it frequently and the table is very large
Result: No

#### Question 9:
It stores data by columns and since we select everything it can't estimate how much data will be read









