from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = "taxi:manufacturer-list"
CAR_LIST_URL = "taxi:car-list"
DRIVER_LIST_URL = "taxi:driver-list"
HOME_PAGE_URL = "taxi:index"


class PublicHomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(HOME_PAGE_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123pass"
        )
        self.client.force_login(self.user)

    def test_receive_manufacturers(self):
        Manufacturer.objects.create(name="Name1", country="Ukraine")
        Manufacturer.objects.create(name="Name2", country="Ukraine")

        response = self.client.get(reverse(MANUFACTURER_LIST_URL))
        self.assertEqual(response.status_code, 200)
        manufacturer = list(Manufacturer.objects.all())
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            manufacturer
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):

        response = self.client.get(reverse(CAR_LIST_URL))
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123pass"
        )
        self.client.force_login(self.user)

    def test_receive_cars(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Name1", country="Ukraine"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Name2", country="Ukraine"
        )
        Car.objects.create(
            model="Model1",
            manufacturer=manufacturer1
        )
        Car.objects.create(
            model="Model2",
            manufacturer=manufacturer2
        )
        response = self.client.get(reverse(CAR_LIST_URL))
        self.assertEqual(response.status_code, 200)
        cars = list(Car.objects.all())
        self.assertEqual(
            list(response.context["car_list"]),
            cars
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):

        response = self.client.get(reverse(DRIVER_LIST_URL))
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123pass"
        )
        self.client.force_login(self.user)

    def test_receive_drivers(self):
        Driver.objects.create(
            username="driver.driver",
            password="driver123pass",
            license_number="AAA11111"
        )
        response = self.client.get(reverse(DRIVER_LIST_URL))
        self.assertEqual(response.status_code, 200)
        drivers = list(Driver.objects.all())
        self.assertEqual(
            list(response.context["driver_list"]),
            drivers
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
