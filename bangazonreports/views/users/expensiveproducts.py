"""Module for generating expensive products report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def expensive_products(request):
    """Function to build an HTML report of completed products"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT *
                FROM bangazonapi_Product
                WHERE bangazonapi_Product.price > 999 
            """)

            dataset = db_cursor.fetchall()

            expensive_products = {}

            for row in dataset:
                uid = row["id"]

                expensive_products[uid] = {}
                expensive_products[uid]["id"] = uid
                expensive_products[uid]["name"] = row["name"]
                expensive_products[uid]["price"] = row["price"]
                expensive_products[uid]["description"] = row["description"]

        list_of_expensive_products = expensive_products.values()

        template = 'users/list_of_expensive_products.html'
        context = {
            'expensive_products': list_of_expensive_products
        }

        return render(request, template, context)