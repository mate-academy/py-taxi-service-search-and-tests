from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US"
        )
        cls.driver = get_user_model().objects.create(
            username="Driver",
            first_name="Test",
            last_name="Black",
            license_number="ABC12345"
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(str(self.manufacturer), "Test Manufacturer US")

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_create_driver_with_license_number(self) -> None:
        self.assertEqual(self.driver.username, "Driver")
        self.assertEqual(self.driver.first_name, "Test")
        self.assertEqual(self.driver.last_name, "Black")
        self.assertEqual(self.driver.license_number, "ABC12345")

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), "Test")

    def test_driver_car_relationship(self) -> None:
        car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)
        self.assertIn(self.driver, car.drivers.all())


class PublicManufacturerListViewTests(TestCase):

    def test_login_required(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self) -> None:
        url = reverse("taxi:manufacturer-list")
        Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="US"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Germany"
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Test Manufacturer1")
        self.assertContains(res, "Test Manufacturer2")
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateSearchTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

        self.manufacturer_matched = Manufacturer.objects.create(
            name="Toyota Motor", country="Japan"
        )
        self.manufacturer_unmatched = Manufacturer.objects.create(
            name="Ford Company", country="USA"
        )

        self.car_matched = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer_matched
        )
        self.car_unmatched = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer_unmatched
        )

        self.driver_matched = get_user_model().objects.create_user(
            username="driver_speedy",
            password="password123",
            license_number="AAA12345"
        )
        self.driver_unmatched = get_user_model().objects.create_user(
            username="racer_pro",
            password="password123",
            license_number="BBB12345"
        )

    def test_search_manufacturer_by_name(self) -> None:

        url = reverse("taxi:manufacturer-list")

        res = self.client.get(url, {"manufacturer_name": "toyota"})

        self.assertEqual(res.status_code, 200)
        self.assertIn(
            self.manufacturer_matched, res.context["manufacturer_list"])
        self.assertNotIn(
            self.manufacturer_unmatched, res.context["manufacturer_list"])

    def test_search_car_by_model(self) -> None:

        url = reverse("taxi:car-list")

        res = self.client.get(url, {"model": "camry"})

        self.assertEqual(res.status_code, 200)
        self.assertIn(self.car_matched, res.context["car_list"])
        self.assertNotIn(self.car_unmatched, res.context["car_list"])

    def test_search_driver_by_username(self) -> None:

        url = reverse("taxi:driver-list")

        res = self.client.get(url, {"username": "speed"})

        self.assertEqual(res.status_code, 200)
        self.assertIn(self.driver_matched, res.context["driver_list"])
        self.assertNotIn(self.driver_unmatched, res.context["driver_list"])

    def test_search_empty_results(self) -> None:

        url = reverse("taxi:manufacturer-list")

        res = self.client.get(url, {"manufacturer_name": "NonExistent"})

        self.assertEqual(res.status_code, 200)

        self.assertEqual(len(res.context["manufacturer_list"]), 0)
