from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer(name="Test")
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "TestModel")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test_username",
            password="test111",
            first_name="test_first_name",
            last_name="test_last_name",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "test_username (test_first_name test_last_name)"
        )


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "test test_country")


class CarSearchTest(TestCase):
    def setUp(self):
        self.manufacturer_tesla = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.manufacturer_ford = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer_tesla
        )
        self.car2 = Car.objects.create(
            model="Model 3",
            manufacturer=self.manufacturer_tesla
        )
        self.car3 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer_ford
        )

    def test_search_existing_model(self):
        response = self.client.get(reverse("car_list") + "?q=Model S")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model S")
        self.assertNotContains(response, "Model 3")
        self.assertNotContains(response, "Mustang")

    def test_search_case_insensitive(self):
        response_lower = self.client.get(reverse("car_list") + "?q=mustang")
        response_upper = self.client.get(reverse("car_list") + "?q=MUSTANG")
        self.assertEqual(response_lower.content, response_upper.content)
