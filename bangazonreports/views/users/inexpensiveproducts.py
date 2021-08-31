"""Module for generating inexpensive products report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def inexpensive_products(request):
    """Function to build an HTML report of completed products"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT *
                FROM bangazonapi_Product
                WHERE bangazonapi_Product.price < 1000 
            """)

            dataset = db_cursor.fetchall()

            inexpensive_products = {}

            for row in dataset:
                uid = row["id"]

                inexpensive_products[uid] = {}
                inexpensive_products[uid]["id"] = uid
                inexpensive_products[uid]["name"] = row["name"]
                inexpensive_products[uid]["price"] = row["price"]
                inexpensive_products[uid]["description"] = row["description"]

        list_of_inexpensive_products = inexpensive_products.values()

        template = 'users/list_of_inexpensive_products.html'
        context = {
            'inexpensive_products': list_of_inexpensive_products
        }

        return render(request, template, context)