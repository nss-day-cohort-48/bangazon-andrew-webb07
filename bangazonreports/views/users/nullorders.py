"""Module for generating unpayed orders report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def null_orders(request):
    """Function to build an HTML report of orders without payment"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT bangazonapi_order.id AS order_id, 
                SUM(bangazonapi_product.price) AS total_price, 
                auth_user.first_name || " " || auth_user.last_name AS customer_name
                FROM bangazonapi_Order
                JOIN bangazonapi_OrderProduct
                ON bangazonapi_OrderProduct.order_id = bangazonapi_order.id
                JOIN bangazonapi_Product
                ON bangazonapi_Product.id = bangazonapi_OrderProduct.product_id
                JOIN auth_user
                ON auth_user.id = bangazonapi_Order.customer_id
                WHERE bangazonapi_order.payment_type_id IS NULL
                GROUP BY bangazonapi_order.id
            """)

            dataset = db_cursor.fetchall()

            null_orders = {}

            for row in dataset:
                uid = row["order_id"]

                null_orders[uid] = {}
                null_orders[uid]["order_id"] = uid
                null_orders[uid]["customer_name"] = row["customer_name"]
                null_orders[uid]["total_price"] = row["total_price"]

        list_of_null_orders = null_orders.values()

        template = 'users/list_of_null_orders.html'
        context = {
            'null_orders': list_of_null_orders
        }

        return render(request, template, context)