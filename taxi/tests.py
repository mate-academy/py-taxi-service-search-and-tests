from django.test import TestCase
import unittest
from django.test import Client


class TaxiServiceTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_http_req_res_quantity_items_db(self):
        response = self.client.get("/drivers/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)

        response = self.client.get("/drivers/search/?search=w")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)

        response = self.client.get("/drivers/search/?search=adm")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)

        response = self.client.get("/cars/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 3)

        response = self.client.get("/cars/search/?search=werw")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 0)

        response = self.client.get("/cars/search/?search=dus")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)

        response = self.client.get("/cars/search/?search=Hyundai")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)

        response = self.client.get("/manufacturers/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

        response = self.client.get("/manufacturers/search/?search=sdsd")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

        response = self.client.get("/manufacturers/search/?search=renault")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

        response = self.client.get("/manufacturers/search/?search=re")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

        response = self.client.get("/manufacturers/search/?search=france")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
