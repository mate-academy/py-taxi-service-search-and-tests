from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
            license_number="ADM12345",
        )

        self.client.force_login(self.user)


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            "john ( )",
        )


class ManufacturerModelTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            "Toyota Japan",
        )


class CarModelTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car = Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer,
        )

    def test_car_str(self) -> None:
        self.assertEqual(
            str(self.car),
            self.car.model,
        )


class DriverViewTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )

    def test_driver_list_view(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "john",
        )


class CarViewTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car = Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer,
        )

    def test_car_list_view(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "BMW X5",
        )


class ManufacturerViewTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_manufacturer_list_view(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Toyota",
        )


class DriverSearchTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )

        Driver.objects.create_user(
            username="alex",
            password="test12345",
            license_number="XYZ12345",
        )

    def test_search_driver_by_username(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list"),
            {
                "username": "john",
            },
        )

        self.assertContains(
            response,
            "john",
        )

        self.assertNotContains(
            response,
            "alex",
        )


class CarSearchTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Car.objects.create(
            model="BMW X5",
            manufacturer=manufacturer,
        )

        Car.objects.create(
            model="Audi A6",
            manufacturer=manufacturer,
        )

    def test_search_car_by_model(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list"),
            {
                "model": "BMW",
            },
        )

        self.assertContains(
            response,
            "BMW X5",
        )

        self.assertNotContains(
            response,
            "Audi A6",
        )


class ManufacturerSearchTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

    def test_search_manufacturer_by_name(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {
                "name": "Toyota",
            },
        )

        self.assertContains(
            response,
            "Toyota",
        )

        self.assertNotContains(
            response,
            "BMW",
        )
