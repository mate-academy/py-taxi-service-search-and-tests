from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.forms import (
    ManufacturerNameSearchForm,
    CarModelSearchForm,
    DriverUsernameSearchForm,
)
from taxi.models import Manufacturer, Car
from taxi.views import ManufacturerListView, CarListView, DriverListView

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="1qazcde3",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test1")
        Manufacturer.objects.create(name="Test2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_search_form_is_present(self):
        search_form = ManufacturerNameSearchForm()
        response = self.client.get(MANUFACTURER_URL)
        self.assertIsInstance(
            response.context["search_form"],
            type(search_form)
        )

    def test_manufacturer_get_queryset(self):
        Manufacturer.objects.create(name="test")
        request = RequestFactory().get("manufacturers/?name=test")
        view = ManufacturerListView()
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(
            list(queryset),
            list(Manufacturer.objects.filter(name="test"))
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="1qazcde3",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(model="Test1", manufacturer=manufacturer)
        Car.objects.create(model="Test2", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_car_search_form_is_present(self):
        search_form = CarModelSearchForm()
        response = self.client.get(CAR_URL)
        self.assertIsInstance(
            response.context["search_form"],
            type(search_form)
        )

    def test_car_get_queryset(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(model="Test", manufacturer=manufacturer)
        request = RequestFactory().get("cars/?model=Test")
        view = CarListView()
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(
            list(queryset),
            list(Car.objects.filter(model="Test"))
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="1qazcde3",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_driver_search_form_is_present(self):
        search_form = DriverUsernameSearchForm()
        response = self.client.get(DRIVER_URL)
        self.assertIsInstance(
            response.context["search_form"],
            type(search_form)
        )

    def test_driver_get_queryset(self):
        request = RequestFactory().get("cars/?username=test_username")
        view = DriverListView()
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(
            list(queryset),
            list(get_user_model().objects.filter(username="test_username"))
        )
