from django.contrib.auth import get_user_model
from django.test import TestCase,  Client
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver

INDEX_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


# Index page tests
class PublicIndexTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        resp = self.client.get(INDEX_URL)

        self.assertNotEqual(resp.status_code, 200)

class PrivateIndexTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        resp = self.client.get(INDEX_URL)

        self.assertEqual(resp.status_code, 200)


# Manufacturers page tests
class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        resp = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test1", country="country1")
        Manufacturer.objects.create(name="Test2", country="country2")

        resp = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")


# Car page tests
class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        resp = self.client.get(CAR_URL)

        self.assertNotEqual(resp.status_code, 200)

class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer1 = Manufacturer.objects.create(name="Test1", country="country1")
        manufacturer2 = Manufacturer.objects.create(name="Test2", country="country2")
        Car.objects.create(model="test_model1", manufacturer=manufacturer1)
        Car.objects.create(model="test_model2", manufacturer=manufacturer2)

        resp = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(resp, "taxi/car_list.html")


# Driver page tests
class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        resp = self.client.get(DRIVER_URL)

        self.assertNotEqual(resp.status_code, 200)

class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="driver1",
            password="driver111",
            license_number="BAD11111"
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="driver222",
            license_number="BAD22222"
        )
        get_user_model().objects.create_user(
            username="driver3",
            password="driver333",
            license_number="BAD33333"
        )

        resp = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(resp, "taxi/driver_list.html")
