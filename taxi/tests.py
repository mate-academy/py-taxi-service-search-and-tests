from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicTests(TestCase):

    def test_login_required_for_lists(self):
        pages = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]
        for page in pages:
            response = self.client.get(page)
            self.assertNotEqual(response.status_code, 200)


class PrivateSearchTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
            license_number="ABC11111"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Tesla", country="USA")

        self.car1 = Car.objects.create(model="Camry", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="Model S", manufacturer=self.manufacturer2)

        self.driver1 = get_user_model().objects.create_user(
            username="driver_john",
            password="password123",
            license_number="AAA12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver_alex",
            password="password123",
            license_number="BBB54321"
        )

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": "Toy"})
        manufacturers = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer1, manufacturers)
        self.assertNotIn(self.manufacturer2, manufacturers)

    def test_search_car_by_model(self):
        url = reverse("taxi:car-list")

        response = self.client.get(url, {"model": "Model"})
        cars = response.context["car_list"]

        self.assertIn(self.car2, cars)
        self.assertNotIn(self.car1, cars)

    def test_search_driver_by_username(self):
        url = reverse("taxi:driver-list")

        response = self.client.get(url, {"username": "john"})
        drivers = response.context["driver_list"]

        self.assertIn(self.driver1, drivers)
        self.assertNotIn(self.driver2, drivers)


class FormValidationTests(TestCase):

    def test_validate_license_number_success(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        try:
            validate_license_number("XYZ98765")
        except ValidationError:
            self.fail("validate_license_number raised ValidationError unexpectedly!")

    def test_validate_license_number_wrong_length(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

        with self.assertRaises(ValidationError):
            validate_license_number("ABC123456")

    def test_validate_license_number_wrong_letters(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            validate_license_number("AbC12345")
        with self.assertRaises(ValidationError):
            validate_license_number("A1C12345")

    def test_validate_license_number_wrong_digits(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234A")
