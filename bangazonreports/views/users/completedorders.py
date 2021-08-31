"""Module for generating completed orders report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def completed_orders(request):
    """Function to build an HTML report of completed orders"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT bangazonapi_order.id AS order_id, SUM(bangazonapi_product.price) AS total_price, auth_user.first_name || " " || auth_user.last_name AS customer_name, bangazonapi_payment.merchant_name AS payment_type
                FROM bangazonapi_Order
                LEFT JOIN bangazonapi_OrderProduct
                ON bangazonapi_OrderProduct.order_id = bangazonapi_order.id
                LEFT JOIN bangazonapi_Product
                ON bangazonapi_Product.id = bangazonapi_OrderProduct.product_id
                JOIN auth_user
                ON auth_user.id = bangazonapi_Order.customer_id
                JOIN bangazonapi_payment
                ON bangazonapi_payment.id = bangazonapi_order.payment_type_id
                WHERE bangazonapi_order.payment_type_id IS NOT NULL
                GROUP BY bangazonapi_order.id
            """)

            dataset = db_cursor.fetchall()

            completed_orders = {}

            for row in dataset:
                uid = row["order_id"]

                completed_orders[uid] = {}
                completed_orders[uid]["order_id"] = uid
                completed_orders[uid]["customer_name"] = row["customer_name"]
                completed_orders[uid]["total_price"] = row["total_price"]
                completed_orders[uid]["payment_type"] = row["payment_type"]

        list_of_completed_orders = completed_orders.values()

        template = 'users/list_of_completed_orders.html'
        context = {
            'completed_orders': list_of_completed_orders
        }

        return render(request, template, context)