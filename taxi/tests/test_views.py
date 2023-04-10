from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
MANUFACTURERS_URL_WITH_SEARCH = reverse("taxi:manufacturer-list") + "?name=F"
CARS_URL = reverse("taxi:car-list")
CARS_URL_WITH_SEARCH = reverse("taxi:car-list") + "?model=V"
DRIVERS_URL = reverse("taxi:driver-list")
DRIVERS_URL_WITH_SEARCH = reverse("taxi:driver-list") + "?username=1"
DRIVERS_URL_CREATE = reverse("taxi:driver-create")


class PublicManufacturersTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicCarsTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicDriversTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]), len(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        response = self.client.get(MANUFACTURERS_URL_WITH_SEARCH)

        manufacturers = Manufacturer.objects.filter(name__icontains="F")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Avalon",
            manufacturer=self.manufacturer
        )

    def test_retrieve_car(self):
        response = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), len(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        response = self.client.get(CARS_URL_WITH_SEARCH)

        cars = Car.objects.filter(model__icontains="V")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            username="driver1",
            password="testpass",
            license_number="D001"
        )
        self.driver2 = Driver.objects.create(
            username="driver2",
            password="testpass",
            license_number="D002"
        )
        self.driver3 = Driver.objects.create(
            username="driver3",
            password="testpass",
            license_number="D003"
        )

    def test_retrieve_driver(self):
        response = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), len(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        response = self.client.get(DRIVERS_URL_WITH_SEARCH)

        drivers = Driver.objects.filter(username__icontains="1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
