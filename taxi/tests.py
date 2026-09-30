from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from taxi.models import Manufacturer, Driver, Car
from taxi.forms import validate_license_number


class LicenseValidationTests(TestCase):
    def test_valid_license_number(self):
        valid_number = "ABC12345"
        self.assertEqual(validate_license_number(valid_number), valid_number)

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")
        with self.assertRaises(ValidationError):
            validate_license_number("ABCD12345")

    def test_invalid_first_three_chars(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")
        with self.assertRaises(ValidationError):
            validate_license_number("12312345")

    def test_invalid_last_five_chars(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234A")


class TaxiSearchAndFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = Driver.objects.create_user(
            username="testdriver",
            password="password123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.m1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.m2 = Manufacturer.objects.create(name="Ford", country="USA")

        self.car1 = Car.objects.create(model="Corolla", manufacturer=self.m1)
        self.car2 = Car.objects.create(model="Mustang", manufacturer=self.m2)

        self.driver2 = Driver.objects.create_user(
            username="janedoe",
            password="password123",
            license_number="XYZ67890"
        )

    def test_manufacturer_search_feature(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

        response_empty = self.client.get(url, {"name": "Tesla"})
        self.assertEqual(response_empty.status_code, 200)
        self.assertNotContains(response_empty, "Toyota")

    def test_car_search_feature(self):
        url = reverse("taxi:car-list")

        response = self.client.get(url, {"model": "Corolla"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Mustang")

    def test_driver_search_feature(self):
        url = reverse("taxi:driver-list")

        response = self.client.get(url, {"username": "janedoe"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "janedoe")
        self.assertNotIn(self.user, response.context["driver_list"])

    def test_index_view_statistics(self):
        url = reverse("taxi:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 2)
        self.assertEqual(response.context["num_cars"], 2)
        self.assertEqual(response.context["num_manufacturers"], 2)

    def test_toggle_assign_to_car_feature(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car1.id])

        self.assertNotIn(self.car1, self.user.cars.all())

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertIn(self.car1, self.user.cars.all())

        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertNotIn(self.car1, self.user.cars.all())
