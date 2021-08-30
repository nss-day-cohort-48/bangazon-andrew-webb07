-- As a business analyst, I would like to see an HTML report showing all orders that have not been paid for yet.

-- Order Id
-- Customer name
-- Total cost of all items on the order

SELECT bangazonapi_order.id AS order_id, SUM(bangazonapi_product.price) AS total_price, auth_user.first_name || " " || auth_user.last_name AS customer_name
FROM bangazonapi_Order
JOIN bangazonapi_OrderProduct
ON bangazonapi_OrderProduct.order_id = bangazonapi_order.id
JOIN bangazonapi_Product
ON bangazonapi_Product.id = bangazonapi_OrderProduct.product_id
JOIN auth_user
ON auth_user.id = bangazonapi_Order.customer_id
WHERE bangazonapi_order.payment_type_id IS NULL
GROUP BY auth_user.first_name
