-- Active: 1758796168795@@127.0.0.1@5432@ecom_data
-- SQL script to transform and load data from staging to dimensional tables

-- 1. Populate dim_customers (avoid duplicates)
INSERT INTO dim_customers (customer_id, customer_age, customer_gender)
SELECT DISTINCT customer_id, customer_age, customer_gender
FROM staging_ecommerce_sales
ON CONFLICT (customer_id) DO NOTHING;

-- 2. Populate fact_sales
INSERT INTO fact_sales (
    order_id, customer_id, product_id, category, order_date, quantity, total_amount, shipping_cost, profit_margin, payment_method, region, returned
)
SELECT 
    order_id, customer_id, product_id, category, order_date, quantity, total_amount, shipping_cost, profit_margin, payment_method, region, returned
FROM staging_ecommerce_sales
ON CONFLICT (order_id) DO NOTHING;