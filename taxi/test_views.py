from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from taxi.forms import CarSearchForm, ManufacturerSearchForm
from taxi.models import Car, Manufacturer, Driver
from taxi.views import CarListView, ManufacturerListView, DriverListView

CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="USERNAME",
            password="<PASSWORD>",
            license_number="TES12345",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Tesla",
            manufacturer=manufacturer
        )
        self.second_car = Car.objects.create(
            model="Lada",
            manufacturer=manufacturer
        )
        self.factory = RequestFactory()

    def test_car_list_retrieve(self):
        car_list = Car.objects.all()
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(
            str(response.context["car_list"]),
            str(car_list)
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )  # template testing

    def test_search_form_car_list(self):
        search_form = CarSearchForm(initial={"model": self.second_car.model})
        self.assertEqual(search_form.initial["model"], self.second_car.model)

    def test_query_set_car_list(self):
        request = self.factory.get(CAR_LIST_URL, {"model": "Lada"})
        car_list_view = CarListView()
        car_list_view.request = request
        query_set = car_list_view.get_queryset()
        expected_queryset = Car.objects.filter(model="Lada")
        self.assertQuerysetEqual(query_set, expected_queryset)


class ManufacturerListViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="<COMPANY>",
            country="<COUNTRY>"
        )
        self.second_manufacturer = Manufacturer.objects.create(
            name="<COMPANY2>",
            country="<COUNTRY2>"
        )
        self.factory = RequestFactory()

    def test_search_form_manufacturer_list(self):
        search_form = ManufacturerSearchForm(
            initial={"name": self.second_manufacturer.name}
        )
        expected_result = self.second_manufacturer.name
        self.assertEqual(
            search_form.initial["name"],
            expected_result
        )

    def test_queryset_manufacturer_list(self):
        request = self.factory.get(
            MANUFACTURER_LIST_URL,
            {"name": self.second_manufacturer.name}
        )
        manufacturer_list_view = ManufacturerListView()
        manufacturer_list_view.request = request
        query_set = manufacturer_list_view.get_queryset()
        expected_queryset = Manufacturer.objects.filter(
            name=self.second_manufacturer.name
        )
        self.assertQuerysetEqual(query_set, expected_queryset)


class DriverListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="<USERNAME>",
            password="<PASSWORD>123",
            license_number="TES12345",
        )
        self.second_user = get_user_model().objects.create_user(
            username="<USERNAME2>",
            password="<PASSWORD>123",
            license_number="ABC12345"
        )
        self.factory = RequestFactory()

    def test_search_form_manufacturer_list(self):
        search_form = ManufacturerSearchForm(
            initial={"username": self.second_user.username}
        )
        expected_result = self.second_user.username
        self.assertEqual(search_form.initial["username"], expected_result)

    def test_queryset_manufacturer_list(self):
        request = self.factory.get(
            DRIVER_LIST_URL,
            {"username": self.second_user.username}
        )
        driver_list_view = DriverListView()
        driver_list_view.request = request
        queryset = driver_list_view.get_queryset()
        expected_queryset = Driver.objects.filter(
            username=self.second_user.username
        )
        self.assertQuerysetEqual(queryset, expected_queryset)
