from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer


class TestForm(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
        )

    def test_driver_license_update_form_is_valid(self):
        form_data = {
            "license_number": "AMD12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_is_not_valid(self):
        form_data = {
            "license_number": "AM1234578"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_search_form_are_valid(self):
        cars_data = [
            {
                "model": "X5",
                "manufacturer": self.manufacturer,
            },
            {
                "model": "TEST",
                "manufacturer": self.manufacturer,
            },
            {
                "model": "123",
                "manufacturer": self.manufacturer,
            },
            {
                "model": "65",
                "manufacturer": self.manufacturer,
            },
        ]

        for car_data in cars_data:
            Car.objects.create(**car_data)

        url = reverse("taxi:car-list") + "?model=5"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 2)

    def test_driver_search_form_are_valid(self):
        drivers_data = [
            {
                "username": "bob",
                "password": "1234",
                "license_number": "AMD12345",
            },
            {
                "username": "jack",
                "password": "1234",
                "license_number": "AMD12545",
            },
            {
                "username": "mall",
                "password": "1234",
                "license_number": "AMD19345",
            },
            {
                "username": "some_guy",
                "password": "1234",
                "license_number": "AMD10345",
            },
        ]

        for driver_data in drivers_data:
            get_user_model().objects.create_user(**driver_data)

        url = reverse("taxi:driver-list") + "?username=g"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 1)

    def test_manufacturer_search_form_are_valid(self):
        manufacturers_data = [
            {
                "name": "G",
                "country": "USA",
            },
            {
                "name": "parag",
                "country": "USA",
            },
            {
                "name": "sequg",
                "country": "USA",
            },
            {
                "name": "gigig",
                "country": "USA",
            },
        ]

        for manufacturer_data in manufacturers_data:
            Manufacturer.objects.create(**manufacturer_data)

        url = reverse("taxi:manufacturer-list") + "?name=g"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 4)
