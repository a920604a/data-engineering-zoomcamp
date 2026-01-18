import pandas as pd
from sqlalchemy import create_engine
from time import time

# 建立 DB 連線
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

# 1️⃣ 讀取 parquet（先取前 100 筆產生 schema）
df = pd.read_parquet('green_tripdata_2025-11.parquet').head(100)

print(pd.io.sql.get_schema(df, name='green_taxi_data', con=engine))

# 2️⃣ 分批寫入（parquet 無 iterator，手動切 chunks）
df_full = pd.read_parquet('green_tripdata_2025-11.parquet')

chunksize = 10000
total_rows = len(df_full)

for start in range(0, total_rows, chunksize):
    t_start = time()

    df_chunk = df_full.iloc[start:start + chunksize]

    # 若時間欄位尚未是 datetime（保守處理）
    if 'lpep_pickup_datetime' in df_chunk.columns:
        df_chunk.lpep_pickup_datetime = pd.to_datetime(df_chunk.lpep_pickup_datetime)
        df_chunk.lpep_dropoff_datetime = pd.to_datetime(df_chunk.lpep_dropoff_datetime)

    df_chunk.to_sql(
        name='green_taxi_data',
        con=engine,
        if_exists='append',
        index=False
    )

    t_end = time()
    print(f'Inserted rows {start}–{start + len(df_chunk)}, took {t_end - t_start:.3f} seconds')

print("All data has been processed.")

# 3️⃣ zones 表（維持原本 CSV）
df_zones = pd.read_csv('taxi_zone_lookup.csv')
df_zones.to_sql(name='zones', con=engine, if_exists='replace', index=False)
