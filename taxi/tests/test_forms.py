from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Subaru test")
        Car.objects.create(
            model="Boxer",
            manufacturer=manufacturer
        )
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Boxer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boxer")
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Subaru test")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Subaru"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subaru")
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="driver_test",
            password="12345driver",
            license_number="1234"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver_test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver_test")
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_license_number(self):
        get_user_model().objects.create_user(
            username="driver_test",
            password="12345driver",
            license_number="1234"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"license_number": "1234"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1234")
        self.assertTemplateUsed(response, "taxi/driver_list.html")
