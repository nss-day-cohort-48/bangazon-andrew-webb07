import json
from rest_framework import status
from rest_framework.test import APITestCase
from bangazonapi.models import Payment, Order


class OrderTests(APITestCase):
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

        # Create a product category
        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Create a product
        url = "/products"
        data = { "name": "Kite", "price": 14.99, "quantity": 60, "description": "It flies high", "category_id": 1, "location": "Pittsburgh" }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payment_type = Payment()
        payment_type.merchant_name = "Visa"
        payment_type.account_number = "121212121"
        payment_type.customer_id = 1
        payment_type.expiration_date = "2023-01-01"
        payment_type.create_date = "2021-09-01"
        payment_type.save()

    def test_change_order(self):
        """
        Ensure we can change an existing order.
        """
        order = Order()
        order.customer_id = 1
        order.payment_type_id = 1
        order.created_date = "2021-09-01"
        order.save()

        data = {
            "customer": 1,
            "payment_type": 1,
            "created_date": "2021-08-01"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/orders/{order.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get Order again to verify changes
        response = self.client.get(f"/orders/{order.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["created_date"], "2021-08-01")

    def test_add_product_to_order(self):
        """
        Ensure we can add a product to an order.
        """
        # Add product to order
        url = "/cart"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was added
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["payment_type"], None)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)


    def test_remove_product_from_order(self):
        """
        Ensure we can remove a product from an order.
        """
        # Add product
        self.test_add_product_to_order()

        # Remove product from cart
        url = "/cart/1"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was removed
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 0)
        self.assertEqual(len(json_response["lineitems"]), 0)

    # TODO: Complete order by adding payment type

    # TODO: New line item is not added to closed order