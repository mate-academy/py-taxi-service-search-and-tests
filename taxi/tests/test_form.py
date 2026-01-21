from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Driver, Car, Manufacturer


class DriverCreationFormTest(TestCase):
    def test_driver_creation_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "new_username",
            "password1": "<PASSWORD123>",
            "password2": "<PASSWORD123>",
            "first_name": "test first name",
            "last_name": "test last name",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )


class DriverSearchTests(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create_user(
            username="john_doe",
            password="testpass123",
            license_number="ADM12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="alice_smith",
            password="testpass123",
            license_number="ADM54321"
        )
        self.client.force_login(self.driver1)

    def test_search_by_username_returns_correct_result(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=john"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "alice_smith")


class CarSearchTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="alice_smith",
            password="testpass123",
            license_number="ADM54321"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Accord",
            manufacturer=self.manufacturer
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=civic"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Civic")
        self.assertNotContains(response, "Accord")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="alice_smith",
            password="testpass123",
            license_number="ADM54321"
        )
        self.client.force_login(self.driver)
        self.m1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.m2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=toy"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")
