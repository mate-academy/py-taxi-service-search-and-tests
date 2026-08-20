from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="roma",
            password="112322d",
            license_number="XYZ12345",
        )
        self.client.login(username="roma", password="112322d")

        self.driver = Driver.objects.create(
            username="romsa",
            password="1123s32d",
            license_number="BBD12345",
        )

    def test_driver_without_search(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "roma")

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"search": "roma"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "roma")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="roma",
            password="112322d",
            license_number="XYZ12345",
        )
        self.client.login(username="roma", password="112322d")

        manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer)
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer)

    def test_car_list_view_without_search(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Camry")

    def test_car_list_view_with_search(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Corolla"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")
