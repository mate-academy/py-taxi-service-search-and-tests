from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from taxi.views import DriverListView, CarListView, ManufacturerListView

from taxi.forms import (
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerListView(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="TestPassword123"
        )
        self.factory = RequestFactory()
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test1")
        manufacturer = Manufacturer.objects.all()

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_context_data_manufacturer(self):
        response = self.client.get(
            "/manufacturers/",
            {"name": "test_name"}
        )
        context = response.context_data
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            context["search_form"],
            ManufacturerNameSearchForm
        )
        self.assertEqual(context["search_form"].initial["name"], "test_name")

    def test_queryset_manufacturer(self):
        Manufacturer.objects.create(name="test_name")

        url = reverse("taxi:manufacturer-list")
        request = self.factory.get(url, {"name": "test"})
        request.user = self.user

        response = ManufacturerListView.as_view()(request)

        self.assertQuerysetEqual(
            list(response.context_data["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="test"))
        )


class PublicCarListView(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_pass"
        )

        self.factory = RequestFactory()
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(name="test1"),
        )
        car = Car.objects.all()

        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_get_context_data_car(self):
        response = self.client.get(
            "/cars",
            {"model": "test_model"},
            follow=True
        )
        context = response.context_data

        self.assertIsInstance(context["search_form"], CarModelSearchForm)
        self.assertIn("search_form", context)
        self.assertEqual(context["search_form"].initial["model"], "test_model")

    def test_queryset_car(self):
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(name="test1"),
        )

        url = reverse("taxi:car-list")
        request = self.factory.get(url, {"model": "test"})
        request.user = self.user

        response = CarListView.as_view()(request)

        self.assertQuerysetEqual(
            list(response.context_data["car_list"]),
            list(Car.objects.filter(model__icontains="test"))
        )


class PublicDriverListView(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_pass"
        )

        self.factory = RequestFactory()
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="test_driver",
            password="test_pass",
            license_number="TES12345"
        )
        driver = Driver.objects.all()

        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200),
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_get_context_data_driver(self):
        response = self.client.get(
            "/drivers/",
            {"username": "test_user"}
        )
        context = response.context_data

        self.assertIsInstance(context["search_form"], DriverUsernameSearchForm)
        self.assertIn("search_form", context)
        self.assertEqual(
            context["search_form"].initial["username"],
            "test_user"
        )

    def test_get_queryset_driver(self):
        Driver.objects.create(
            username="test_driver",
            password="test_pass",
            license_number="TES12345"
        )

        url = reverse("taxi:driver-list")
        request = self.factory.get(url, {"username": "test"})
        request.user = self.user

        response = DriverListView.as_view()(request)

        self.assertQuerysetEqual(
            list(response.context_data["driver_list"]),
            list(Driver.objects.filter(username__icontains="test")))
