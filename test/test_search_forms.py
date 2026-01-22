from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchCarFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="aboba",
            password="<PASSWORD_12345>",
            first_name="Andreww",
            last_name="SS",
        )
        self.manufacturer_1 = Manufacturer.objects.create(
            name="Audi",
            country="USA"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="RS6 Avant",
            manufacturer=self.manufacturer_1,
        )
        self.car = Car.objects.create(
            model="M5 F90",
            manufacturer=self.manufacturer_2,
        )
        self.client.force_login(self.user)

    def test_search_form(self):
        url = reverse("taxi:car-list")
        form_data = {
            "model": "RS6 Avant",
        }
        response = self.client.get(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RS6 Avant")
        self.assertNotContains(response, "M5 F90")


class SearchManufacturerFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="aboba",
            password="<PASSWORD_12345>",
            first_name="Andreww",
            last_name="SS",
        )
        self.manufacturer_1 = Manufacturer.objects.create(
            name="Audi",
            country="USA"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.client.force_login(self.user)

    def test_search_form(self):
        url = reverse("taxi:manufacturer-list")
        form_data = {
            "name": "Audi",
        }
        response = self.client.get(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "BMW")


class SearchDriverFormTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="aboba",
            password="<PASSWORD_12345>",
            first_name="Andreww",
            last_name="SS",
            license_number="LTE12345",
        )
        user_model.objects.create_user(
            username="pupa",
            password="<PASSWORD_1234fd5>",
            first_name="Iomap",
            last_name="FJifd",
            license_number="LTE14345",
        )

        self.client.force_login(self.user)

    def test_search_form(self):
        url = reverse("taxi:driver-list")
        form_data = {
            "username": "abo",
        }
        response = self.client.get(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "aboba")
        self.assertNotContains(response, "pupa")
