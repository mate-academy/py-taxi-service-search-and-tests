from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class TestViewsSetUp(TestCase):
    def setUp(self) -> None:
        self.search_name = "test"
        self.driver = Driver.objects.create(
            username="test1",
            password="test123",
            first_name="Test First",
            last_name="test_last",
            license_number="AEC11111"
        )

        Driver.objects.create(
            username="test2",
            password="test123",
            first_name="Test First",
            last_name="test_last",
            license_number="ZDC11111"
        )

        self.manufacturer = Manufacturer.objects.create(
            name=self.search_name,
            country="test")

        Manufacturer.objects.create(name="test2",
                                    country="test")

        self.car = Car.objects.create(
            model=self.search_name,
            manufacturer=self.manufacturer
        )

        self.user = get_user_model().objects.create_user(
            username="test3",
            password="test123345",
            license_number="TEX22222"
        )

        self.client.force_login(self.user)


class PublicManufacturerTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestViewsSetUp):
    def test_retrieve_manufacturers(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self) -> None:
        response = self.client.get(MANUFACTURER_URL, {"name": self.search_name})
        context_manufacturer = Manufacturer.objects.filter(
            name__icontains=self.search_name
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            context_manufacturer
        )


class PublicDriverTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestViewsSetUp):
    def test_retrieve_driver(self) -> None:
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response,
                                "taxi/driver_list.html")

    def test_search_driver_by_username(self) -> None:
        response = self.client.get(DRIVER_URL, {"username": self.search_name})
        context_driver = Driver.objects.filter(
            username__icontains=self.search_name
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context["driver_list"]),
            list(context_driver),
        )


class PublicCarTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestViewsSetUp):
    def test_retrieve_driver(self) -> None:
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response,
                                "taxi/car_list.html")

    def test_search_car_by_model(self) -> None:
        """Test that we can find Driver by name"""
        response = self.client.get(
            CAR_URL,
            {"model": self.search_name})
        context_cars = Car.objects.filter(
            model__icontains=self.search_name
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            context_cars,
        )


class ToggleAssignToCarTestCase(TestViewsSetUp):
    def test_toggle_assign_to_car(self) -> None:
        url = reverse("taxi:toggle-car-assign",
                      args=[self.car.pk])
        response = self.client.get(url)
        self.assertNotIn(self.car,
                         self.driver.cars.all()
                         )
        self.assertEqual(response.status_code, 302)
