
## Question 1. What's the version of pip in the python:3.13 image? (1 point)

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?

- 25.3

> docker run -it --rm --entrypoint bash python:3.13 -lc "pip --version"
> pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)


## Question 2. Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database? (1 point)



Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- db:5432



## ## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?


- 8,007

```sql
SELECT COUNT(*) 
FROM green_taxi_data
WHERE trip_distance <= 1.0
  AND lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime <  '2025-12-01';

```


## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

- "2025-11-14"	88.03

```sql
SELECT 
    DATE(lpep_pickup_datetime) AS pickup_day,
    MAX(trip_distance) AS max_distance
FROM green_taxi_data
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;

```

## Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?


- "East Harlem North"	9281.919999999996

```sql
SELECT 
    z."Zone" AS pickup_zone,
    SUM(g."total_amount") AS total_revenue
FROM green_taxi_data g
JOIN zones z
    ON g."PULocationID" = z."LocationID"
WHERE 
    g."lpep_pickup_datetime" >= '2025-11-18'
    AND g."lpep_pickup_datetime" <  '2025-11-19'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;

```


## Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.



```sql
SELECT 
    z_drop."Zone" AS dropoff_zone,
    SUM(g."tip_amount") AS total_tip
FROM green_taxi_data g
JOIN zones z_pick
    ON g."PULocationID" = z_pick."LocationID"
JOIN zones z_drop
    ON g."DOLocationID" = z_drop."LocationID"
WHERE 
    z_pick."Zone" = 'East Harlem North'
    AND g."lpep_pickup_datetime" >= '2025-11-01'
    AND g."lpep_pickup_datetime" <  '2025-12-01'
GROUP BY z_drop."Zone"
ORDER BY total_tip DESC
-- LIMIT 1;


```