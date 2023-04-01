from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm
from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTets(TestCase):

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="test12",
            first_name="Test",
            last_name="Test",
            license_number="LOL12345"
        )
        Driver.objects.create(
            username="test32",
            first_name="Test",
            last_name="Test",
            license_number="LOL54321"
        )

        res = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )


class PrivateManufacturerTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="VAZ", country="Germany")

        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )


class PrivateCarTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )

        res = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )


class ToggleAssignToCarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="user12345",
            license_number="LOL12345"
        )
        self.car = Car.objects.create(
            model="RAV4",
            manufacturer=self.manufacturer
        )
        self.url = reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id]
        )

    def test_toggle_assign_to_car(self):
        self.client.force_login(self.driver)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car in self.driver.cars.all())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car not in self.driver.cars.all())


class TestSearchForms(TestCase):
    def test_driver_search_form_valid_data(self):
        form = DriverSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_no_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_no_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_no_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
