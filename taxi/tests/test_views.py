from django.test import TestCase
from django.urls import reverse


class TestLoginRequired(TestCase):

    def test_car_list_view(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_view(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list_view(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)
