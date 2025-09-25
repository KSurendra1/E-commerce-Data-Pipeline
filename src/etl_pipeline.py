# File: src/etl_pipeline.py

import pandas as pd
import psycopg2
from psycopg2 import sql

def connect_db(db_params):
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the database.")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def load_data_to_staging(conn, file_path):
    """
    Loads data from the CSV file into a staging table in the database.
    This is the "L" (Load) step in ELT.
    """
    try:
        # Step 1: Extract data from the CSV file
        df = pd.read_csv(file_path)
        cursor = conn.cursor()
        
        # Step 2: Perform initial cleaning and type conversion
        # Standardize column names
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Convert data types to match the database schema
        df['order_date'] = pd.to_datetime(df['order_date']).dt.date
        df['customer_age'] = pd.to_numeric(df['customer_age'], errors='coerce').fillna(0).astype(int)
        df['returned'] = df['returned'].map({'Yes': True, 'No': False})
        
        # Step 3: Data Quality Checks
        # Drop rows with duplicate order_id
        initial_rows = len(df)
        df.drop_duplicates(subset=['order_id'], inplace=True)
        dropped_rows = initial_rows - len(df)
        if dropped_rows > 0:
            print(f"Dropped {dropped_rows} duplicate rows.")

        print(f"Loading {len(df)} rows into the staging table...")

        # Clear existing data in the staging table before loading
        cursor.execute("TRUNCATE TABLE staging_ecommerce_sales;")
        
        # Insert data using a multi-row insert for efficiency
        # We prepare the values string with placeholders
        values_str = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO staging_ecommerce_sales ({','.join(df.columns)}) VALUES ({values_str})"
        
        # Prepare data for insertion
        data_to_insert = [tuple(row) for row in df.values]
        
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        print("Data loaded to staging table successfully.")
        
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        conn.rollback()
        print(f"Error loading data to staging: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()

def execute_transformation(conn, script_path):
    """
    Executes a SQL script for data transformation.
    This is the "T" (Transform) step in ELT.
    """
    try:
        with open(script_path, 'r') as file:
            sql_script = file.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_script)
        conn.commit()
        print("SQL transformation successful. Data is ready in dim_customers and fact_sales tables.")
        
    except FileNotFoundError:
        print(f"Error: The SQL script file {script_path} was not found.")
        return False
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error executing transformation script: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
    return True

def main():
    """
    Main function to run the ELT pipeline.
    """
    # Replace with your PostgreSQL connection details
    db_params = {
        "host": "localhost",
        "database": "ecom_data",
        "user": "postgres",
        "password": "12345"
    }

    raw_data_path = "data/raw/ecommerce_sales_34500.csv"
    transform_script_path = "sql/transform_data.sql"
    
    conn = connect_db(db_params)
    if not conn:
        return

    try:
        # Step 1: Load data from CSV to staging table
        load_data_to_staging(conn, raw_data_path)

        # Step 2: Execute SQL transformation to populate DW tables
        execute_transformation(conn, transform_script_path)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
