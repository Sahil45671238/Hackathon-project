CREATE DATABASE olist_db;
USE olist_db;
-- 1.1 Monthly orders, revenue, avg rating -- 

SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS yearmonth,
    COUNT(*) AS total_orders,
    SUM(COALESCE(p.payment_value, 0)) AS total_revenue,
    AVG(r.review_score) AS avg_review_score
FROM orders_prepared o
LEFT JOIN (
    SELECT 
        order_id,
        SUM(payment_value) AS payment_value
    FROM order_payments_prepared
    GROUP BY order_id
) p ON o.order_id = p.order_id
LEFT JOIN reviews_prepared r
    ON o.order_id = r.order_id
GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m')
ORDER BY yearmonth;

-- 1.2 Order status breakup over time

SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS yearmonth,
    order_status,
    COUNT(*) AS total_orders
FROM orders_prepared
GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m'), order_status
ORDER BY yearmonth, order_status;

-- 2.1 On‑time vs late: avg review
SELECT
    CASE 
        WHEN is_late = 1 THEN 'Late'
        WHEN is_late = 0 THEN 'On_time_or_early'
        ELSE 'No_delivery_info'
    END AS delivery_status,
    COUNT(*) AS total_orders,
    AVG(r.review_score) AS avg_review_score
FROM orders_prepared o
LEFT JOIN reviews_prepared r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY delivery_status;

-- 2.2 Delay buckets vs avg review
SELECT
    CASE
        WHEN delivery_delay_days IS NULL THEN 'No_info'
        WHEN delivery_delay_days <= 0 THEN 'On_time_or_early'
        WHEN delivery_delay_days BETWEEN 0 AND 5 THEN '0_5_days_late'
        WHEN delivery_delay_days BETWEEN 5 AND 10 THEN '5_10_days_late'
        ELSE '10+_days_late'
    END AS delay_bucket,
    COUNT(*) AS total_orders,
    AVG(r.review_score) AS avg_review_score
FROM orders_prepared o
LEFT JOIN reviews_prepared r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY delay_bucket
ORDER BY delay_bucket;

-- 3.1 State wise delivery + rating (customer_state)
SELECT
    c.customer_state,
    COUNT(*) AS total_orders,
    AVG(o.delivery_time_days) AS avg_delivery_time_days,
    AVG(o.delivery_delay_days) AS avg_delay_days,
    AVG(r.review_score) AS avg_review_score
FROM orders_prepared o
JOIN customers c
    ON o.customer_id = c.customer_id
LEFT JOIN reviews_prepared r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
HAVING COUNT(*) >= 100
ORDER BY avg_delay_days DESC;

-- 4.1 Category wise orders, revenue, avg rating

SELECT
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.price) AS total_revenue,
    SUM(oi.price) / COUNT(*) AS avg_price_per_item,
    AVG(r.review_score) AS avg_review_score
FROM order_items_prepared oi
LEFT JOIN products_prepared p
    ON oi.product_id = p.product_id
JOIN orders_prepared o
    ON oi.order_id = o.order_id
LEFT JOIN reviews_prepared r
    ON oi.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
HAVING COUNT(DISTINCT oi.order_id) >= 50    -- chhoti categories hatao
ORDER BY avg_review_score ASC;

-- 4.2 Category wise order volume top 10

SELECT
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) AS orders_count
FROM order_items_prepared oi
LEFT JOIN products_prepared p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY orders_count DESC;

-- payment wise order 
SELECT
    op.payment_type,
    COUNT(DISTINCT op.order_id) AS orders_count,
    AVG(p_tot.total_payment_value) AS avg_order_value
FROM order_payments_prepared op
LEFT JOIN (
    SELECT 
        order_id,
        SUM(payment_value) AS total_payment_value
    FROM order_payments_prepared
    GROUP BY order_id
) p_tot ON op.order_id = p_tot.order_id
GROUP BY op.payment_type;
