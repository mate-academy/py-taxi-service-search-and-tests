from http.client import responses

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (DriverCreationForm,
                        DriversUsernameSearchForm,
                        CarModelSearchForm,
                        ManufacturerNameSearchForm)
from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Test",
                                                   country="Testilania")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="Test Username",
            password="PASSWORD",
            first_name="Test Firstname",
            last_name="Test Lastname",
            license_number="ABC12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicUserViewTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateUserViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test Username",
            password="PASSWORD",
            first_name="Test Firstname",
            last_name="Test Lastname",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car1 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Volvo", country="Switzerland")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturer_list))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_drivers(self):
        Driver.objects.create_user(
            username="Lewis Hamilton",
            password="PASSWORD",
            first_name="Lewis",
            last_name="Hamilton",
            license_number="LHC12345"
        )
        Driver.objects.create_user(
            username="Michael Schumacher",
            password="PASSWORD",
            first_name="Michael",
            last_name="Schumacher",
            license_number="MSC12345"
        )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        driver_list = Driver.objects.all()
        self.assertEqual(list(
            response.context["driver_list"]), list(driver_list)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

        car_list = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car_list))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_toggle_assign_to_car(self):
        self.car1.drivers.add(self.user)
        self.assertIn(self.car1, self.user.cars.all())


class FormTests(TestCase):
    def test_user_creation_form_with_username_first_last_name_is_valid(self):
        form_data = {
            "username": "Lewis_Hamilton",
            "password1": "Password123!",
            "password2": "Password123!",
            "license_number": "LHC12345",
            "first_name": "Lewis",
            "last_name": "Hamilton"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validator_license_number(self):
        license_number = "ABC12345"

        self.assertEqual(len(license_number), 8)
        self.assertTrue(license_number[:3].isupper())
        self.assertTrue(license_number[:3].isalpha())
        self.assertTrue(license_number[3:].isdigit())


class DriversUsernameSearchFormTest(TestCase):
    def test_drivers_form_valid_with_username(self):
        form_data = {"username": "test user"}
        form = DriversUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_drivers_form_valid_with_empty_username(self):
        form_data = {"username": ""}
        form = DriversUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_drivers_form_invalid_with_long_username(self):
        form_data = {"username": "a" * 256}
        form = DriversUsernameSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_drivers_form_label_is_empty(self):
        form = DriversUsernameSearchForm()
        self.assertEqual(form["username"].label, "")

    def test_drivers_form_has_placeholder(self):
        form = DriversUsernameSearchForm()
        placeholder = form["username"].field.widget.attrs["placeholder"]
        self.assertEqual(placeholder, "Search by username")


class CarModelSearchFormTest(TestCase):
    def test_car_form_valid_with_model(self):
        form_data = {"model": "test model"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_valid_with_empty_model(self):
        form_data = {"model": ""}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_with_long_model(self):
        form_data = {"model": "a" * 256}
        form = CarModelSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_car_form_label_is_empty(self):
        form = CarModelSearchForm()
        self.assertEqual(form["model"].label, "")

    def test_car_form_has_placeholder(self):
        form = CarModelSearchForm()
        placeholder = form["model"].field.widget.attrs["placeholder"]
        self.assertEqual(placeholder, "Search by model")


class ManufacturerNameSearchFormTest(TestCase):
    def test_manufacturer_form_valid_with_name(self):
        form_data = {"name": "test name"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_form_valid_with_empty_name(self):
        form_data = {"name": ""}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_form_invalid_with_long_name(self):
        form_data = {"name": "a" * 256}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_manufacturer_form_label_is_empty(self):
        form = ManufacturerNameSearchForm()
        self.assertEqual(form["name"].label, "")

    def test_manufacturer_form_has_placeholder(self):
        form = ManufacturerNameSearchForm()
        placeholder = form["name"].field.widget.attrs["placeholder"]
        self.assertEqual(placeholder, "Search by name")
