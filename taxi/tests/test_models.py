from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name}"
                         f" {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="john",
            password="pass",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )
        self.assertEqual(str(driver), f"{driver.username}"
                                      f" ({driver.first_name}"
                                      f" {driver.last_name})")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="john",
            password="pass",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )
        url_from_method = driver.get_absolute_url()
        expected = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(url_from_method, expected)

    def test_get_absolute_url_resolves_view(self):
        driver = Driver.objects.create_user(
            username="john", password="pass", first_name="John",
            last_name="Doe", license_number="ABC123"
        )
        client = Client()
        client.force_login(user=driver)
        response = client.get(driver.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
