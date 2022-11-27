from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicAllViewsTests(TestCase):
    def test_login_required_manufacture(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="maxitoska",
            license_number="ABM34567"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        res = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="sergey_vlog",
            license_number="BNH32627"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="X1",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="I7",
            manufacturer=manufacturer
        )

        res = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="maxitoska",
            license_number="ABM34567",
            password="max12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="kitty",
            license_number="MBA23456",
            password="kitty123"
        )
        get_user_model().objects.create_user(
            username="tom_and_jarry",
            license_number="JAR56834",
            password="4567865tom"
        )

        res = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="maxitoska",
            license_number="JKQ12345"
        )
        self.client.force_login(self.user)

    def test_search_drivers_by_username(self):
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?name=maxitoska")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="maxitoska")),
        )

    def test_search_cars_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?name=Civic")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="Civic")),
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?name=Honda")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Honda")),
        )
