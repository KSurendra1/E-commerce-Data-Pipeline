import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'ecom_data',
    'user': 'postgres',
    'password': '12345'
}

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the database.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_data_from_db(conn, query):
    """Fetches data from the database using a given query."""
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def visualize_sales_by_region(conn):
    """
    Generates a bar chart showing total sales by region.
    Business Problem: What are our top-performing regions?
    """
    query = """
    SELECT region, SUM(total_amount) AS total_sales
    FROM fact_sales
    GROUP BY region
    ORDER BY total_sales DESC;
    """
    sales_by_region = fetch_data_from_db(conn, query)
    
    if not sales_by_region.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(x='region', y='total_sales', data=sales_by_region, palette='viridis')
        plt.title('Total Sales by Region')
        plt.xlabel('Region')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No data to visualize for sales by region.")

def visualize_sales_by_gender(conn):
    """
    Generates a pie chart showing sales distribution by customer gender.
    Business Problem: Which customer gender segment contributes most to our revenue?
    """
    query = """
    SELECT dc.customer_gender, SUM(fs.total_amount) AS total_sales
    FROM fact_sales fs
    JOIN dim_customers dc ON fs.customer_id = dc.customer_id
    GROUP BY dc.customer_gender;
    """
    sales_by_gender = fetch_data_from_db(conn, query)
    
    if not sales_by_gender.empty:
        plt.figure(figsize=(8, 8))
        plt.pie(sales_by_gender['total_sales'], labels=sales_by_gender['customer_gender'], autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        plt.title('Sales Distribution by Customer Gender')
        plt.tight_layout()
        plt.show()
    else:
        print("No data to visualize for sales by gender.")

def visualize_monthly_sales(conn):
    """
    Generates a line chart showing sales trends over time.
    Business Problem: How have our sales performed month-over-month?
    """
    query = """
    SELECT
        EXTRACT(YEAR FROM order_date) AS year,
        EXTRACT(MONTH FROM order_date) AS month,
        SUM(total_amount) AS monthly_sales
    FROM fact_sales
    GROUP BY 1, 2
    ORDER BY 1, 2;
    """
    monthly_sales = fetch_data_from_db(conn, query)
    
    if not monthly_sales.empty:
        # Create a combined year-month column for plotting
        monthly_sales['year_month'] = pd.to_datetime(monthly_sales['year'].astype(int).astype(str) + '-' + monthly_sales['month'].astype(int).astype(str))
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='year_month', y='monthly_sales', data=monthly_sales, marker='o')
        plt.title('Monthly Sales Trend Over Time')
        plt.xlabel('Month')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("No data to visualize for monthly sales.")

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        try:
            # Generate all visualizations
            visualize_sales_by_region(conn)
            visualize_sales_by_gender(conn)
            visualize_monthly_sales(conn)
        finally:
            conn.close()
            print("Database connection closed.")
