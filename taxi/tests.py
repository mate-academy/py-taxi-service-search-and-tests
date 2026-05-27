from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer

User = get_user_model()


class PublicViewsTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="test12345",
            license_number="ADM12345",
        )

        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1,
        )

        self.car2 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer2,
        )

        self.driver = User.objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="ABC12345",
        )

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"},
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_car(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cor"},
        )

        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "X5")

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "admin")


class FormTests(TestCase):
    def test_driver_license_valid(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )
        self.assertTrue(form.is_valid())

    def test_driver_license_invalid(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "abc111"}
        )
        self.assertFalse(form.is_valid())
