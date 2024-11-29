from django.contrib.auth import get_user, get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_SEARCH_WORD = "Alfa"
DRIVER_SEARCH_WORD = "test1"
CAR_SEARCH_WORD = "X"


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        username = "dimka"
        password = "12345dimka"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Alfa Romeo",
            country="Italy"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        Manufacturer.objects.create(
            name="Alfa Romeo",
            country="Italy"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        res = self.client.get(
            f"{MANUFACTURER_URL}?name={MANUFACTURER_SEARCH_WORD}"
        )
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.filter(
            name__icontains=MANUFACTURER_SEARCH_WORD
        )
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        username = "dimka"
        password = "12345dimka"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create_user(
            username="test1user",
            password="test1user",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="test2user",
            password="test2user",
            license_number="DEF67890"
        )
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_driver(self):
        Driver.objects.create_user(
            username="test1user",
            password="test1user",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="test2user",
            password="test2user",
            license_number="DEF67890"
        )
        res = self.client.get(f"{DRIVER_URL}?username={DRIVER_SEARCH_WORD}")
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.filter(username__icontains=DRIVER_SEARCH_WORD)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        username = "dimka"
        password = "12345dimka"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            )
        )
        Car.objects.create(
            model="S-Class",
            manufacturer=Manufacturer.objects.create(
                name="Mercedes",
                country="Germany"
            )
        )
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_car(self):
        Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            )
        )
        Car.objects.create(
            model="S-Class",
            manufacturer=Manufacturer.objects.create(
                name="Mercedes",
                country="Germany"
            )
        )
        res = self.client.get(f"{CAR_URL}?model={CAR_SEARCH_WORD}")
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.filter(model__icontains=CAR_SEARCH_WORD)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
