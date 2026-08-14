from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="TST12345"
        )
        self.client.force_login(self.user)

        self.man1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.man2 = Manufacturer.objects.create(name="Tesla", country="USA")

        self.car1 = Car.objects.create(model="Camry", manufacturer=self.man1)
        self.car2 = Car.objects.create(model="Model S", manufacturer=self.man2)

        self.driver1 = Driver.objects.create_user(
            username="john_doe",
            password="password123",
            license_number="JOH12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="alex_smith",
            password="password123",
            license_number="ALE12345"
        )

    def test_retrieve_manufacturers(self) -> None:
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            [self.man2, self.man1]
        )

    def test_search_manufacturer_by_name(self) -> None:
        res = self.client.get(MANUFACTURER_URL, data={"name": "toy"})
        self.assertIn(self.man1, res.context["manufacturer_list"])
        self.assertNotIn(self.man2, res.context["manufacturer_list"])

    def test_retrieve_cars(self) -> None:
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_car_by_model(self) -> None:
        res = self.client.get(CAR_URL, data={"model": "Model"})
        self.assertIn(self.car2, res.context["car_list"])
        self.assertNotIn(self.car1, res.context["car_list"])

    def test_retrieve_drivers(self) -> None:
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_driver_by_username(self) -> None:
        res = self.client.get(DRIVER_URL, data={"username": "john"})
        self.assertIn(self.driver1, res.context["driver_list"])
        self.assertNotIn(self.driver2, res.context["driver_list"])


class PublicViewsTests(TestCase):
    def test_login_required_for_views(self) -> None:
        res_man = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res_man.status_code, 200)

        res_car = self.client.get(CAR_URL)
        self.assertNotEqual(res_car.status_code, 200)

        res_driver = self.client.get(DRIVER_URL)
        self.assertNotEqual(res_driver.status_code, 200)
