from django.test import TestCase
from django.urls import reverse_lazy


class FormsTest(TestCase):
    def test_car_search_form(self):
        data = {
            "model": "test_model",
            "page": 1,
        }
        response = self.client.get(
            reverse_lazy("taxi:car-list"),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "model")
        self.assertContains(response, "page")

    def test_manufacturer_search_form(self):
        data = {
            "name": "test_name",
            "page": 1,
        }
        response = self.client.get(
            reverse_lazy("taxi:manufacturer-list"),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")
        self.assertContains(response, "page")

    def test_driver_search_form(self):
        data = {
            "username": "test_name",
            "page": 1,
        }
        response = self.client.get(
            reverse_lazy("taxi:driver-list"),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")
        self.assertContains(response, "page")
