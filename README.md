E-commerce Data Warehouse Pipeline
This project demonstrates the design and implementation of a robust data pipeline for an e-commerce business. It showcases foundational skills in modern data engineering, including Extract, Load, and Transform (ELT) processes, data warehousing, and data visualization.

🚀 The Motivation
The core goal of this project is to take raw, messy e-commerce sales data and transform it into a clean, structured, and analytics-ready format. This addresses a common business problem: how to turn raw transactional data into a valuable asset for reporting and business intelligence.

By creating a data warehouse, we enable fast and efficient querying, allowing business analysts to easily answer critical questions about sales trends, customer behavior, and regional performance.

⚙️ Technologies Used
Python: The primary programming language for orchestrating the data pipeline.

Pandas: Used for data manipulation and initial cleaning of the raw CSV file.

Psycopg2: The PostgreSQL adapter for Python, used to connect to the database.

Matplotlib & Seaborn: Libraries for creating static data visualizations.

PostgreSQL: The relational database used to host the data warehouse.

SQL: Used for all data transformations and to perform business analysis.

Git: Version control for the entire project.

📊 Project Architecture
The pipeline follows a modern ELT (Extract, Load, Transform) approach.

Extract & Load: The Python script extracts data from a raw CSV file and loads it directly into a staging_ecommerce_sales table in the PostgreSQL database.

Transform: The transform_data.sql script is executed within the database to clean and normalize the data. This populates two key data warehouse tables:

dim_customers: A dimension table containing unique customer information.

fact_sales: A fact table with sales transactions, linked to the dim_customers table.

Analyze & Visualize: The clean, final data is ready for analysis using the queries in reports.sql and for visualization using the visualize_data.py script.

📁 Project Directory Structure
E-commerce-Data-Warehouse/
├── data/
│   ├── raw/
│   │   └── ecommerce_sales_34500.csv
│   └── processed/
├── sql/
│   ├── create_tables.sql
│   ├── transform_data.sql
│   └── reports.sql
├── src/
│   ├── etl_pipeline.py
│   └── visualize_data.py
├── .gitignore
├── README.md
└── requirements.txt

🔧 Setup and Execution
Follow these steps to set up and run the project locally.

Step 1: Clone the Repository
git clone <>
cd E-commerce-Data-Warehouse

Step 2: Set Up the Python Environment
Create a virtual environment (recommended) and install the dependencies:

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

Step 3: Database Setup
Ensure you have a PostgreSQL server running.

Create a new database for the project (e.g., ecom_data).

Execute the SQL commands from sql/create_tables.sql in your PostgreSQL client to create the necessary tables.

Open src/etl_pipeline.py and update the database connection details in the db_params dictionary.

Step 4: Place the Data File
Place the ecommerce_sales_34500.csv file into the data/raw/ directory.

Step 5: Run the Pipeline
Navigate to the project's root directory in your terminal and execute the main pipeline script:

python src/etl_pipeline.py

This will load the data into your PostgreSQL database.

Step 6: Generate Visualizations
To see the results of your pipeline, run the visualization script:

python src/visualize_data.py

This will generate several charts showing key business metrics.