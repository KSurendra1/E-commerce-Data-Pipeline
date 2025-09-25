-- Active: 1758796168795@@127.0.0.1@5432@ecom_data
-- Staging table for raw ecommerce sales data
DROP TABLE IF EXISTS staging_ecommerce_sales;
CREATE TABLE staging_ecommerce_sales (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10,2),
    discount DECIMAL(5,2),
    quantity INT,
    payment_method VARCHAR(50),
    order_date DATE,
    delivery_time_days INT,
    region VARCHAR(50),
    returned BOOLEAN,
    total_amount DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    profit_margin DECIMAL(10,2),
    customer_age INT,
    customer_gender VARCHAR(50)
);