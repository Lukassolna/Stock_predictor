import psycopg2
import pandas as pd



def seb(password):
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname="PROJECT",
        user="postgres",
        password=password,  # Use the renamed variable here
        host="localhost",
        port="5432"
    )
    # Create a cursor object
    cur = conn.cursor()
    # Execute a query to select all rows from the 'SEB' table
    cur.execute("SELECT * FROM SEB;")
    # Fetch all rows
    rows = cur.fetchall()
    # Define column names
    column_names = ["date", "close", "Change", "Up", "Down", "Av up", "Av down", "Relative", "RSI"]
    # Create a DataFrame
    df_seb = pd.DataFrame(rows, columns=column_names)
    # Close the cursor and connection
    cur.close()
    conn.close()
    return df_seb
