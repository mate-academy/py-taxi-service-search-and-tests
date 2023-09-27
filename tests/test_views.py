from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_manufacturer_list(self) -> None:
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_list(self) -> None:
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_list(self) -> None:
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            first_name="TestFirstName",
            last_name="TestLastName",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_view(self) -> None:
        Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(res.context["object_list"]),
            list(manufacturers)
        )

    def test_car_list_view(self) -> None:
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                name="test_name",
                country="test_country"
            )
        )

        res = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(
            list(res.context["object_list"]),
            list(cars)
        )

    def test_driver_list_view(self) -> None:
        get_user_model().objects.create_user(
            username="test_list_view",
            password="test_password",
            license_number="TST00000",
        )

        res = self.client.get(DRIVER_URL)

        self.assertEqual(
            list(res.context["object_list"]),
            list(get_user_model().objects.all())
        )


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self) -> None:
        Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        res = self.client.get(MANUFACTURER_URL, {"name": "test_name"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name="test_name"))
        )

    def test_search_driver_by_username(self) -> None:
        res = self.client.get(DRIVER_URL, {"username": "test_username"})

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            list(res.context["driver_list"]),
            list(get_user_model().objects.filter(username="test_username"))
        )

    def test_search_from_car(self) -> None:
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                country="test", name="test"
            )
        )

        res = self.client.get(CAR_URL, {"model": "test_model"})

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            list(res.context["car_list"]),
            list(Car.objects.filter(model="test_model"))
        )
