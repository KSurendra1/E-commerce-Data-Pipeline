
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customers;

-- Create the dimension table for customers
CREATE TABLE dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_age INT,
    customer_gender VARCHAR(50)
);

-- Create the fact table for sales
CREATE TABLE fact_sales (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES dim_customers(customer_id),
    product_id VARCHAR(50),
    category VARCHAR(50),
    order_date DATE,
    quantity INT,
    total_amount DECIMAL(10, 2),
    shipping_cost DECIMAL(10, 2),
    profit_margin DECIMAL(10, 2),
    payment_method VARCHAR(50),
    region VARCHAR(50),
    returned BOOLEAN
);
