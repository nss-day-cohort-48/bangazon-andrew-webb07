-- As a business analyst, I would like to see an HTML report showing all orders that have not been paid for yet.

-- Order Id
-- Customer name
-- Total cost of all items on the order

SELECT order.id, user.first_name || " " || user.last_name AS user.full_name, SUM(product.price)
FROM Order
JOIN OrderProduct
ON OrderProduct.order_id = order.id
JOIN Product
ON Product.id = OrderProduct.product_id
WHERE order.payment_type_id = "NULL"
GROUP BY order.payment_type_id

select *
from order