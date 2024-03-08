from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicTest(TestCase):
    def test_login_required_manufacturer(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="suzuki", country="japan")
        Manufacturer.objects.create(name="toyota", country="Japan")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Driver.objects.create(
            username="test11",
            first_name="test12",
            last_name="test13",
            license_number="TST12345"
        )
        Driver.objects.create(
            username="test21",
            first_name="test22",
            last_name="test23",
            license_number="TST12346"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        driver = Driver.objects.create(
            username="test11",
            first_name="test12",
            last_name="test13",
            license_number="TST12345"
        )
        manufacturer = Manufacturer.objects.create(
            name="toyota",
            country="japan"
        )
        car1 = Car.objects.create(
            model="test1",
            manufacturer=manufacturer
        )
        car1.drivers.set([driver])
        car2 = Car.objects.create(
            model="test2",
            manufacturer=manufacturer
        )
        car2.drivers.set([driver])
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
