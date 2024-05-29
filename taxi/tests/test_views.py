from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


def get_car_detail_url(pk):
    return reverse("taxi:car-detail", args=[pk])


def get_driver_detail_url(pk):
    return reverse("taxi:driver-detail", args=[pk])


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="test_name", country="test_country")
        Manufacturer.objects.create(name="test_name2", country="test_country2")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search_form(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "test_name"})
        form = ManufacturerNameSearchForm(data={"name": "test_name"})
        self.assertTrue(form.is_valid())
        self.assertContains(response, "test_name")


class PublicCarTest(TestCase):
    def test_login_required_for_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_detail(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        response = self.client.get(get_driver_detail_url(car.pk))
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model", manufacturer=self.manufacturer
        )

    def test_retrieve_cars(self):
        Car.objects.create(model="test_model", manufacturer=self.manufacturer)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.select_related("manufacturer")
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail_view(self):
        response = self.client.get(get_car_detail_url(self.car.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_car_search_form(self):
        response = self.client.get(CAR_LIST_URL, {"model": "test_model"})
        form = CarModelSearchForm(data={"model": "test_model"})
        self.assertTrue(form.is_valid())
        self.assertContains(response, "test_model")


class PublicDriverTest(TestCase):
    def test_login_required_for_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_detail(self):
        user = get_user_model().objects.create_user(
            username="username", password="password"
        )
        response = self.client.get(get_driver_detail_url(user.pk))
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            license_number="12345678"
        )

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            license_number="87654321"
        )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "test_driver",
            "password1": "pass1word123",
            "password2": "pass1word123",
            "license_number": "ABC12345",
            "first_name": "test_name",
            "last_name": "test_last_name",
        }
        self.client.post(reverse("taxi:driver-create"), form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])

    def test_driver_detail_view(self):
        response = self.client.get(get_driver_detail_url(self.driver.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_search_form(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver1"})
        form = DriverUsernameSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())
        self.assertContains(response, "driver1")
