from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver


class TaxiIndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")


class ViewsTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser", password="12345"
        )

    def test_manufacturer_list_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_list_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_list_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
