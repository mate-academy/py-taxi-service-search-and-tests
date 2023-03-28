from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
MANUFACTURERS_SEARCH_URL = reverse("taxi:manufacturer-list") + "?name=a"
DRIVERS_URL = reverse("taxi:driver-list")
DRIVERS_SEARCH_URL = reverse("taxi:driver-list") + "?username=a"
CAR_URL = reverse("taxi:car-list")
CAR_SEARCH_URL = reverse("taxi:car-list") + "?model=a"


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="lkjhfdsa",
            first_name="Driver",
            last_name="Driverio",
            license_number="OIU29032"
        )
        self.client.force_login(self.driver)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Aang", country="Test")
        Manufacturer.objects.create(name="Ang", country="Test")
        Manufacturer.objects.create(name="Oong", country="Test")
        res = self.client.get(MANUFACTURERS_SEARCH_URL)
        manufacturers = Manufacturer.objects.filter(name__icontains="a")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="lkjhfdsa",
            first_name="Driver",
            last_name="Driverio",
            license_number="OIU29032"
        )
        self.client.force_login(self.driver)

    def test_search_manufacturer_by_name(self):
        get_user_model().objects.create(
            username="user_1",
            password="password",
            license_number="LOI90875"
        )
        get_user_model().objects.create(
            username="user_1a",
            password="password",
            license_number="GOI90875"
        )
        get_user_model().objects.create(
            username="user_1b",
            password="password",
            license_number="LGI90875"
        )
        res = self.client.get(DRIVERS_SEARCH_URL)
        drivers = Driver.objects.filter(username__icontains="a")
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="lkjhfdsa",
            first_name="Driver",
            last_name="Driverio",
            license_number="OIU29032"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="The Creator",
            country="Flatland"
        )
        self.client.force_login(self.driver)

    def test_car_search_by_model(self):
        Car.objects.create(model="RAX", manufacturer=self.manufacturer)
        Car.objects.create(model="RGX", manufacturer=self.manufacturer)
        Car.objects.create(model="Ola", manufacturer=self.manufacturer)
        cars = list(Car.objects.filter(
            model__icontains="a"
        ))
        res = self.client.get(CAR_SEARCH_URL)

        self.assertEqual(
            list(res.context["car_list"]),
            cars,
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
