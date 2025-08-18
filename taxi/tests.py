from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Manufacturer, Car, Driver
from taxi.forms import validate_license_number


class LicenseValidationTest(TestCase):
    def test_valid_license_number(self):
        valid_number = "ABC12345"
        self.assertEqual(validate_license_number(valid_number), valid_number)

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB1234")

    def test_invalid_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AbC12345")

    def test_invalid_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12A45")


class SearchFeatureTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="pass", license_number="AAA00001"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer2
        )

        self.driver1 = get_user_model().objects.create_user(
            username="john",
            password="12345",
            license_number="BBB00001"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="jack",
            password="12345",
            license_number="CCC00001"
        )

        self.car1.drivers.add(self.driver1)

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?search=john"
        )
        self.assertContains(response, "john")
        self.assertNotContains(response, "jack")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?search=Corolla"
        )
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "X5")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search=Toyota"
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_driver_car_relation(self):
        self.assertIn(self.driver1, self.car1.drivers.all())
        self.assertNotIn(self.driver2, self.car1.drivers.all())


class CoreViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice",
            password="pass",
            license_number="AAA00001"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer
        )
        self.driver = self.user

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)

    def test_toggle_assign_to_car(self):
        self.assertNotIn(self.driver, self.car.drivers.all())
        self.client.get(reverse(
            "taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.car.refresh_from_db()
        self.assertIn(self.driver, self.car.drivers.all())
        self.client.get(reverse(
            "taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.car.refresh_from_db()
        self.assertNotIn(self.driver, self.car.drivers.all())
