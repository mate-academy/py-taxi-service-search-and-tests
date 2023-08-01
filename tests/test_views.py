from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Car, Manufacturer

DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURES_URL = reverse("taxi:manufacturer-list")


class PublicDataTests(TestCase):
    def test_login_required_on_drivers_list_page(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_on_cars_list_page(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_on_manufactures_list_page(self):
        res = self.client.get(MANUFACTURES_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDataTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers_list(self):
        get_user_model().objects.create_user(
            username="test1",
            password="123456783",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="test2",
            password="123456783",
            license_number="ACB12345"
        )

        res = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        Car.objects.create(model="M1", manufacturer=manufacturer)
        Car.objects.create(model="M2", manufacturer=manufacturer)

        res = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        res = self.client.get(MANUFACTURES_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
