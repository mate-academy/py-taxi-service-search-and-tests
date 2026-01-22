from django.contrib.auth import get_user_model

from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test1",
            country="USA",
        )
        Manufacturer.objects.create(
            name="test2",
            country="Ukraine",
        )

        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicCarsTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        manufacturer = Manufacturer.objects.create(
            name="Lilit",
            country="Ukraine"
        )

        driver = Driver.objects.create(
            license_number="AAA55555",
            username="Bob25",
            first_name="Bob",
            last_name="Pop",
            password="test_Password1",
        )

        car = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )

        car.drivers.add(driver)

        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)

        cars = Car.objects.all()

        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(res, "taxi/car_list.html")


class PublicDriversTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriversTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Driver.objects.create(
            license_number="AAA51515",
            username="MrAnna",
            first_name="Anna",
            last_name="Dark",
            password="test_Password1",
        )

        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)

        drivers = Driver.objects.all().order_by("username")

        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )

        self.assertTemplateUsed(res, "taxi/driver_list.html")


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="USA",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="Ukraine",
        )
        self.url = MANUFACTURER_URL

    def test_get_context_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertIn("search_form", response.context)

    def test_get_queryset_without_search(self):
        response = self.client.get(self.url)
        manufacturers = Manufacturer.objects.all()

        self.assertQuerysetEqual(
            response.context["manufacturer_list"], manufacturers
        )

    def test_get_queryset_with_search(self):
        response = self.client.get(self.url, {"name": "test1"})

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            1
        )
        self.assertEqual(
            response.context["manufacturer_list"][0],
            self.manufacturer1
        )


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            license_number="AAA11555",
            username="Ruslan15",
            first_name="Ruslan",
            last_name="Topal",
            password="test_Password1"
        )
        self.driver2 = Driver.objects.create(
            license_number="AAA22555",
            username="AnnaDark",
            first_name="Anna",
            last_name="Dark",
            password="test_Password1"
        )
        self.url = DRIVER_URL

    def test_get_context_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("driver_list", response.context)
        self.assertEqual(len(response.context["driver_list"]), 3)
        self.assertIn("search_form", response.context)

    def test_get_queryset_without_search(self):
        response = self.client.get(self.url)
        drivers = Driver.objects.all().order_by("username")

        self.assertQuerysetEqual(
            response.context["driver_list"],
            drivers,
            transform=lambda x: x
        )

    def test_get_queryset_with_search(self):
        response = self.client.get(self.url, {"username": "AnnaDark"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(response.context["driver_list"][0], self.driver2)


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Lilit",
            country="Ukraine"
        )

        self.car1 = Car.objects.create(
            model="KIA",
            manufacturer=manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Tesla",
            manufacturer=manufacturer,
        )
        self.url = CAR_URL

    def test_get_context_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        self.assertEqual(len(response.context["car_list"]), 2)
        self.assertIn("search_form", response.context)

    def test_get_queryset_without_search(self):
        response = self.client.get(self.url)
        manufacturers = Car.objects.all().order_by("model")

        self.assertQuerysetEqual(
            response.context["car_list"],
            manufacturers,
            transform=lambda x: x
        )

    def test_get_queryset_with_search(self):
        response = self.client.get(self.url, {"model": "KIA"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0], self.car1)
