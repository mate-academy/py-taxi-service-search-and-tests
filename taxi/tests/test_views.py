from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicTests(TestCase):
    def test_login_required_for_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_list(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="testpass123",
            license_number="ADM12345",
        )
        self.client.force_login(self.user)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

        self.car_1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="X5", manufacturer=self.manufacturer_2
        )

        self.driver_2 = get_user_model().objects.create_user(
            username="jane.doe",
            password="testpass123",
            license_number="JAN12345",
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "toy"})

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_manufacturer_search_empty_returns_all(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})

        self.assertContains(response, "Toyota")
        self.assertContains(response, "BMW")

    def test_car_search_by_model(self):
        response = self.client.get(CAR_LIST_URL, {"model": "cam"})

        self.assertContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_driver_search_by_username(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "jane"})
        driver_list = response.context["driver_list"]

        self.assertEqual(list(driver_list), [self.driver_2])

    def test_driver_search_no_match_returns_empty_list(self):
        response = self.client.get(
            DRIVER_LIST_URL, {"username": "nonexistent"}
        )

        self.assertEqual(len(response.context["driver_list"]), 0)


class ToggleAssignToCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="testpass123",
            license_number="ADM12345",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry", manufacturer=manufacturer
        )

    def test_assign_driver_to_car(self):
        self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.id})
        )

        self.assertIn(self.user, self.car.drivers.all())

    def test_unassign_driver_from_car(self):
        self.car.drivers.add(self.user)

        self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.id})
        )

        self.assertNotIn(self.user, self.car.drivers.all())
