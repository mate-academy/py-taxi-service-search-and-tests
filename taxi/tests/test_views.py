from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 302)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="123qwe",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test1", country="test country")
        Manufacturer.objects.create(name="test2", country="test country2")
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["object_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

        res = self.client.get(MANUFACTURER_URL, {"name": "toy"})

        self.assertEqual(
            list(res.context["object_list"]), [toyota])


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 302)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="123qwe",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create_user(
            username="testuser",
            password="qwe123",
            license_number="AAA12349",
        )
        Driver.objects.create_user(
            username="testuser2",
            password="asd123",
            license_number="AAA12348",
        )
        res = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["object_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_driver_by_username(self):
        test_driver = Driver.objects.create_user(
            username="max",
            password="qwe123",
            license_number="AAA12349",
        )
        Driver.objects.create_user(
            username="vlad",
            password="asd123",
            license_number="AAA12348",
        )

        res = self.client.get(DRIVER_URL, {"username": "ma"})
        self.assertEqual(list(res.context["object_list"]), [test_driver])


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 302)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="123qwe",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test country"
        )

    def test_retrieve_car(self):
        Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer,
        )
        res = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["object_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_car_by_model(self):
        expected_car = Car.objects.create(
            model="qwe123",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="asd456",
            manufacturer=self.manufacturer,
        )

        res = self.client.get(CAR_URL, {"model": "qwe"})

        self.assertEqual(list(res.context["object_list"]), [expected_car])
