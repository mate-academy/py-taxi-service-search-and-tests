from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer


DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class ValidLicenseNumberFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("DAF12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("ABC123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("RAF1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("FA123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("ABCD2345").is_valid())


class UpdateDriverLicenseNumberTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "ADM22345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "a5"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)


class DriverSearchViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="test12345", license_number="ADM12345"
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="bob", password="test12345", license_number="BOB12345"
        )

    def test_empty_search_returns_all_drivers(self):
        response = self.client.get(DRIVER_URL, {"username": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all()),
        )

    def test_search_filters_drivers_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "bo"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertContains(response, "bob")


class CarSearchViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="test12345", license_number="ADM12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Car1",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Car2",
            manufacturer=self.manufacturer
        )

    def test_empty_search_returns_all_cars(self):
        response = self.client.get(CAR_URL, {"model": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all()),
        )

    def test_search_filters_drivers_by_username(self):
        response = self.client.get(CAR_URL, {"car_model": "2"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertContains(response, "Car2")


class ManufacturerSearchViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="test12345", license_number="ADM12345"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test1",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test2",
            country="UK"
        )

    def test_empty_search_returns_all_drivers(self):
        response = self.client.get(MANUFACTURER_URL, {"name": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )

    def test_search_filters_drivers_by_username(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "2"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertContains(response, "Test2")
