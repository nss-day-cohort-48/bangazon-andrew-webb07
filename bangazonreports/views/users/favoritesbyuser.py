"""Module for generating favorites by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Favorite
from bangazonreports.views import Connection


def user_favorite_list(request):
    """Function to build an HTML report of favorites by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    f.id,
                    f.customer_id,
                    f.seller_id,
                    c.phone_number,
                    c.address,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    bangazonapi_favorite f
                JOIN
                    bangazonapi_customer c ON c.id = f.customer_id
                JOIN 
                    auth_user u ON c.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            favorites_by_user = {}

            for row in dataset:
                favorite = Favorite()
                favorite.customer_id = row["customer_id"]
                favorite.seller_id = row["seller_id"]

                uid = row["user_id"]

                if uid in favorites_by_user:

                    # Add the current game to the `games` list for it
                    favorites_by_user[uid]['favorites'].append(favorite)

                else:
                    # Otherwise, create the key and dictionary value
                    favorites_by_user[uid] = {}
                    favorites_by_user[uid]["id"] = uid
                    favorites_by_user[uid]["full_name"] = row["full_name"]
                    favorites_by_user[uid]["favorites"] = [favorite]

        list_of_users_with_favorites = favorites_by_user.values()

        template = 'users/list_with_users_favorites.html'
        context = {
            'user_favorite_list': list_of_users_with_favorites
        }

        return render(request, template, context)