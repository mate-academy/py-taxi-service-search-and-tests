from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test",
            country="TestCountry"
        )
        Manufacturer.objects.create(
            name="Test2",
            country="TestCountry2"
        )

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_with_search(self):
        response = self.client.get(MANUFACTURER_URL + "?name=B")

        manufacturers = Manufacturer.objects.filter(name__icontains="B")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpass123",
            first_name="TestFirst",
            last_name="TestLast",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Car.objects.create(model="TestModel1", manufacturer=self.manufacturer)
        Car.objects.create(model="TestModel2", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        cars = list(Car.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            cars,
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_with_search(self):
        cars = list(Car.objects.filter(
            model__icontains="t"
        ))
        response = self.client.get(CAR_URL + "?model=t")

        self.assertEqual(
            list(response.context["car_list"]),
            cars,
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpass123",
            first_name="TestFirst",
            last_name="TestLast",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="test2",
            password="testpass456",
            first_name="TestFirst2",
            last_name="TestLast2",
            license_number="TES67890"
        )
        get_user_model().objects.create_user(
            username="test3",
            password="testpass1",
            first_name="TestFirst3",
            last_name="Super",
            license_number="MSP12345"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        drivers = list(get_user_model().objects.all())
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            drivers,
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_drivers_after_searching_by_username(self):
        drivers = list(get_user_model().objects.filter(
            username__icontains="te"
        ))
        response = self.client.get(DRIVER_URL, {"username": "te"})

        self.assertEqual(
            list(response.context["driver_list"]),
            drivers,
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")