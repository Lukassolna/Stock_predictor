import psycopg2
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from global_var import omx
def sql_to_pandas(ticker,password):
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname="PROJECT",
        user="postgres",
        password=password,  
        host="localhost",
        port="5432"
    )
    
    cur = conn.cursor()
    
    cur.execute(f"SELECT * FROM {ticker} ;")
    # Fetch all rows
    rows = cur.fetchall()
    # Define column names
    column_names = ["date", "close", "Change", "Up", "Down", "Av up", "Av down", "Relative", "RSI"]
    
    df = pd.DataFrame(rows, columns=column_names)
    # Close the cursor and connection
    cur.close()
    conn.close()
    return df

def csv_to_sql(ticker, csv_file_path, password):
   
    df = pd.read_csv(csv_file_path)
    print(df)
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname="PROJECT",
        user="postgres",
        password=password,
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    ticker_table_name = ticker.replace('.', '_').replace('-', '_')

    # Create the table
    cur.execute(f"""
        CREATE TABLE {ticker_table_name} (
            date DATE,
            close NUMERIC,
            Change NUMERIC,
            Up NUMERIC,
            Down NUMERIC,
            Av_up NUMERIC,
            Av_down NUMERIC,
            Relative NUMERIC,
            RSI NUMERIC,
            SMA_10_close NUMERIC,
            percentage_diff NUMERIC,
            next_day_change NUMERIC,
            change_10 NUMERIC
        );
    """)
    conn.commit()

# Insert data into the table
  # Insert data into the table
    for _, row in df.iterrows():
        cur.execute(f"""
            INSERT INTO {ticker_table_name} (date, close, Change, Up, Down, Av_up, Av_down, Relative, RSI, SMA_10_close, percentage_diff, next_day_change, change_10)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, tuple(row))
    conn.commit()


    # Close the cursor and connection
    cur.close()
    conn.close()

def store_csv_in_sql_server(password):
    for ticker in omx:
        csv_file_path = f'new_csv_files/{ticker}.csv'
        print(csv_file_path)
        csv_to_sql(f'{ticker}', csv_file_path, password)
