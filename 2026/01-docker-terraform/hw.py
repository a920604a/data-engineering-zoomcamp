import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

def question3():
    
    query = """
        SELECT 
            trip_distance, 
            lpep_pickup_datetime
        FROM public.green_taxi_data
            """

    # 使用 Pandas 讀取資料
    df = pd.read_sql(query, engine)
    print(    df.head(5) )


if __name__ == "__main__":
    question3()
   

    

