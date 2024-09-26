from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test1"
        )
        Manufacturer.objects.create(
            name="test2"
        )
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_detail_car_page(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )

        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        res = self.client.get(reverse("taxi:car-detail", args=[car.id]))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test1"
        )
        Car.objects.create(
            model="test2",
            manufacturer=manufacturer
        )
        res = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
