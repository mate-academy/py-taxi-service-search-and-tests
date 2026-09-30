from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer


DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicPagesTests(TestCase):
    def test_login_required_for_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create_user(
            username="admin",
            password="test12345",
            license_number="ADM12345",
        )
        get_user_model().objects.create_user(
            username="taxi_driver",
            password="test12345",
            license_number="TAX12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer,
        )
        Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.get(name="BMW"),
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_driver_search_by_username(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "taxi"})

        self.assertContains(response, "taxi_driver")
        self.assertNotContains(response, "ADM12345")

    def test_car_search_by_model(self):
        response = self.client.get(CAR_LIST_URL, {"model": "cor"})

        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "X5")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "toy"})

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")


class DriverLicenseUpdateFormTests(TestCase):
    def test_license_number_is_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})

        self.assertTrue(form.is_valid())

    def test_license_number_with_invalid_length_is_not_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})

        self.assertFalse(form.is_valid())
