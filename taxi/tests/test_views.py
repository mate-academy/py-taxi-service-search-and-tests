from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


CARS_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicCarListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="parker1",
            password="spider123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        Car.objects.create(model="RX7", manufacturer=manufacturer)
        response = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]),
                         list(cars))

    def test_cars_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Tavria",
            country="Ukraine"
        )
        Car.objects.create(model="TavriaNova", manufacturer=manufacturer)
        response = self.client.get(CARS_LIST_URL)
        cars_search = Car.objects.filter(model="TavriaNova")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]),
                         list(cars_search))


class PublicManufacturerListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="parker1",
            password="spider123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Honda", country="Japan")
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Tavria", country="Ukraine")
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturer_search = Manufacturer.objects.filter(name="Tavria")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturer_search))


class PublicDriverListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="parker1",
            password="spider123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="test1",
            password="test123456",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="test2",
            password="test654321",
            license_number="BCA12345"
        )
        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "test3"})
        driver_search = get_user_model().objects.filter(username="test3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(driver_search))
