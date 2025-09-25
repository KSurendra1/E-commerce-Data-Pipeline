-- File: sql/reports.sql

-- 1. Total Sales and Profit by Region
-- This query calculates the total sales and profit for each geographical region,
-- showing a high-level overview of regional performance.
SELECT
    region,
    SUM(total_amount) AS total_sales,
    SUM(profit_margin) AS total_profit
FROM
    fact_sales
GROUP BY
    region
ORDER BY
    total_sales DESC;

-- 2. Top 5 Best-Selling Products by Quantity
-- This query identifies the top 5 products based on the total quantity sold,
-- which helps in inventory and marketing decisions.
SELECT
    product_id,
    SUM(quantity) AS total_quantity_sold
FROM
    fact_sales
GROUP BY
    product_id
ORDER BY
    total_quantity_sold DESC
LIMIT 5;

-- 3. Customer Demographics Analysis
-- This query counts the number of customers by age group and gender,
-- providing insights into the target audience.
SELECT
    customer_gender,
    CASE
        WHEN customer_age BETWEEN 18 AND 25 THEN '18-25'
        WHEN customer_age BETWEEN 26 AND 35 THEN '26-35'
        WHEN customer_age BETWEEN 36 AND 50 THEN '36-50'
        WHEN customer_age > 50 THEN '50+'
        ELSE 'Unknown'
    END AS age_group,
    COUNT(t1.customer_id) AS number_of_customers
FROM
    dim_customers AS t1
GROUP BY
    customer_gender,
    age_group
ORDER BY
    age_group,
    customer_gender;

-- 4. Monthly Revenue Trend
-- This query shows how total revenue and profit have changed over time on a monthly basis.
SELECT
    DATE_TRUNC('month', order_date) AS order_month,
    SUM(total_amount) AS monthly_revenue,
    SUM(profit_margin) AS monthly_profit
FROM
    fact_sales
GROUP BY
    order_month
ORDER BY
    order_month;

-- 5. Customer Return Rate by Category
-- This query calculates the percentage of returned products for each category,
-- helping to identify product categories with high return rates.
SELECT
    category,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN returned THEN 1 ELSE 0 END) AS returned_orders,
    (SUM(CASE WHEN returned THEN 1 ELSE 0 END) * 100.0) / COUNT(*) AS return_rate_percentage
FROM
    fact_sales
GROUP BY
    category
ORDER BY
    return_rate_percentage DESC;
