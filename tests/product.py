import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from bangazonapi.models import Product, Rating


class ProductTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Sporting Goods")

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        url = "/products"
        data = {
            "name": "Kite",
            "price": 14.99,
            "quantity": 60,
            "description": "It flies high",
            "category_id": 1,
            "location": "Pittsburgh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 14.99)
        self.assertEqual(json_response["quantity"], 60)
        self.assertEqual(json_response["description"], "It flies high")
        self.assertEqual(json_response["location"], "Pittsburgh")

    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        self.test_create_product()

        url = "/products/1"
        data = {
            "name": "Kite",
            "price": 24.99,
            "quantity": 40,
            "description": "It flies very high",
            "category_id": 1,
            "created_date": datetime.date.today(),
            "location": "Pittsburgh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 24.99)
        self.assertEqual(json_response["quantity"], 40)
        self.assertEqual(json_response["description"], "It flies very high")
        self.assertEqual(json_response["location"], "Pittsburgh")

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """
        self.test_create_product()
        self.test_create_product()
        self.test_create_product()

        url = "/products"

        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 3)

    def test_delete_product(self):
        """
        Ensure we can delete an existing product.
        """
        product = Product()
        product.name = "Equinox"
        product.customer_id = 1
        product.price = 537.51
        product.description = "2012 Chevy"
        product.quantity = 1
        product.created_date = "2019-01-28"
        product.category_id = 1
        product.location = "Sison"
        product.image_path = ""
        product.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/products/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET Product AGAIN TO VERIFY 404 response
        response = self.client.get(f"/products/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rating_product(self):
        """
        Ensure we can add a rating to a product and the average rating exists
        """
        product = Product()
        product.name = "Equinox"
        product.customer_id = 1
        product.price = 537.51
        product.description = "2012 Chevy"
        product.quantity = 1
        product.category_id = 1
        product.location = "Sison"
        product.image_path = ""
        product.can_be_rated = True
        product.save()

        rating = Rating()
        rating.customer_id = 1
        rating.product_id = 1
        rating.score = 3

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/products/{product.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["name"], product.name)
        self.assertEqual(json_response["price"], product.price)
        self.assertEqual(json_response["description"], product.description)
        self.assertEqual(json_response["quantity"], product.quantity)
        self.assertEqual(json_response["created_date"], "2021-09-02")
        self.assertEqual(json_response["location"], product.location)
        self.assertEqual(json_response["image_path"], None)
        self.assertEqual(json_response["average_rating"], product.average_rating)