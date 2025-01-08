from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm, \
    DriverSearchForm, CarSearchForm, ManufacturerSearchForm, \
    validate_license_number
from taxi.models import Manufacturer, Driver, Car


MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")
HOME_FORMAT_URL = reverse("taxi:index")
DRIVER_FORMAT_URL = reverse("taxi:driver-list")
CAR_FORMAT_URL = reverse("taxi:car-list")


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="USA")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            first_name="test",
            last_name="test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="USA")
        car = Car.objects.create(model="model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)


class PublicAccessibilityTest(TestCase):
    def test_login_required(self):
        links = [
            MANUFACTURER_FORMAT_URL,
            HOME_FORMAT_URL,
            DRIVER_FORMAT_URL,
            CAR_FORMAT_URL
        ]
        for value in links:
            res = self.client.get(value)
            self.assertNotEqual(res.status_code, 200)


class PrivateAccessibilityTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",

        )
        self.client.force_login(self.user)

    def test_accessibility_logged_user(self):
        links = [
            MANUFACTURER_FORMAT_URL,
            HOME_FORMAT_URL,
            DRIVER_FORMAT_URL,
            CAR_FORMAT_URL
        ]
        for value in links:
            response = self.client.get(value)
            self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test", country="USA")
        Manufacturer.objects.create(name="test2", country="USA")
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            license_number="DEF67890"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Model S",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_driver(self):
        form_data = {
            "model": "Model S",
            "manufacturer": self.manufacturer.id
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "license_number": "XYZ12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "newdriver",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "license_number": "12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update_form_valid(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_update_form_invalid_license_number(self):
        form_data = {"license_number": "INVALID"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_valid(self):
        form_data = {"username": "testuser"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid(self):
        form_data = {"model": "Model S"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_empty(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "Tesla"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        valid_license = "ABC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_invalid_license_number_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB123")

    def test_invalid_license_number_format(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12XYZ")
